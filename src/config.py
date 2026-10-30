"""Configurações da aplicação via variáveis de ambiente."""
from __future__ import annotations

from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    def __init__(self):
        self.supabase_url: str = os.getenv("SUPABASE_URL", "")
        self.supabase_key: str = os.getenv("SUPABASE_KEY", "")
        self.supabase_table: str = os.getenv("SUPABASE_TABLE", "animal_reports")
        self.images_dir: Path = Path(os.getenv("IMAGES_DIR", "data/images"))
        self.demo_db_path: Path = Path(os.getenv("DEMO_DB_PATH", "data/demo_db.json"))
        self.clip_model_name: str = os.getenv("CLIP_MODEL_NAME", "openai/clip-vit-base-patch32")
        self.max_upload_mb: int = int(os.getenv("MAX_UPLOAD_MB", "5"))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
