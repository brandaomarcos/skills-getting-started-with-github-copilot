from fastapi.testclient import TestClient
from app import app, activities_collection

client = TestClient(app)

def test_get_activities():
    # Arrange: Ensure the database is prepopulated with activities
    activities_collection.delete_many({})  # Clear the collection
    activities_collection.insert_many([
        {
            "name": "Test Club",
            "description": "A test activity",
            "schedule": "Mondays, 3:00 PM - 4:00 PM",
            "max_participants": 10,
            "participants": ["test1@mergington.edu", "test2@mergington.edu"]
        },
        {
            "name": "Sample Club",
            "description": "Another test activity",
            "schedule": "Fridays, 4:00 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["sample1@mergington.edu"]
        }
    ])

    # Act: Make a GET request to the /activities endpoint
    response = client.get("/activities")

    # Assert: Verify the response
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == 2
    assert activities[0]["name"] == "Test Club"
    assert activities[0]["description"] == "A test activity"
    assert activities[0]["schedule"] == "Mondays, 3:00 PM - 4:00 PM"
    assert activities[0]["max_participants"] == 10
    assert activities[0]["participants"] == ["test1@mergington.edu", "test2@mergington.edu"]
    assert activities[1]["name"] == "Sample Club"
    assert activities[1]["description"] == "Another test activity"
    assert activities[1]["schedule"] == "Fridays, 4:00 PM - 5:00 PM"
    assert activities[1]["max_participants"] == 15
    assert activities[1]["participants"] == ["sample1@mergington.edu"]