from fastapi import Depends, FastAPI, HTTPException
from models import Base, Event, Ticket
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from db import EventCreate, TicketCreate, TicketUpdate
import operations
import uvicorn

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
async def create_event(event: EventCreate, database: Session = Depends(get_db)):
    return operations.create_event(event, database)


# Delete event
@app.delete("/events/{event_id}")
async def delete_event(event_id: int, database: Session = Depends(get_db)):
    try:
        event = operations.get_event(event_id, database)
    except operations.NotFoundError as exc:
        raise HTTPException(status_code=404) from exc
    operations.delete_event(event, database)
    return event


# Get event by id
@app.get("/events/{event_id}")
async def get_event(event_id: int, database: Session = Depends(get_db)):
    try:
        event = operations.get_event(event_id, database)
    except operations.NotFoundError as exc:
        raise HTTPException(status_code=404) from exc
    return event


# Get all events
@app.get("/events")
async def get_all_events(database: Session = Depends(get_db)):
    return operations.get_all_events(database)


# Book ticket
@app.post("/tickets")
async def book_ticket(ticket: TicketCreate, database: Session = Depends(get_db)):
    try:
        return operations.book_ticket(ticket, database)
    except operations.NoAvailableTickets as exc:
        raise HTTPException(status_code=400) from exc


@app.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: int, database: Session = Depends(get_db)):
    try:
        ticket = operations.get_ticket(ticket_id, database)
    except operations.NotFoundError as exc:
        raise HTTPException(status_code=404) from exc
    return ticket


# Update ticket
@app.put("/tickets/{ticket_id}")
async def update_ticket(
    ticket_id: int, ticket_update: TicketUpdate, db: Session = Depends(get_db)
):
    try:
        return operations.update_ticket(ticket_id, ticket_update, db)
    except operations.NotFoundError as exc:
        raise HTTPException(status_code=404) from exc
    except operations.EventAlreadyStarted as exc:
        raise HTTPException(status_code=400) from exc


# Cancel ticket
@app.delete("/tickets/{ticket_id}")
async def cancel_ticket(ticket_id: int, db: Session = Depends(get_db)):
    try:
        return operations.delete_ticket(ticket_id, db)
    except operations.NotFoundError as exc:
        raise HTTPException(status_code=404) from exc
    except operations.EventAlreadyStarted as exc:
        raise HTTPException(status_code=400) from exc


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
