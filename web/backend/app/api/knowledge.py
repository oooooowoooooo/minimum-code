"""Knowledge points routes."""
import random
from typing import Optional

from fastapi import APIRouter, HTTPException

from app.services import data_service

router = APIRouter(prefix="/api/knowledge-points", tags=["knowledge-points"])


@router.get("/stats")
def get_knowledge_points_stats():
    """Return aggregate statistics about knowledge points."""
    points = data_service.get_knowledge_points_data().get("points", [])
    points_per_week: dict[str, int] = {}
    points_per_module: dict[str, int] = {}
    games_per_type: dict[str, int] = {}
    for p in points:
        w = str(p["week"])
        m = p["module"]
        points_per_week[w] = points_per_week.get(w, 0) + 1
        points_per_module[m] = points_per_module.get(m, 0) + 1
        game = p.get("game")
        if game and game.get("type"):
            gt = game["type"]
            games_per_type[gt] = games_per_type.get(gt, 0) + 1
    return {
        "total_points": len(points),
        "points_per_week": points_per_week,
        "points_per_module": points_per_module,
        "games_per_type": games_per_type,
    }


@router.get("")
def list_knowledge_points(
    week: Optional[int] = None,
    module: Optional[str] = None,
    search: Optional[str] = None,
    game_type: Optional[str] = None,
    page: int = 1,
    per_page: int = 20,
):
    """Return all knowledge points with optional filtering and pagination."""
    points = data_service.get_knowledge_points_data().get("points", [])

    if week is not None:
        points = [p for p in points if p["week"] == week]
    if module is not None:
        points = [p for p in points if p["module"] == module]
    if search is not None:
        q = search.lower()
        points = [p for p in points if q in p.get("title", "").lower() or q in p.get("explanation", "").lower()]
    if game_type is not None:
        points = [p for p in points if p.get("game", {}).get("type") == game_type]

    total = len(points)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = points[start:end]

    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page if per_page > 0 else 0,
        "points": paginated,
    }


@router.get("/random")
def get_random_knowledge_points(count: int = 10):
    """Return random knowledge points for review."""
    points = data_service.get_knowledge_points_data().get("points", [])
    if not points:
        raise HTTPException(status_code=404, detail="No knowledge points available")
    count = max(1, min(count, 100, len(points)))
    sampled = random.sample(points, count)
    return {"count": len(sampled), "points": sampled}


@router.get("/id/{point_id}")
def get_knowledge_point_by_id(point_id: int):
    """Return a single knowledge point by its index in the array."""
    points = data_service.get_knowledge_points_data().get("points", [])
    if point_id < 0 or point_id >= len(points):
        raise HTTPException(status_code=404, detail=f"Knowledge point {point_id} not found (valid range: 0-{len(points)-1})")
    return {"id": point_id, "point": points[point_id]}


@router.get("/by-week/{week}")
def get_knowledge_points_by_week(week: int):
    """Return all knowledge points for a specific week."""
    points = [p for p in data_service.get_knowledge_points_data().get("points", []) if p["week"] == week]
    if not points:
        raise HTTPException(status_code=404, detail=f"No knowledge points found for week {week}")
    return {"week": week, "count": len(points), "points": points}
