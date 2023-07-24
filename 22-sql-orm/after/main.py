import uvicorn
from db import EventCreate, TicketCreate
from fastapi import Depends, FastAPI, HTTPException
from models import Base, Event, Ticket
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
@app.post("/events", response_model=None)
async def create_event(
    event: EventCreate, database: Session = Depends(get_db)
) -> Event:
    db_event = Event(**event.dict())
    database.add(db_event)
    database.commit()
    database.refresh(db_event)
    return db_event

# Delete event
@app.delete("/events/{event_id}", response_model=None)
async def delete_event(event_id: int, database: Session = Depends(get_db)) -> Event:
    event = database.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    database.delete(event)
    database.commit()
    return event

# Get event by id
@app.get("/events/{event_id}", response_model=None)
async def get_event(event_id: int, database: Session = Depends(get_db)) -> Event:
    event = database.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


# Get all events
@app.get("/events", response_model=None)
async def get_all_events(database: Session = Depends(get_db)) -> list[Event]:
    events = database.query(Event).all()
    return events

# Book ticket
@app.post("/tickets", response_model=None)
async def book_ticket(
    ticket: TicketCreate, database: Session = Depends(get_db)
) -> Ticket:
    event = database.query(Event).filter(Event.id == ticket.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.available_tickets < 1:
        raise HTTPException(status_code=400, detail="No available tickets")
    
    db_ticket = Ticket(**ticket.dict())
    database.add(db_ticket)
    database.commit()
    database.refresh(db_ticket)

    event.available_tickets -= 1
    database.commit()

    return db_ticket

# Get ticket by id
@app.get("/tickets/{ticket_id}", response_model=None)
async def get_ticket(ticket_id: int, database: Session = Depends(get_db)) -> Ticket:
    ticket = database.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000) # type: ignore


if __name__ == "__main__":
    main()
