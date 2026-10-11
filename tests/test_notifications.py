import copy

import pytest

from app import app
from services.users import USERS

INVALID_PREF_ERROR = "Invalid notification_pref: must be one of: email, sms, none"


@pytest.fixture(autouse=True)
def known_users():
    snapshot = copy.deepcopy(USERS)
    USERS.clear()
    USERS.update({
        1: {"id": 1, "name": "Alice", "email": "alice@example.com", "notification_pref": "none"},
        2: {"id": 2, "name": "Bob",   "email": "bob@example.com",   "notification_pref": "none"},
    })
    yield
    USERS.clear()
    USERS.update(snapshot)

@pytest.fixture
def client():
    return app.test_client()

def test_get_notifications_default_none(client):
    response = client.get("/api/users/1/notifications")
    assert response.status_code == 200
    assert response.get_json() == {"user_id": 1, "notification_pref": "none"}

def test_get_notifications_missing_user(client):
    response = client.get("/api/users/999/notifications")
    assert response.status_code == 404
    assert response.get_json()["error"] == "User not found"

@pytest.mark.parametrize("pref", ["email", "sms", "none"])
def test_patch_notifications_valid(client, pref):
    response = client.patch("/api/users/1/notifications", json={"notification_pref": pref})
    assert response.status_code == 200
    assert response.get_json() == {"user_id": 1, "notification_pref": pref}
    assert client.get("/api/users/1/notifications").get_json()["notification_pref"] == pref

def test_patch_notifications_does_not_affect_other_users(client):
    client.patch("/api/users/1/notifications", json={"notification_pref": "sms"})
    assert client.get("/api/users/2/notifications").get_json()["notification_pref"] == "none"

@pytest.mark.parametrize("pref", ["push", "EMAIL", "", " email", None, 1, True, ["email"]])
def test_patch_notifications_invalid(client, pref):
    response = client.patch("/api/users/1/notifications", json={"notification_pref": pref})
    assert response.status_code == 422
    assert response.get_json()["error"] == INVALID_PREF_ERROR
    assert USERS[1]["notification_pref"] == "none"

def test_patch_notifications_missing_field(client):
    response = client.patch("/api/users/1/notifications", json={})
    assert response.status_code == 422
    assert response.get_json()["error"] == INVALID_PREF_ERROR

def test_patch_notifications_no_body(client):
    response = client.patch("/api/users/1/notifications")
    assert response.status_code == 422
    assert response.get_json()["error"] == INVALID_PREF_ERROR

def test_patch_notifications_missing_user(client):
    response = client.patch("/api/users/999/notifications", json={"notification_pref": "email"})
    assert response.status_code == 404
    assert response.get_json()["error"] == "User not found"

def test_user_detail_includes_notification_pref(client):
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.get_json()["notification_pref"] == "none"

def test_user_detail_reflects_updated_notification_pref(client):
    client.patch("/api/users/2/notifications", json={"notification_pref": "email"})
    assert client.get("/api/users/2").get_json()["notification_pref"] == "email"

def test_user_list_includes_notification_pref(client):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert {user["id"]: user["notification_pref"] for user in response.get_json()} == {
        1: "none",
        2: "none",
    }

def test_user_list_reflects_updated_notification_pref(client):
    client.patch("/api/users/1/notifications", json={"notification_pref": "sms"})
    response = client.get("/api/users")
    assert {user["id"]: user["notification_pref"] for user in response.get_json()} == {
        1: "sms",
        2: "none",
    }
