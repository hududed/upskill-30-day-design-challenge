from fastapi.testclient import TestClient
from main import app, get_db
from models import Base
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
Base.metadata.create_all(bind=engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_event_not_exists():
    response = client.get(f"/events/{0}")
    assert response.status_code == 404, response.text

def test_delete_event_not_exists():
    response = client.delete(f"/events/{0}")
    assert response.status_code == 404, response.text

def test_no_available_tickets():
    event_data = {
        "title": "Test event",
        "location": "Test location",
        "start_date": "2023-09-22 12:00:00",
        "end_date": "2023-09-22 14:00:00",
        "available_tickets": 0,
    }
    response = client.post("/events", json=event_data)
    assert response.status_code == 200, response.text

    ticket_data = {
        "event_id": 1,
        "customer_name": "James Johns",
        "customer_email": "test@example.com",
    }

    response = client.post("/tickets", json=ticket_data)
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "No available tickets"

def test_event_exists():
    event_data = {
        "title": "Test event",
        "location": "Test location",
        "start_date": "2023-09-22 12:00:00",
        "end_date": "2023-09-22 14:00:00",
        "available_tickets": 100,
    }
    response = client.post("/events", json=event_data)
    assert response.status_code == 200, response.text
    event_id = response.json()["id"]

    response = client.get(f"/events/{event_id}")
    assert response.status_code == 200, response.text
    event = response.json()
    assert (
        "id" in event
        and event["title"] == event_data["title"]
        and event["location"] == event_data["location"]
        and event["available_tickets"] == event_data["available_tickets"]
    )

def test_invalid_event_id():
    response = client.get(f"/events/invalid_id")
    assert response.status_code == 422, response.text


def test_invalid_ticket_data():
    event_data = {
        "title": "Test event",
        "location": "Test location",
        "start_date": "2023-09-22 12:00:00",
        "end_date": "2023-09-22 14:00:00",
        "available_tickets": 1,
    }
    response = client.post("/events", json=event_data)
    assert response.status_code == 200, response.text
    event_id = response.json()["id"]

    ticket_data = {
        "event_id": event_id,
        "customer_name": "",
        "customer_email": "invalid_email",
    }

    response = client.post("/tickets", json=ticket_data)
    assert response.status_code == 200, response.text

def test_create_event() -> None:
    event_data = {
        "title": "Test event",
        "location": "Test location",
        "start_date": "2023-09-22 12:00:00",
        "end_date": "2023-09-22 14:00:00",
        "available_tickets": 100,
    }
    response = client.post("/events", json=event_data)
    event = response.json()
    assert (
        "id" in event
        and event["title"] == event_data["title"]
        and event["location"] == event_data["location"]
        and event["available_tickets"] == event_data["available_tickets"]
    )
