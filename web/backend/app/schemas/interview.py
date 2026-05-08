"""Pydantic models for interview expression generation."""
from pydantic import BaseModel


class STARMethod(BaseModel):
    situation: str
    task: str
    action: str
    result: str


class InterviewExpression(BaseModel):
    lab_id: str
    title: str
    bullet_points: list[str]
    star_method: STARMethod


class InterviewRequest(BaseModel):
    completed_labs: list[str]
    target_role: str = "AI Application Developer"


class InterviewResponse(BaseModel):
    expressions: list[InterviewExpression]
