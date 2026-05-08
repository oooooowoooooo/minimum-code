"""Labs routes."""
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from app.repositories import json_repository
from app.schemas.lab import Lab, LabSummary, AcceptanceCriterion

router = APIRouter(prefix="/api/labs", tags=["labs"])


def _load_labs() -> list[dict]:
    """Load labs from labs.json, return mock if not found."""
    data = json_repository.read_json("labs.json")
    if data and "labs" in data:
        return data["labs"]
    # Mock data until labs.json is created
    return [
        {
            "id": "config-loader",
            "title": "Configuration Loader",
            "description": "Build a config loader that reads YAML/JSON/env vars with type validation and defaults.",
            "track_id": "python-engineering",
            "difficulty": "beginner",
            "starter_code": "from pathlib import Path\nfrom typing import Any\n\nclass ConfigLoader:\n    def __init__(self, config_path: str):\n        pass\n\n    def load(self) -> dict[str, Any]:\n        raise NotImplementedError\n",
            "acceptance_criteria": [
                {"id": "ac-1", "description": "Loads YAML config files", "test_hint": "test_loads_yaml"},
                {"id": "ac-2", "description": "Loads JSON config files", "test_hint": "test_loads_json"},
                {"id": "ac-3", "description": "Environment variables override file values", "test_hint": "test_env_override"},
            ],
            "hints": ["Use pathlib for file detection", "Check file extension to choose parser"],
        },
        {
            "id": "llm-client",
            "title": "LLM Client",
            "description": "Build an async LLM client with retry, timeout, and streaming support.",
            "track_id": "ai-integration",
            "difficulty": "intermediate",
            "starter_code": "import httpx\nfrom typing import AsyncIterator\n\nclass LLMClient:\n    def __init__(self, api_key: str, base_url: str):\n        pass\n\n    async def complete(self, prompt: str, model: str = 'gpt-4') -> str:\n        raise NotImplementedError\n\n    async def stream(self, prompt: str, model: str = 'gpt-4') -> AsyncIterator[str]:\n        raise NotImplementedError\n",
            "acceptance_criteria": [
                {"id": "ac-1", "description": "Makes async HTTP requests to LLM API", "test_hint": "test_async_request"},
                {"id": "ac-2", "description": "Retries on transient errors with exponential backoff", "test_hint": "test_retry"},
                {"id": "ac-3", "description": "Supports streaming responses", "test_hint": "test_streaming"},
            ],
            "hints": ["Use httpx.AsyncClient for async requests", "Implement exponential backoff with jitter"],
        },
        {
            "id": "middleware-chain",
            "title": "Middleware Chain",
            "description": "Implement a middleware chain pattern that processes requests through a pipeline.",
            "track_id": "system-design",
            "difficulty": "intermediate",
            "starter_code": "from typing import Callable, Any\n\nclass Middleware:\n    async def process(self, request: dict, next_handler: Callable) -> dict:\n        raise NotImplementedError\n\nclass MiddlewareChain:\n    def __init__(self):\n        self.middlewares: list[Middleware] = []\n\n    def add(self, middleware: Middleware) -> 'MiddlewareChain':\n        pass\n\n    async def execute(self, request: dict) -> dict:\n        pass\n",
            "acceptance_criteria": [
                {"id": "ac-1", "description": "Processes request through middleware chain in order", "test_hint": "test_chain_order"},
                {"id": "ac-2", "description": "Each middleware can modify the request", "test_hint": "test_modify_request"},
                {"id": "ac-3", "description": "Middleware can short-circuit the chain", "test_hint": "test_short_circuit"},
            ],
            "hints": ["Build the chain in reverse order", "Each handler wraps the next"],
        },
        {
            "id": "rag-pipeline",
            "title": "RAG Pipeline",
            "description": "Build a retrieval-augmented generation pipeline with document chunking and vector search.",
            "track_id": "ai-integration",
            "difficulty": "advanced",
            "starter_code": "from dataclasses import dataclass\n\n@dataclass\nclass Document:\n    content: str\n    metadata: dict\n\nclass RAGPipeline:\n    def __init__(self, llm_client, embedding_model: str):\n        pass\n\n    def ingest(self, documents: list[Document]) -> None:\n        pass\n\n    def query(self, question: str, top_k: int = 3) -> str:\n        pass\n",
            "acceptance_criteria": [
                {"id": "ac-1", "description": "Chunks documents into overlapping segments", "test_hint": "test_chunking"},
                {"id": "ac-2", "description": "Embeds and stores document chunks", "test_hint": "test_embedding"},
                {"id": "ac-3", "description": "Retrieves relevant context for queries", "test_hint": "test_retrieval"},
                {"id": "ac-4", "description": "Generates answer with retrieved context", "test_hint": "test_generation"},
            ],
            "hints": ["Use cosine similarity for vector search", "Overlap chunks by 20% for context continuity"],
        },
    ]


@router.get("", response_model=list[LabSummary])
def list_labs():
    """List all labs."""
    labs = _load_labs()
    return [
        LabSummary(
            id=lab["id"],
            title=lab["title"],
            description=lab["description"],
            track_id=lab["track_id"],
            difficulty=lab.get("difficulty", "beginner"),
        )
        for lab in labs
    ]


@router.get("/{lab_id}", response_model=Lab)
def get_lab(lab_id: str):
    """Get lab detail with starter code and acceptance criteria."""
    labs = _load_labs()
    lab = next((l for l in labs if l["id"] == lab_id), None)
    if not lab:
        raise HTTPException(status_code=404, detail=f"Lab '{lab_id}' not found")
    return Lab(
        id=lab["id"],
        title=lab["title"],
        description=lab["description"],
        track_id=lab["track_id"],
        difficulty=lab.get("difficulty", "beginner"),
        starter_code=lab.get("starter_code", ""),
        acceptance_criteria=[AcceptanceCriterion(**ac) for ac in lab.get("acceptance_criteria", [])],
        hints=lab.get("hints", []),
    )


@router.get("/{lab_id}/test")
def get_lab_test(lab_id: str):
    """Get test file content for a lab."""
    labs = _load_labs()
    lab = next((l for l in labs if l["id"] == lab_id), None)
    if not lab:
        raise HTTPException(status_code=404, detail=f"Lab '{lab_id}' not found")

    # Generate test content from acceptance criteria
    test_lines = [f'"""Tests for {lab["title"]}."""', "", "import pytest", ""]
    for ac in lab.get("acceptance_criteria", []):
        test_name = ac.get("test_hint", f"test_{ac['id']}")
        test_lines.append(f"")
        test_lines.append(f"def {test_name}():")
        test_lines.append(f'    """{ac["description"]}."""')
        test_lines.append(f"    pytest.skip('Not implemented')")
        test_lines.append("")

    return PlainTextResponse("\n".join(test_lines), media_type="text/plain")
