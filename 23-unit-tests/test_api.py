from fastapi.testclient import TestClient
from main import app, get_db
from models import Base
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
Base.metadata.create_all(bind=engine)       
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_event():
    event_data = {
        "title": "Test event",
        "location": "Test location",
        "start_date": "2023-03-15 09:00:00",
        "end_date": "2023-03-18 16:00:00",
        "available_tickets": 50,
    }
    response = client.post("/events", json=event_data)
    event = response.json()
    assert (
        "id" in event
        and event["title"] == event_data["title"]
        and event["location"] == event_data["location"]
        and event["available_tickets"] == event_data["available_tickets"]
    )