"""Interview expression routes."""
from fastapi import APIRouter

from app.schemas.interview import InterviewRequest, InterviewResponse, InterviewExpression, STARMethod
from app.services import interview_service

router = APIRouter(prefix="/api/interview", tags=["interview"])


@router.post("/generate", response_model=InterviewResponse)
def generate_expressions(request: InterviewRequest):
    """Generate interview expressions from completed labs."""
    raw = interview_service.generate_expressions(
        completed_labs=request.completed_labs,
        target_role=request.target_role,
    )
    expressions = [
        InterviewExpression(
            lab_id=expr["lab_id"],
            title=expr["title"],
            bullet_points=expr["bullet_points"],
            star_method=STARMethod(**expr["star_method"]),
        )
        for expr in raw
    ]
    return InterviewResponse(expressions=expressions)
