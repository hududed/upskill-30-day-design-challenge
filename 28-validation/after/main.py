from message import Message, MessageType, MessageSystem

from fastapi import Depends, FastAPI, HTTPException
from models import Base, Event, Ticket
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from db import TicketCreate, TicketUpdate, EventCreate
import operations
import uvicorn

SQLALCHEMY_DATABASE_URL = "sqlite:///./events.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Message handlers


def handle_message_ticket_bought_email(message: Message):
    ticket: Ticket = message.data  # type: ignore
    customer_name = ticket.customer_name
    email = ticket.customer_email
    print(f"Ticket bought for event {ticket.event_id} by {customer_name} ({email}).")
    # self.email_service.send_email(email, message)
    print(message)


def handle_message_ticket_bought_sms(message: Message):
    ticket: Ticket = message.data  # type: ignore
    print(f"Your ticket has been reserved under id {ticket.id}!")
    # self.email_service.send_email(email, message)
    print(message)


def handle_message_event_created_email(message: Message):
    event: Event = message.data  # type: ignore
    print(f"Event {event.title} created!")
    # self.email_service.send_email(email, message)
    print(message)


# Initialize database session
def get_db():
    database = SessionLocal()
    yield database
    database.close()


def get_message_system() -> MessageSystem:
    message_system = MessageSystem()
    message_system.attach(MessageType.TICKET_BOOKED, handle_message_ticket_bought_email)
    message_system.attach(MessageType.TICKET_BOOKED, handle_message_ticket_bought_sms)
    message_system.attach(MessageType.EVENT_CREATED, handle_message_event_created_email)
    return message_system


# Create event
@app.post("/events")
async def create_event(
    event: EventCreate,
    database: Session = Depends(get_db),
    message_system: MessageSystem = Depends(get_message_system),
):
    return operations.create_event(event, database, message_system)


# Delete event
@app.delete("/events/{event_id}")
async def delete_event(event_id: int, database: Session = Depends(get_db)):
    try:
        return operations.delete_event(event_id, database)
    except operations.NotFoundError as exc:
        raise HTTPException(status_code=404) from exc


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
async def book_ticket(
    ticket: TicketCreate,
    database: Session = Depends(get_db),
    message_system: MessageSystem = Depends(get_message_system),
):
    try:
        return operations.book_ticket(ticket, database, message_system)
    except operations.NoAvailableTickets as exc:
        raise HTTPException(status_code=400) from exc


@app.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: int, database: Session = Depends(get_db)):
    try:
        return operations.get_ticket(ticket_id, database)
    except operations.NotFoundError as exc:
        raise HTTPException(status_code=404) from exc


# Update ticket
@app.put("/tickets/{ticket_id}")
async def update_ticket(
    ticket_id: int, ticket_update: TicketUpdate, db: Session = Depends(get_db)
):
    try:
        return operations.update_ticket(ticket_id, ticket_update, db)
    except operations.NotFoundError as exc:
        raise HTTPException(status_code=404) from exc


# Delete ticket
@app.delete("/tickets/{ticket_id}")
async def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    try:
        return operations.delete_ticket(ticket_id, db)
    except operations.NotFoundError as exc:
        raise HTTPException(status_code=404) from exc


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
