import pytest
from fastapi.test import TestClient
from app import app

@pytest.fixture
def test_client():
    client = TestClient(app)
    return client

def test_list_tasks():
    response = test_client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_task():
    response = test_client.post("/tasks", json={"title": "Test Task", "description": "Test Description"})
    assert response.status_code == 201
    assert isinstance(response.json(), dict)

def test_read_task():
    # Create a task first
    response = test_client.post("/tasks", json={"title": "Read Task", "description": "Read Description"})
    task_id = response.json()["id"]
    response = test_client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_update_task():
    # Create a task first
    response = test_client.post("/tasks", json={"title": "Update Task", "description": "Update Description"})
    task_id = response.json()["id"]
    response = test_client.put(f"/tasks/{task_id}", json={"title": "Updated Task"})
    assert response.status_code == 200
    response = test_client.get(f"/tasks/{task_id}")
    assert response.json()["title"] == "Updated Task"

def test_delete_task():
    # Create a task first
    response = test_client.post("/tasks", json={"title": "Delete Task", "description": "Delete Description"})
    task_id = response.json()["id"]
    response = test_client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    response = test_client.get(f"/tasks/{task_id}")
    assert response.status_code == 404