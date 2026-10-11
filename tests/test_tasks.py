import copy

import pytest

from app import app
from services.tasks import (
    TASKS,
    create_task,
    get_task,
    get_tasks,
    get_tasks_by_user,
    parse_priority,
    process_order,
    update_task_priority,
)
from utils.errors import NotFoundError, ValidationError


@pytest.fixture
def restore_tasks():
    snapshot = copy.deepcopy(TASKS)
    yield
    TASKS.clear()
    TASKS.update(snapshot)

@pytest.fixture
def client():
    return app.test_client()

@pytest.fixture
def known_tasks(restore_tasks):
    TASKS.clear()
    TASKS.update({
        1: {"id": 1, "title": "Low",         "done": False, "user_id": 1, "priority": 1},
        2: {"id": 2, "title": "Normal",      "done": False, "user_id": 1, "priority": 3},
        3: {"id": 3, "title": "Also normal", "done": True,  "user_id": 2, "priority": 3},
    })

def test_process_order_valid(restore_tasks):
    result = process_order(1)
    assert result["done"] is True

def test_process_order_invalid():
    with pytest.raises(KeyError):
        process_order(999)

def test_get_task_valid():
    result = get_task(2)
    assert result["title"] == "Write report"

def test_get_task_invalid():
    with pytest.raises(NotFoundError):
        get_task(999)

def test_get_tasks_by_user_valid():
    result = get_tasks_by_user(1)
    assert {task["id"] for task in result} == {1, 2}

def test_get_tasks_by_user_no_tasks():
    result = get_tasks_by_user(999)
    assert result == []

def test_get_task_existing_has_default_priority():
    assert get_task(2)["priority"] == 3

def test_create_task_default_priority(restore_tasks):
    result = create_task("New task", 3)
    assert result["priority"] == 3

def test_create_task_custom_priority(restore_tasks):
    result = create_task("Urgent task", 3, priority=5)
    assert result["priority"] == 5

@pytest.mark.parametrize("priority", [0, 6, -1, "3", 2.5, True, None])
def test_create_task_invalid_priority(priority):
    with pytest.raises(ValidationError):
        create_task("Bad task", 3, priority=priority)

def test_update_task_priority_valid(restore_tasks):
    result = update_task_priority(3, 1)
    assert result["priority"] == 1
    assert get_task(3)["priority"] == 1

@pytest.mark.parametrize("priority", [0, 6, -1, "3", 2.5, True, None])
def test_update_task_priority_invalid(restore_tasks, priority):
    with pytest.raises(ValidationError):
        update_task_priority(3, priority)
    assert get_task(3)["priority"] == 3

def test_update_task_priority_missing_task(restore_tasks):
    with pytest.raises(NotFoundError):
        update_task_priority(999, 2)

def test_patch_task_priority_success(client, restore_tasks):
    response = client.patch("/api/tasks/3", json={"priority": 5})
    assert response.status_code == 200
    assert response.get_json()["priority"] == 5

def test_patch_task_priority_invalid(client, restore_tasks):
    response = client.patch("/api/tasks/3", json={"priority": 9})
    assert response.status_code == 422
    assert response.get_json()["error"] == "Invalid priority: must be an integer between 1 and 5"

def test_patch_task_priority_missing_task(client, restore_tasks):
    response = client.patch("/api/tasks/999", json={"priority": 2})
    assert response.status_code == 404
    assert response.get_json()["error"] == "Task not found"

def test_patch_task_priority_missing_field(client, restore_tasks):
    response = client.patch("/api/tasks/3", json={})
    assert response.status_code == 422

def test_get_tasks_no_priority_returns_all(known_tasks):
    assert [task["id"] for task in get_tasks()] == [1, 2, 3]

def test_get_tasks_filters_by_priority(known_tasks):
    assert [task["id"] for task in get_tasks(1)] == [1]
    assert [task["id"] for task in get_tasks(3)] == [2, 3]

def test_get_tasks_no_matches(known_tasks):
    assert get_tasks(4) == []

@pytest.mark.parametrize("priority", [0, 6, True])
def test_get_tasks_invalid_priority(known_tasks, priority):
    with pytest.raises(ValidationError):
        get_tasks(priority)

@pytest.mark.parametrize("value", ["1", "2", "3", "4", "5"])
def test_parse_priority_valid(value):
    assert parse_priority(value) == int(value)

@pytest.mark.parametrize("value", ["+3", " 3 ", "03", "abc", "", "2.5", "0", "6"])
def test_parse_priority_invalid(value):
    with pytest.raises(ValidationError):
        parse_priority(value)

def test_list_tasks_no_priority(client, known_tasks):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert [task["id"] for task in response.get_json()] == [1, 2, 3]

def test_list_tasks_filtered_by_priority(client, known_tasks):
    response = client.get("/api/tasks?priority=3")
    assert response.status_code == 200
    assert [task["id"] for task in response.get_json()] == [2, 3]

def test_list_tasks_priority_no_matches(client, known_tasks):
    response = client.get("/api/tasks?priority=4")
    assert response.status_code == 200
    assert response.get_json() == []

@pytest.mark.parametrize("value", ["6", "abc", "", "%2B3", "%203%20", "03"])
def test_list_tasks_invalid_priority(client, known_tasks, value):
    response = client.get(f"/api/tasks?priority={value}")
    assert response.status_code == 422
    assert response.get_json()["error"] == "Invalid priority: must be an integer between 1 and 5"

def test_get_task_route_includes_priority(client):
    response = client.get("/api/tasks/2")
    assert response.status_code == 200
    assert response.get_json()["priority"] == 3

def test_post_task_default_priority(client, restore_tasks):
    response = client.post("/api/tasks", json={"title": "New", "user_id": 3})
    assert response.status_code == 201
    assert response.get_json()["priority"] == 3

def test_post_task_custom_priority(client, restore_tasks):
    response = client.post("/api/tasks", json={"title": "New", "user_id": 3, "priority": 1})
    assert response.status_code == 201
    assert response.get_json()["priority"] == 1

@pytest.mark.parametrize("priority", [0, 6, "3", True, None])
def test_post_task_invalid_priority(client, restore_tasks, priority):
    response = client.post("/api/tasks", json={"title": "New", "user_id": 3, "priority": priority})
    assert response.status_code == 422
    assert response.get_json()["error"] == "Invalid priority: must be an integer between 1 and 5"
