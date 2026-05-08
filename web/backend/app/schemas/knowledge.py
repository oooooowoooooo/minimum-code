"""Pydantic models for knowledge points (shared types)."""
from typing import Optional
from pydantic import BaseModel


class KnowledgePointFilter(BaseModel):
    week: Optional[int] = None
    module: Optional[str] = None
    search: Optional[str] = None
    game_type: Optional[str] = None
    page: int = 1
    per_page: int = 20
