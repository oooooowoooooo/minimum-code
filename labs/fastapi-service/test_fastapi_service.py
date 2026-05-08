import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from starter import app
    return TestClient(app)


def test_create_task(client):
    """POST /tasks should create a task and return 201."""
    resp = client.post("/tasks", json={"title": "Learn FastAPI", "priority": "high"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Learn FastAPI"
    assert data["priority"] == "high"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data


def test_list_tasks(client):
    """GET /tasks should return all tasks."""
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert len(resp.json()) >= 2


def test_get_task(client):
    """GET /tasks/{id} should return a single task."""
    create = client.post("/tasks", json={"title": "Find me"})
    task_id = create.json()["id"]
    resp = client.get(f"/tasks/{task_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Find me"


def test_get_task_not_found(client):
    """GET /tasks/{id} should return 404 for nonexistent task."""
    resp = client.get("/tasks/nonexistent-id")
    assert resp.status_code == 404


def test_delete_task(client):
    """DELETE /tasks/{id} should remove task and return 204."""
    create = client.post("/tasks", json={"title": "Delete me"})
    task_id = create.json()["id"]
    resp = client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 204
    # Verify deleted
    resp = client.get(f"/tasks/{task_id}")
    assert resp.status_code == 404


def test_invalid_body(client):
    """POST /tasks with missing title should return 422."""
    resp = client.post("/tasks", json={"priority": "high"})
    assert resp.status_code == 422
