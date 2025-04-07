"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from mongomock import MongoClient

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# Initialize a mock MongoDB client
mock_client = MongoClient()
db = mock_client['mergington_high_school']

# Prepopulate the database with the existing hardcoded activities
activities_collection = db['activities']
activities_collection.insert_many([
    {
        "name": "Chess Club",
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    {
        "name": "Programming Class",
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    {
        "name": "Gym Class",
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    {
        "name": "Soccer Team",
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    {
        "name": "Basketball Team",
        "description": "Practice basketball skills and participate in tournaments",
        "schedule": "Wednesdays and Fridays, 3:00 PM - 4:30 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    {
        "name": "Art Club",
        "description": "Explore various art techniques and create your own masterpieces",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    {
        "name": "Drama Club",
        "description": "Learn acting skills and participate in school plays",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    {
        "name": "Math Club",
        "description": "Solve challenging math problems and prepare for competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    {
        "name": "Science Club",
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Fridays, 3:00 PM - 4:30 PM",
        "max_participants": 12,
        "participants": ["elijah@mergington.edu", "lucas@mergington.edu"]
    }
])


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    activities = [
        {
            "name": activity.get("name"),
            "description": activity.get("description"),
            "schedule": activity.get("schedule"),
            "max_participants": activity.get("max_participants"),
            "participants": activity.get("participants"),
        }
        for activity in activities_collection.find({}, {"_id": 0})
    ]
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Query the database for the specific activity
    activity = activities_collection.find_one({"name": activity_name}, {"_id": 0})

    # Validate activity exists
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # check to ensure that the activity has not already reached max_participants
    if len(activity.get("participants", [])) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")
    
    # Validate student is not already signed up
    if email in activity.get("participants", []):
        raise HTTPException(status_code=400, detail="Student already signed up")


    # Add the student to the participants list
    activities_collection.update_one(
        {"name": activity_name},
        {"$addToSet": {"participants": email}}
    )

    return {"message": f"Student {email} signed up for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    # Query the database for the specific activity
    activity = activities_collection.find_one({"name": activity_name}, {"_id": 0})

    # Validate activity exists
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate student is signed up
    if email not in activity.get("participants", []):
        raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

    # Remove student from participants
    activities_collection.update_one(
        {"name": activity_name},
        {"$pull": {"participants": email}}
    )
    return {"message": f"Unregistered {email} from {activity_name}"}
