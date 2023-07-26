import operations
import uvicorn
from db import EventCreate, TicketCreate
from fastapi import Depends, FastAPI, HTTPException
from models import Base, Event
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./events.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


app = FastAPI()


# Initialize database session
def get_db():
    database = SessionLocal()
    yield database
    database.close()


# Create event
@app.post("/events")
async def create_event(
    event: EventCreate, database: Session = Depends(get_db)
) -> Event:
    return operations.create_event(event, database)


# Delete event
@app.delete("/events/{event_id}")
async def delete_event(event_id: int, database: Session = Depends(get_db)):
    try:
        event = operations.get_event(event_id, database)
    except operations.NotFoundError:
        raise HTTPException(status_code=404, detail="Event not found")
    operations.delete_event(event, database)
    return event


# Get event by id
@app.get("/events/{event_id}")
async def get_event(event_id: int, database: Session = Depends(get_db)):
    try:
        event = operations.get_event(event_id, database)
    except operations.NotFoundError:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


# Get all events
@app.get("/events")
async def get_all_events(database: Session = Depends(get_db)):
    return operations.get_all_events(database)


# Book ticket
@app.post("/tickets")
async def book_ticket(ticket: TicketCreate, database: Session = Depends(get_db)):
    try:
        event = operations.book_ticket(ticket, database)
    except operations.NotFoundError:
        raise HTTPException(status_code=404, detail="Event not found")
    except operations.NoTicketsAvailable:
        raise HTTPException(status_code=400, detail="No available tickets")
    return event


@app.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: int, database: Session = Depends(get_db)):
    try:
        ticket = operations.get_ticket(ticket_id, database)
    except operations.NotFoundError:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
