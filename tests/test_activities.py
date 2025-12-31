import pytest


def test_get_activities(client):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    
    # Verify structure
    assert isinstance(data, dict)
    assert "Debate Team" in data
    assert "Math Olympiad" in data
    assert "Basketball" in data
    
    # Verify activity structure
    activity = data["Debate Team"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_activity_has_initial_participants(client):
    """Test that activities have initial participants"""
    response = client.get("/activities")
    data = response.json()
    
    # Debate Team should have alex@mergington.edu
    assert "alex@mergington.edu" in data["Debate Team"]["participants"]
    assert "james@mergington.edu" in data["Math Olympiad"]["participants"]
    assert "marcus@mergington.edu" in data["Basketball"]["participants"]


def test_signup_for_activity(client):
    """Test signing up for an activity"""
    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    
    # Verify the participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate_participant(client):
    """Test that signing up twice fails"""
    email = "duplicate@mergington.edu"
    
    # First signup should succeed
    response1 = client.post(
        f"/activities/Digital Art/signup?email={email}"
    )
    assert response1.status_code == 200
    
    # Second signup should fail
    response2 = client.post(
        f"/activities/Digital Art/signup?email={email}"
    )
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]


def test_signup_nonexistent_activity(client):
    """Test signing up for a non-existent activity"""
    response = client.post(
        "/activities/Nonexistent Activity/signup?email=test@mergington.edu"
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_unregister_from_activity(client):
    """Test unregistering from an activity"""
    email = "unregister_test@mergington.edu"
    
    # First, sign up
    signup_response = client.post(
        f"/activities/Programming Class/signup?email={email}"
    )
    assert signup_response.status_code == 200
    
    # Then unregister
    unregister_response = client.delete(
        f"/activities/Programming Class/unregister?email={email}"
    )
    assert unregister_response.status_code == 200
    assert "Unregistered" in unregister_response.json()["message"]
    
    # Verify the participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities["Programming Class"]["participants"]


def test_unregister_nonexistent_participant(client):
    """Test unregistering a participant who doesn't exist"""
    response = client.delete(
        "/activities/Volleyball/unregister?email=doesnotexist@mergington.edu"
    )
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_nonexistent_activity(client):
    """Test unregistering from a non-existent activity"""
    response = client.delete(
        "/activities/Nonexistent Activity/unregister?email=test@mergington.edu"
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
