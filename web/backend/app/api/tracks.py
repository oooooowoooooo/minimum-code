"""Competency tracks routes."""
from fastapi import APIRouter, HTTPException

from app.repositories import json_repository
from app.schemas.track import Track, TrackSummary, Skill

router = APIRouter(prefix="/api/tracks", tags=["tracks"])


def _load_tracks() -> list[dict]:
    """Load tracks from competency_map.json, return mock if not found."""
    data = json_repository.read_json("competency_map.json")
    if data and "tracks" in data:
        return data["tracks"]
    # Mock data until competency_map.json is created
    return [
        {
            "id": "python-engineering",
            "title": "Python Engineering",
            "description": "Core Python skills for AI application development",
            "icon": "🐍",
            "skills": [
                {"id": "py-fundamentals", "title": "Python Fundamentals", "description": "Variables, types, functions, classes", "level": "beginner"},
                {"id": "py-async", "title": "Async Programming", "description": "Coroutines, TaskGroup, event loops", "level": "intermediate"},
                {"id": "py-patterns", "title": "Design Patterns", "description": "DI, middleware, repository, pipeline", "level": "advanced"},
            ],
        },
        {
            "id": "typescript-mastery",
            "title": "TypeScript Mastery",
            "description": "Type-safe web development with TypeScript",
            "icon": "🔷",
            "skills": [
                {"id": "ts-types", "title": "Type System", "description": "Interfaces, generics, mapped types", "level": "beginner"},
                {"id": "ts-async", "title": "Async Patterns", "description": "Promises, async/await, AbortController", "level": "intermediate"},
                {"id": "ts-frameworks", "title": "Framework Internals", "description": "Next.js, tRPC, Tauri architecture", "level": "advanced"},
            ],
        },
        {
            "id": "ai-integration",
            "title": "AI Integration",
            "description": "Integrating LLMs into applications",
            "icon": "🤖",
            "skills": [
                {"id": "ai-prompt", "title": "Prompt Engineering", "description": "System prompts, chain-of-thought, few-shot", "level": "beginner"},
                {"id": "ai-rag", "title": "RAG Systems", "description": "Document parsing, vector retrieval, context injection", "level": "intermediate"},
                {"id": "ai-agents", "title": "Agent Systems", "description": "Multi-agent collaboration, tool use", "level": "advanced"},
            ],
        },
        {
            "id": "api-development",
            "title": "API Development",
            "description": "Building robust APIs and services",
            "icon": "🚀",
            "skills": [
                {"id": "api-design", "title": "API Design", "description": "REST, middleware, dependency injection", "level": "beginner"},
                {"id": "api-testing", "title": "Testing", "description": "Unit tests, integration tests, mocking", "level": "intermediate"},
                {"id": "api-optimization", "title": "Performance", "description": "Caching, async I/O, profiling", "level": "advanced"},
            ],
        },
        {
            "id": "system-design",
            "title": "System Design",
            "description": "Architectural thinking and pattern application",
            "icon": "🏛️",
            "skills": [
                {"id": "sd-patterns", "title": "Design Patterns", "description": "Builder, strategy, observer, factory", "level": "beginner"},
                {"id": "sd-architecture", "title": "Architecture", "description": "Boundaries, data flow, component design", "level": "intermediate"},
                {"id": "sd-tradeoffs", "title": "Tradeoff Analysis", "description": "Evaluating options and making decisions", "level": "advanced"},
            ],
        },
        {
            "id": "devops",
            "title": "DevOps & Deployment",
            "description": "CI/CD, containerization, and monitoring",
            "icon": "🔧",
            "skills": [
                {"id": "do-docker", "title": "Docker", "description": "Containerization, Dockerfile, compose", "level": "beginner"},
                {"id": "do-cicd", "title": "CI/CD", "description": "Automated build, test, deploy pipelines", "level": "intermediate"},
                {"id": "do-monitoring", "title": "Monitoring", "description": "Observability, logging, alerting", "level": "advanced"},
            ],
        },
    ]


@router.get("", response_model=list[TrackSummary])
def list_tracks():
    """List all competency tracks."""
    tracks = _load_tracks()
    return [
        TrackSummary(
            id=t["id"],
            title=t["title"],
            description=t.get("goal", t.get("description", "")),
            icon=t.get("icon", ""),
            skill_count=len(t.get("skills", [])),
        )
        for t in tracks
    ]


@router.get("/{track_id}", response_model=Track)
def get_track(track_id: str):
    """Get track detail with skills."""
    tracks = _load_tracks()
    track = next((t for t in tracks if t["id"] == track_id), None)
    if not track:
        raise HTTPException(status_code=404, detail=f"Track '{track_id}' not found")
    return Track(
        id=track["id"],
        title=track["title"],
        description=track.get("goal", track.get("description", "")),
        icon=track.get("icon", ""),
        skills=[Skill(
            id=s["id"],
            title=s["title"],
            description=s.get("why", s.get("description", "")),
            level=s.get("level", "beginner"),
        ) for s in track.get("skills", [])],
    )


@router.get("/{track_id}/skills/{skill_id}", response_model=Skill)
def get_skill(track_id: str, skill_id: str):
    """Get skill detail within a track."""
    tracks = _load_tracks()
    track = next((t for t in tracks if t["id"] == track_id), None)
    if not track:
        raise HTTPException(status_code=404, detail=f"Track '{track_id}' not found")
    skill = next((s for s in track.get("skills", []) if s["id"] == skill_id), None)
    if not skill:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' not found in track '{track_id}'")
    return Skill(**skill)
