import os
import json
from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from ..models.base import Base

CONFIG_DIR = Path.home() / ".accountant_app"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_SQLITE_DB = CONFIG_DIR / "app.sqlite"

_engine = None
_SessionLocal = None


def _load_db_url() -> Optional[str]:
	# Prefer environment variable if set
	db_url = os.getenv("DB_URL")
	if db_url:
		return db_url
	if CONFIG_FILE.exists():
		try:
			with open(CONFIG_FILE, "r", encoding="utf-8") as f:
				data = json.load(f)
				return data.get("db_url")
		except Exception:
			return None
	return None


def _fallback_sqlite_url() -> str:
	CONFIG_DIR.mkdir(parents=True, exist_ok=True)
	return f"sqlite:///{DEFAULT_SQLITE_DB}"


def get_engine():
	global _engine
	if _engine is None:
		db_url = _load_db_url()
		if not db_url:
			# Fallback to local SQLite for first-run/demo
			db_url = _fallback_sqlite_url()
		_engine = create_engine(db_url, pool_pre_ping=True)
	return _engine


def get_session() -> Session:
	global _SessionLocal
	if _SessionLocal is None:
		_SessionLocal = sessionmaker(bind=get_engine(), expire_on_commit=False)
	return _SessionLocal()


def initialize_database() -> None:
	# Import models to register them with Base
	from .. import models  # noqa: F401
	Base.metadata.create_all(bind=get_engine())