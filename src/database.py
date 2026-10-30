"""Camada de acesso a dados: Supabase ou repositório local para demonstração."""
from __future__ import annotations

import json
import uuid
from datetime import date, datetime
from pathlib import Path
from typing import Any

REPORT_TYPES = ["perdido", "encontrado"]
SPECIES = ["cachorro", "gato", "pássaro", "coelho", "outro"]


class DatabaseError(Exception):
    pass


class ValidationError(Exception):
    pass


def validate_report(report: dict) -> None:
    """Valida os campos obrigatórios de um registro."""
    required = ["report_type", "species", "color", "event_date", "city"]
    for field in required:
        if not report.get(field):
            raise ValidationError(f"Campo obrigatório ausente: {field}")
    if report["report_type"] not in REPORT_TYPES:
        raise ValidationError(f"Tipo inválido: {report['report_type']}")
    if report["species"] not in SPECIES:
        raise ValidationError(f"Espécie inválida: {report['species']}")
    for coord in ("latitude", "longitude"):
        val = report.get(coord)
        if val not in (None, ""):
            try:
                float(val)
            except (TypeError, ValueError):
                raise ValidationError(f"{coord} deve ser um número decimal.")


def _serialize(obj: Any) -> Any:
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    return str(obj)


class LocalRepository:
    """Repositório local em JSON para modo demonstração."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            self.db_path.write_text("[]", encoding="utf-8")

    def _load(self) -> list[dict]:
        try:
            return json.loads(self.db_path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise DatabaseError(f"Erro ao ler banco local: {exc}") from exc

    def _save(self, data: list[dict]) -> None:
        try:
            self.db_path.write_text(
                json.dumps(data, default=_serialize, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception as exc:
            raise DatabaseError(f"Erro ao salvar banco local: {exc}") from exc

    def add_report(self, report: dict) -> dict:
        data = self._load()
        record = {**report, "id": str(uuid.uuid4()), "created_at": datetime.now().isoformat()}
        # serializa datas
        for key, val in record.items():
            if isinstance(val, (date, datetime)):
                record[key] = val.isoformat()
        data.append(record)
        self._save(data)
        return record

    def list_reports(self) -> list[dict]:
        return self._load()


class SupabaseRepository:
    """Repositório usando Supabase como backend."""

    def __init__(self, url: str, key: str, table: str) -> None:
        try:
            from supabase import create_client
            self.client = create_client(url, key)
        except Exception as exc:
            raise DatabaseError(f"Falha ao conectar ao Supabase: {exc}") from exc
        self.table = table

    def add_report(self, report: dict) -> dict:
        payload = {}
        for key, val in report.items():
            if isinstance(val, (date, datetime)):
                payload[key] = val.isoformat()
            elif val == "":
                payload[key] = None
            else:
                payload[key] = val
        try:
            result = self.client.table(self.table).insert(payload).execute()
            return result.data[0] if result.data else payload
        except Exception as exc:
            raise DatabaseError(f"Erro ao salvar no Supabase: {exc}") from exc

    def list_reports(self) -> list[dict]:
        try:
            result = self.client.table(self.table).select("*").order("created_at", desc=True).execute()
            return result.data or []
        except Exception as exc:
            raise DatabaseError(f"Erro ao consultar o Supabase: {exc}") from exc


def get_repository(settings) -> LocalRepository | SupabaseRepository:
    """Retorna o repositório adequado conforme as configurações."""
    if settings.supabase_url and settings.supabase_key:
        return SupabaseRepository(settings.supabase_url, settings.supabase_key, settings.supabase_table)
    return LocalRepository(settings.demo_db_path)
