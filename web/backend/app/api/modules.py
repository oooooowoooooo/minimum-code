"""Module routes: list modules, get module content, quizzes."""
from fastapi import APIRouter, HTTPException

from app.schemas.module import ModuleContent, ModuleInfo, QuizQuestion
from app.services import module_service, quiz_service

router = APIRouter(prefix="/api/modules", tags=["modules"])


@router.get("", response_model=list[ModuleInfo])
def list_modules():
    """List all modules."""
    return module_service.list_modules()


@router.get("/{module_id}", response_model=ModuleContent)
def get_module(module_id: str):
    """Get module content by ID."""
    module = module_service.get_module_content(module_id)
    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")
    return module


@router.get("/{module_id}/quiz", response_model=list[QuizQuestion])
def get_quiz(module_id: str):
    """Get quiz questions for a module."""
    return quiz_service.get_module_quiz(module_id)
