"""JSON file read/write repository."""
import json

from app.core.paths import DATA_DIR


def read_json(filename: str, default=None):
    """Read a JSON file from the data directory. Returns default if not found."""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        return default if default is not None else {}
    return json.loads(filepath.read_text(encoding="utf-8"))


def write_json(filename: str, data):
    """Write data to a JSON file in the data directory."""
    filepath = DATA_DIR / filename
    filepath.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def file_exists(filename: str) -> bool:
    """Check if a file exists in the data directory."""
    return (DATA_DIR / filename).exists()
