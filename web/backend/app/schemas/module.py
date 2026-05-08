"""Pydantic models for modules."""
from typing import Optional
from pydantic import BaseModel


class ModuleInfo(BaseModel):
    id: str
    title: str
    category: str
    icon: str
    description: str
    week: int
    order: int


class Section(BaseModel):
    title: str
    content: str
    type: str = "text"  # text, code, exercise
    language: Optional[str] = None


class ModuleContent(BaseModel):
    id: str
    title: str
    category: str
    icon: str
    sections: list[Section]


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    correct: int
    explanation: str
