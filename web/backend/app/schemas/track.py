"""Pydantic models for competency tracks."""
from typing import Optional
from pydantic import BaseModel


class Skill(BaseModel):
    id: str
    title: str
    description: str = ""
    level: str = "beginner"  # beginner, intermediate, advanced, expert


class Track(BaseModel):
    id: str
    title: str
    description: str
    icon: str = ""
    skills: list[Skill] = []


class TrackSummary(BaseModel):
    id: str
    title: str
    description: str
    icon: str = ""
    skill_count: int = 0
