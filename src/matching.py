"""Busca visual com CLIP: embeddings, cache em memória e ranking por similaridade de cosseno."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from src.image_service import load_image


class ModelLoadError(RuntimeError):
    """Falha ao carregar o modelo CLIP (ex.: sem internet no primeiro uso)."""


@dataclass
class Match:
    report: dict
    score: float
    level: str


def similarity_level(score: float) -> str:
    if score >= 0.90:
        return "alta"
    if score >= 0.80:
        return "média"
    return "baixa"


def _to_tensor(features):
    """Compatível com transformers 4.x (tensor) e 5.x (objeto com pooler_output)."""
    if hasattr(features, "cpu"):
        return features
    for attr in ("image_embeds", "pooler_output"):
        value = getattr(features, attr, None)
        if value is not None:
            return value
    raise TypeError(f"Retorno inesperado do CLIP: {type(features)!r}")


class ClipEmbedder:
    """Carrega o CLIP sob demanda e transforma uma imagem PIL em vetor normalizado."""

    def __init__(self, model_name: str = "openai/clip-vit-base-patch32") -> None:
        self.model_name = model_name
        self._model = None
        self._processor = None

    def _load(self) -> None:
        if self._model is not None:
            return
        try:
            from transformers import CLIPModel, CLIPProcessor

            self._processor = CLIPProcessor.from_pretrained(self.model_name)
            self._model = CLIPModel.from_pretrained(self.model_name)
            self._model.eval()
        except Exception as exc:
            raise ModelLoadError(f"Não foi possível carregar o modelo CLIP: {exc}") from exc

    def __call__(self, image) -> np.ndarray:
        import torch

        self._load()
        inputs = self._processor(images=image.convert("RGB"), return_tensors="pt")
        with torch.no_grad():
            features = _to_tensor(self._model.get_image_features(**inputs))
        vector = features.cpu().numpy()[0].astype("float32")
        norm = np.linalg.norm(vector)
        return vector / norm if norm else vector


class EmbeddingCache:
    """Guarda em memória o embedding de cada imagem cadastrada."""

    def __init__(self, embedder: Callable) -> None:
        self.embedder = embedder
        self._vectors: dict[str, np.ndarray] = {}

    def get(self, report: dict) -> np.ndarray | None:
        path = report.get("image_path", "")
        if path in self._vectors:
            return self._vectors[path]
        image = load_image(path)
        if image is None:
            return None
        vector = self.embedder(image)
        self._vectors[path] = vector
        return vector


def rank_candidates(
    query: np.ndarray,
    reports: list[dict],
    cache: EmbeddingCache,
    top_k: int = 5,
    species: str | None = None,
    report_type: str | None = None,
) -> tuple[list[Match], int]:
    """Retorna (melhores correspondências, quantidade de registros sem imagem local)."""
    matches: list[Match] = []
    missing = 0
    for report in reports:
        if species and report.get("species") != species:
            continue
        if report_type and report.get("report_type") != report_type:
            continue
        vector = cache.get(report)
        if vector is None:
            missing += 1
            continue
        score = float(np.dot(query, vector))
        matches.append(Match(report=report, score=score, level=similarity_level(score)))
    matches.sort(key=lambda m: m.score, reverse=True)
    return matches[:top_k], missing
