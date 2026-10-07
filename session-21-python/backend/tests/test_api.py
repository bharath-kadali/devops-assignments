from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    """Verify healthcheck endpoint returns status UP."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "UP"}

def test_root():
    """Verify root endpoint returns service info."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "TaskBoard API"

def test_create_task():
    """Verify task creation endpoint POST /api/tasks."""
    payload = {
        "title": "Configure EKS Cluster",
        "description": "Deploy AWS EKS with Terraform",
        "priority": "HIGH",
        "status": "TODO",
        "assignee": "DevOps Engineer"
    }
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Configure EKS Cluster"
    assert data["priority"] == "HIGH"
    assert "id" in data

def test_list_tasks():
    """Verify task listing endpoint GET /api/tasks."""
    response = client.get("/api/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) >= 1

def test_get_task_by_id():
    """Verify retrieving a specific task by ID."""
    # Create a task first
    post_res = client.post("/api/tasks", json={"title": "Monitoring Setup", "priority": "MEDIUM", "assignee": "SRE"})
    task_id = post_res.json()["id"]

    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Monitoring Setup"

def test_update_task():
    """Verify updating a task status via PUT /api/tasks/{id}."""
    post_res = client.post("/api/tasks", json={"title": "Test Update", "priority": "LOW", "assignee": "Tester"})
    task_id = post_res.json()["id"]

    put_res = client.put(f"/api/tasks/{task_id}", json={"status": "DONE"})
    assert put_res.status_code == 200
    assert put_res.json()["status"] == "DONE"

def test_task_stats():
    """Verify KPI stats endpoint GET /api/tasks/stats."""
    response = client.get("/api/tasks/stats")
    assert response.status_code == 200
    stats = response.json()
    assert "total" in stats
    assert "todo" in stats
    assert "inProgress" in stats
    assert "done" in stats
    assert stats["total"] >= 1

def test_get_nonexistent_task():
    """Verify 404 response for non-existent task ID."""
    response = client.get("/api/tasks/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_delete_task():
    """Verify deleting a task via DELETE /api/tasks/{id}."""
    post_res = client.post("/api/tasks", json={"title": "Temporary Task", "priority": "LOW", "assignee": "Tester"})
    task_id = post_res.json()["id"]

    del_res = client.delete(f"/api/tasks/{task_id}")
    assert del_res.status_code == 204

    # Confirm it is deleted
    get_res = client.get(f"/api/tasks/{task_id}")
    assert get_res.status_code == 404
