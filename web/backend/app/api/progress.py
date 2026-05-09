"""Progress routes."""
from datetime import datetime

from fastapi import APIRouter

from app.schemas.progress import ProgressUpdate
from app.services import data_service, module_service

router = APIRouter(prefix="/api", tags=["progress"])


@router.get("/progress")
def get_progress():
    """Get current learning progress."""
    return data_service.load_progress()


@router.post("/progress")
def update_progress(update: ProgressUpdate):
    """Update module completion status."""
    progress = data_service.load_progress()
    if progress["started_at"] is None:
        progress["started_at"] = datetime.now().isoformat()
    if update.completed:
        if update.module_id not in progress["completed"]:
            progress["completed"].append(update.module_id)
    else:
        progress["completed"] = [m for m in progress["completed"] if m != update.module_id]
    data_service.save_progress(progress)
    return {"ok": True, "completed": len(progress["completed"])}


@router.get("/stats")
def get_stats():
    """Get overall completion stats."""
    progress = data_service.load_progress()
    total = module_service.module_count()
    done = len(progress["completed"])
    return {
        "total": total,
        "completed": done,
        "percentage": round(done / total * 100) if total else 0,
    }
