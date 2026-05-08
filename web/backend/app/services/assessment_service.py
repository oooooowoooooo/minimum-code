"""Assessment scoring logic."""
from app.repositories import json_repository


def load_questions() -> list[dict]:
    """Load assessment questions from data file, or return defaults."""
    data = json_repository.read_json("rubrics.json")
    if data and "questions" in data:
        return data["questions"]
    # Default mock questions when rubrics.json doesn't exist yet
    return [
        {
            "id": "q1",
            "question": "Which Python feature allows a function to accept another function as an argument?",
            "options": [
                {"id": 0, "text": "Inheritance"},
                {"id": 1, "text": "First-class functions"},
                {"id": 2, "text": "List comprehension"},
                {"id": 3, "text": "Decorators"},
            ],
            "correct": 1,
            "track_id": "python-engineering",
            "explanation": "Python treats functions as first-class objects, enabling higher-order functions.",
        },
        {
            "id": "q2",
            "question": "What does the `async` keyword do in Python?",
            "options": [
                {"id": 0, "text": "Creates a new thread"},
                {"id": 1, "text": "Blocks until complete"},
                {"id": 2, "text": "Defines a coroutine"},
                {"id": 3, "text": "Enables parallel execution"},
            ],
            "correct": 2,
            "track_id": "python-engineering",
            "explanation": "async def defines a coroutine, which can be awaited.",
        },
        {
            "id": "q3",
            "question": "What is the primary purpose of TypeScript's `unknown` type?",
            "options": [
                {"id": 0, "text": "Same as any"},
                {"id": 1, "text": "Forces type narrowing before use"},
                {"id": 2, "text": "Represents null"},
                {"id": 3, "text": "Generic placeholder"},
            ],
            "correct": 1,
            "track_id": "typescript-mastery",
            "explanation": "unknown is type-safe: you must narrow before using the value.",
        },
        {
            "id": "q4",
            "question": "What pattern does FastAPI use for dependency injection?",
            "options": [
                {"id": 0, "text": "Constructor injection"},
                {"id": 1, "text": "Setter injection"},
                {"id": 2, "text": "Type-hint-based auto-resolution"},
                {"id": 3, "text": "XML configuration"},
            ],
            "correct": 2,
            "track_id": "api-development",
            "explanation": "FastAPI inspects function type hints to auto-resolve dependencies.",
        },
        {
            "id": "q5",
            "question": "What does RAG stand for in AI applications?",
            "options": [
                {"id": 0, "text": "Rapid Application Generation"},
                {"id": 1, "text": "Retrieval-Augmented Generation"},
                {"id": 2, "text": "Recursive Agent Group"},
                {"id": 3, "text": "Runtime Application Gateway"},
            ],
            "correct": 1,
            "track_id": "ai-integration",
            "explanation": "RAG retrieves relevant documents to augment LLM generation with context.",
        },
        {
            "id": "q6",
            "question": "What is the Observer pattern used for?",
            "options": [
                {"id": 0, "text": "Logging"},
                {"id": 1, "text": "One-to-many event notification"},
                {"id": 2, "text": "Database queries"},
                {"id": 3, "text": "Caching"},
            ],
            "correct": 1,
            "track_id": "system-design",
            "explanation": "Observer enables loose coupling through event-driven notification.",
        },
        {
            "id": "q7",
            "question": "What does Docker primarily provide?",
            "options": [
                {"id": 0, "text": "Version control"},
                {"id": 1, "text": "Containerization for consistent environments"},
                {"id": 2, "text": "Database management"},
                {"id": 3, "text": "Code compilation"},
            ],
            "correct": 1,
            "track_id": "devops",
            "explanation": "Docker containers ensure consistent behavior across development and production.",
        },
        {
            "id": "q8",
            "question": "What is a key benefit of the Repository pattern?",
            "options": [
                {"id": 0, "text": "Faster queries"},
                {"id": 1, "text": "Abstracts data access from business logic"},
                {"id": 2, "text": "Reduces memory usage"},
                {"id": 3, "text": "Generates UI components"},
            ],
            "correct": 1,
            "track_id": "system-design",
            "explanation": "Repository provides a collection-like interface, hiding storage details.",
        },
        {
            "id": "q9",
            "question": "In prompt engineering, what does chain-of-thought achieve?",
            "options": [
                {"id": 0, "text": "Shorter responses"},
                {"id": 1, "text": "Step-by-step reasoning for better accuracy"},
                {"id": 2, "text": "Faster inference"},
                {"id": 3, "text": "Lower token usage"},
            ],
            "correct": 1,
            "track_id": "ai-integration",
            "explanation": "Chain-of-thought prompting asks the model to reason step by step, improving accuracy.",
        },
    ]


def compute_scores(answers: dict[str, int], questions: list[dict]) -> dict:
    """Compute scores per track and total."""
    track_scores: dict[str, dict] = {}
    total_score = 0
    max_score = 0

    for q in questions:
        track_id = q["track_id"]
        if track_id not in track_scores:
            track_scores[track_id] = {"score": 0, "max": 0}
        track_scores[track_id]["max"] += 1
        max_score += 1

        user_answer = answers.get(q["id"])
        if user_answer is not None and user_answer == q["correct"]:
            track_scores[track_id]["score"] += 1
            total_score += 1

    # Assign levels
    track_results = {}
    for track_id, scores in track_scores.items():
        ratio = scores["score"] / scores["max"] if scores["max"] > 0 else 0
        if ratio >= 0.9:
            level = "expert"
        elif ratio >= 0.7:
            level = "advanced"
        elif ratio >= 0.4:
            level = "intermediate"
        else:
            level = "beginner"
        track_results[track_id] = {
            "score": scores["score"],
            "max": scores["max"],
            "level": level,
        }

    return {
        "total_score": total_score,
        "max_score": max_score,
        "tracks": track_results,
    }
