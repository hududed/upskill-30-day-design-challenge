from datetime import datetime
from typing import Any, Protocol
from message import Message, MessageType, MessageSystem

from models import Event, Ticket


class NoAvailableTickets(Exception):
    pass


class NotFoundError(Exception):
    pass


class EventCreate(Protocol):
    title: str
    location: str
    start_date: datetime
    end_date: datetime
    available_tickets: int

    def dict(self) -> dict[str, Any]:
        ...


class TicketCreate(Protocol):
    event_id: int
    customer_name: str
    customer_email: str

    def dict(self) -> dict[str, Any]:
        ...


class TicketUpdate(Protocol):
    customer_name: str | None = None

    def dict(self) -> dict[str, Any]:
        ...


class Database(Protocol):
    def add(self, instance: object, _warn: bool = True) -> None:
        ...

    def commit(self) -> None:
        ...

    def delete(self, instance: object) -> None:
        ...

    def query(self, instance: object) -> Any:
        ...

    def refresh(self, instance: object) -> None:
        ...


def create_event(
    event: EventCreate, database: Database, message_system: MessageSystem
) -> Event:
    db_event = Event(**event.dict())
    database.add(db_event)
    database.commit()
    database.refresh(db_event)
    message_system.post(
        Message(
            type=MessageType.EVENT_CREATED,
            message="Event created",
            data=db_event,
        )
    )
    return db_event


def delete_event(event_id: int, database: Database) -> Event:
    # Delete the event
    event = get_event(event_id, database)
    database.delete(event)

    # Delete all tickets that are bought for this event
    tickets = database.query(Ticket).filter(Ticket.event_id == event_id)
    for ticket in tickets:
        database.delete(ticket)

    database.commit()
    return event


def get_event(event_id: int, database: Database) -> Event:
    event = database.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise NotFoundError(f"Event with id {event_id} not found.")
    return event


def get_all_events(database: Database) -> list[Event]:
    events = database.query(Event).all()
    return events


def book_ticket(
    ticket: TicketCreate,
    database: Database,
    message_system: MessageSystem,
) -> Ticket:
    event = get_event(ticket.event_id, database)
    if event.available_tickets < 1:
        raise NoAvailableTickets()

    db_ticket = Ticket(**ticket.dict())
    database.add(db_ticket)
    database.commit()
    database.refresh(db_ticket)

    event.available_tickets -= 1
    database.commit()
    message_system.post(
        Message(
            type=MessageType.TICKET_BOOKED,
            message="Ticket booked",
            data=db_ticket,
        )
    )
    return db_ticket


def update_ticket(
    ticket_id: int, ticket_update: TicketUpdate, database: Database
) -> Ticket:
    ticket = get_ticket(ticket_id, database)

    if ticket_update.customer_name:
        ticket.customer_name = ticket_update.customer_name
        database.commit()

    return ticket


def delete_ticket(ticket_id: int, database: Database) -> Ticket:
    ticket = get_ticket(ticket_id, database)
    event = get_event(ticket.event_id, database)

    database.delete(ticket)
    event.available_tickets += 1

    database.commit()
    return ticket


def get_ticket(ticket_id: int, database: Database) -> Ticket:
    ticket = database.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise NotFoundError(f"Ticket with id {ticket_id} not found.")
    return ticket
