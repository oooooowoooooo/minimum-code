"""Quiz lookup service."""
from app.repositories import json_repository
from app.schemas.module import QuizQuestion


def get_module_quiz(module_id: str) -> list[QuizQuestion]:
    """Return quiz questions for a module."""
    quizzes = json_repository.read_json("quizzes.json", default={})
    return [QuizQuestion(**question) for question in quizzes.get(module_id, [])]
