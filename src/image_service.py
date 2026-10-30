"""Serviço de validação, armazenamento e leitura de imagens."""
from __future__ import annotations

import io
import uuid
from pathlib import Path

from PIL import Image, UnidentifiedImageError


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MIN_DIMENSION = 50  # pixels


class ImageValidationError(Exception):
    pass


def validate_image(data: bytes, filename: str, max_mb: int = 5) -> Image.Image:
    """Valida extensão, tamanho e conteúdo real da imagem. Retorna PIL Image."""
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ImageValidationError(f"Extensão não permitida: {ext}. Use jpg, jpeg, png ou webp.")

    max_bytes = max_mb * 1024 * 1024
    if len(data) > max_bytes:
        raise ImageValidationError(f"Arquivo muito grande. Limite: {max_mb} MB.")

    try:
        img = Image.open(io.BytesIO(data))
        img.verify()  # detecta arquivos corrompidos
        img = Image.open(io.BytesIO(data))  # reabre após verify()
        img = img.convert("RGB")
    except UnidentifiedImageError:
        raise ImageValidationError("O arquivo não é uma imagem válida.")
    except Exception as exc:
        raise ImageValidationError(f"Erro ao processar imagem: {exc}") from exc

    if img.width < MIN_DIMENSION or img.height < MIN_DIMENSION:
        raise ImageValidationError(f"Imagem muito pequena. Mínimo: {MIN_DIMENSION}x{MIN_DIMENSION} px.")

    # Remove metadados EXIF
    clean = Image.new(img.mode, img.size)
    clean.putdata(list(img.getdata()))
    return clean


def save_image(image: Image.Image, images_dir: Path) -> str:
    """Salva a imagem em disco e retorna o caminho relativo."""
    images_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.jpg"
    path = images_dir / filename
    image.save(path, format="JPEG", quality=85)
    return str(path)


def load_image(image_path: str) -> Image.Image | None:
    """Carrega uma imagem do disco. Retorna None se não encontrada."""
    try:
        path = Path(image_path)
        if not path.exists():
            return None
        return Image.open(path).convert("RGB")
    except Exception:
        return None
