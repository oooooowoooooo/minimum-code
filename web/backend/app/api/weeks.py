"""Weeks route."""
from fastapi import APIRouter

from app.services import data_service

router = APIRouter(prefix="/api", tags=["weeks"])


@router.get("/weeks")
def list_weeks():
    """Return list of weeks with their modules and point counts."""
    points = data_service.get_knowledge_points_data().get("points", [])
    weeks_map: dict[int, dict] = {}
    for p in points:
        w = p["week"]
        m = p["module"]
        if w not in weeks_map:
            weeks_map[w] = {"week": w, "modules": {}}
        if m not in weeks_map[w]["modules"]:
            weeks_map[w]["modules"][m] = {"module": m, "count": 0}
        weeks_map[w]["modules"][m]["count"] += 1

    result = []
    for w in sorted(weeks_map):
        entry = weeks_map[w]
        result.append({
            "week": entry["week"],
            "modules": list(entry["modules"].values()),
            "total_points": sum(md["count"] for md in entry["modules"].values()),
        })
    return result
