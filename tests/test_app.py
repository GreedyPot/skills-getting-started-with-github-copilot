import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_and_prevent_duplicate():
    # Register a new participant
    response = client.post("/activities/Chess Club/signup?email=tester@mergington.edu")
    assert response.status_code == 200
    assert "Signed up tester@mergington.edu" in response.json()["message"]
    # Try to register again (should fail)
    response = client.post("/activities/Chess Club/signup?email=tester@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_remove_participant():
    # First, add a participant
    client.post("/activities/Programming Class/signup?email=remove@mergington.edu")
    # Remove the participant
    response = client.delete("/activities/Programming Class/signup?email=remove@mergington.edu")
    assert response.status_code == 200
    assert "Removed remove@mergington.edu" in response.json()["message"]
    # Try to remove again (should fail)
    response = client.delete("/activities/Programming Class/signup?email=remove@mergington.edu")
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

def test_remove_from_nonexistent_activity():
    response = client.delete("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
