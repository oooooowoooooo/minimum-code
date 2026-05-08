"""Pydantic models for labs."""
from typing import Optional
from pydantic import BaseModel


class AcceptanceCriterion(BaseModel):
    id: str
    description: str
    test_hint: str = ""


class Lab(BaseModel):
    id: str
    title: str
    description: str
    track_id: str
    difficulty: str = "beginner"
    starter_code: str = ""
    acceptance_criteria: list[AcceptanceCriterion] = []
    hints: list[str] = []


class LabSummary(BaseModel):
    id: str
    title: str
    description: str
    track_id: str
    difficulty: str = "beginner"
