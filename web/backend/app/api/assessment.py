"""Assessment routes."""
from fastapi import APIRouter

from app.schemas.assessment import AssessmentQuestion, AssessmentOption, AssessmentSubmission, AssessmentResult, TrackScore
from app.services import assessment_service

router = APIRouter(prefix="/api/assessment", tags=["assessment"])


@router.get("/questions", response_model=list[AssessmentQuestion])
def get_questions():
    """Get all assessment questions."""
    raw = assessment_service.load_questions()
    return [
        AssessmentQuestion(
            id=q["id"],
            question=q["question"],
            options=[AssessmentOption(**opt) for opt in q["options"]],
            correct=q["correct"],
            track_id=q["track_id"],
            explanation=q.get("explanation", ""),
        )
        for q in raw
    ]


@router.post("/submit", response_model=AssessmentResult)
def submit_answers(submission: AssessmentSubmission):
    """Submit answers and get scores per track."""
    questions = assessment_service.load_questions()
    result = assessment_service.compute_scores(submission.answers, questions)
    tracks = {
        track_id: TrackScore(**data)
        for track_id, data in result["tracks"].items()
    }
    return AssessmentResult(
        total_score=result["total_score"],
        max_score=result["max_score"],
        tracks=tracks,
    )
