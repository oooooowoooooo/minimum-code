"""Pydantic models for progress tracking."""
from pydantic import BaseModel


class ProgressUpdate(BaseModel):
    module_id: str
    completed: bool
