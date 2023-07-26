from datetime import datetime
from typing import Any, Protocol

from models import Event, Ticket


class NoTicketsAvailable(Exception):
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
    name: str
    email: str

    def dict(self) -> dict[str, Any]:
        ...


class Database(Protocol):
    def add(self, instance: object, _warn: bool = True) -> None:
        ...

    def commit(self) -> None:
        ...

    def delete(self, instance: object) -> None:
        ...

    def query(self, instance: object) -> None:
        ...

    def refresh(self, instance: object) -> None:
        ...


def create_event(event: EventCreate, database: Database) -> Event:
    db_event = Event(**event.dict())
    database.add(db_event)
    database.commit()
    database.refresh(db_event)
    return db_event


def delete_event(event: Event, database: Database) -> None:
    database.delete(event)
    database.commit()


def get_event(event_id: int, database: Database) -> Event:
    event = database.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise NotFoundError(f"Event with id {event_id} not found")
    return event


def get_all_events(database: Database) -> list[Event]:
    events = database.query(Event).all()
    return events


def book_ticket(ticket: TicketCreate, database: Database) -> Ticket:
    event = database.query(Event).filter(Event.id == ticket.event_id).first()
    if not event:
        raise NotFoundError(f"Event with id {ticket.event_id} not found")
    if event.available_tickets < 1:
        raise NoTicketsAvailable(f"No tickets available for event {event.id}")

    db_ticket = Ticket(**ticket.dict())
    database.add(db_ticket)
    database.commit()
    database.refresh(db_ticket)

    event.available_tickets -= 1
    database.commit()

    return db_ticket


def get_ticket(ticket_id: int, database: Database) -> Ticket:
    ticket = database.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise NotFoundError(f"Ticket with id {ticket_id} not found")
    return ticket
