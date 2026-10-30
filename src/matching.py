"""Busca visual usando CLIP para gerar embeddings e similaridade de cosseno."""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image


class ModelLoadError(Exception):
    pass


class ClipEmbedder:
    """Carrega o modelo CLIP e gera embeddings de imagens."""

    def __init__(self, model_name: str = "openai/clip-vit-base-patch32") -> None:
        try:
            import torch
            from transformers import CLIPModel, CLIPProcessor

            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.processor = CLIPProcessor.from_pretrained(model_name)
            self.model = CLIPModel.from_pretrained(model_name).to(self.device)
            self.model.eval()
        except Exception as exc:
            raise ModelLoadError(f"Não foi possível carregar o modelo CLIP ({model_name}): {exc}") from exc

    def __call__(self, image: Image.Image) -> np.ndarray:
        """Gera embedding normalizado para uma imagem PIL."""
        import torch

        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            features = self.model.get_image_features(**inputs)
        vec = features.cpu().numpy()[0]
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec


class EmbeddingCache:
    """Mantém embeddings em memória para evitar reprocessamento."""

    def __init__(self, embedder: ClipEmbedder) -> None:
        self.embedder = embedder
        self._cache: dict[str, np.ndarray] = {}

    def get(self, image_path: str) -> Optional[np.ndarray]:
        if image_path in self._cache:
            return self._cache[image_path]
        try:
            img = Image.open(Path(image_path)).convert("RGB")
            embedding = self.embedder(img)
            self._cache[image_path] = embedding
            return embedding
        except Exception:
            return None


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))


def _similarity_level(score: float) -> str:
    if score >= 0.90:
        return "alta"
    if score >= 0.75:
        return "média"
    return "baixa"


@dataclass
class MatchResult:
    report: dict
    score: float
    level: str = field(init=False)

    def __post_init__(self):
        self.level = _similarity_level(self.score)


def rank_candidates(
    query_embedding: np.ndarray,
    reports: list[dict],
    cache: EmbeddingCache,
    top_k: int = 5,
    species: Optional[str] = None,
    report_type: Optional[str] = None,
) -> tuple[list[MatchResult], int]:
    """
    Compara o embedding da query com os registros e retorna os mais semelhantes.

    Retorna (matches, missing) onde missing é o número de registros sem imagem disponível.
    """
    results: list[MatchResult] = []
    missing = 0

    for report in reports:
        if species and report.get("species") != species:
            continue
        if report_type and report.get("report_type") != report_type:
            continue

        image_path = report.get("image_path", "")
        embedding = cache.get(image_path)
        if embedding is None:
            missing += 1
            continue

        score = cosine_similarity(query_embedding, embedding)
        results.append(MatchResult(report=report, score=score))

    results.sort(key=lambda r: r.score, reverse=True)
    return results[:top_k], missing
