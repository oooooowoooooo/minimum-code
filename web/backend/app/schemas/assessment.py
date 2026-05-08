"""Pydantic models for assessment."""
from pydantic import BaseModel


class AssessmentOption(BaseModel):
    id: int
    text: str


class AssessmentQuestion(BaseModel):
    id: str
    question: str
    options: list[AssessmentOption]
    correct: int
    track_id: str
    explanation: str = ""


class AssessmentSubmission(BaseModel):
    answers: dict[str, int]


class TrackScore(BaseModel):
    score: int
    max: int
    level: str


class AssessmentResult(BaseModel):
    total_score: int
    max_score: int
    tracks: dict[str, TrackScore]
