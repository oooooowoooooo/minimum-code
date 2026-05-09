"""Shared filesystem paths for the backend."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]
BACKEND_DIR = PROJECT_ROOT / "web" / "backend"
DATA_DIR = BACKEND_DIR / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)
