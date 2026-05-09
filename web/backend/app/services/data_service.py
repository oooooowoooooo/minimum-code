"""Knowledge-point and progress data service."""
from app.repositories import json_repository

_knowledge_points_data: dict = {"total_points": 0, "weeks": 0, "points": []}


def load_knowledge_points() -> None:
    """Load knowledge points from JSON into the in-memory cache."""
    global _knowledge_points_data
    data = json_repository.read_json("knowledge_points.json")
    if data:
        _knowledge_points_data = data


def get_knowledge_points_data() -> dict:
    """Return the cached knowledge-points data."""
    return _knowledge_points_data


def load_progress() -> dict:
    """Load progress from JSON file."""
    return json_repository.read_json(
        "progress.json",
        default={"completed": [], "started_at": None},
    )


def save_progress(data: dict) -> None:
    """Save progress to JSON file."""
    json_repository.write_json("progress.json", data)
