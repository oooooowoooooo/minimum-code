# Lab 3: FastAPI Service

## Objective

Build a RESTful task management API using FastAPI with Pydantic schemas, dependency injection, and proper HTTP status codes.

## Skills Practiced

- FastAPI routing and path parameters
- Pydantic request/response models
- Dependency injection with `Depends`
- HTTP status codes (201, 204, 404, 422)
- In-memory data store

## Getting Started

```bash
pip install fastapi uvicorn pytest httpx
```

1. Open `starter.py`
2. Uncomment and implement the models, store, and routes
3. Run tests: `pytest test_fastapi_service.py -v`
4. Run server: `uvicorn starter:app --reload`

## API Endpoints

| Method | Path | Status | Description |
|---|---|---|---|
| POST | `/tasks` | 201 | Create a new task |
| GET | `/tasks` | 200 | List all tasks |
| GET | `/tasks/{id}` | 200 / 404 | Get a single task |
| DELETE | `/tasks/{id}` | 204 / 404 | Delete a task |

## Task Schema

```json
{
  "title": "Learn FastAPI",
  "description": "optional",
  "priority": "medium",
  "completed": false,
  "id": "auto-generated UUID",
  "created_at": "ISO timestamp"
}
```

## Solution

See `solution.py` when you're ready to check your work.
