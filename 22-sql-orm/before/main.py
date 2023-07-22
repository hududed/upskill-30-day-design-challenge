import sqlite3

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime


app = FastAPI()


# Information needed to create an event
class EventCreate(BaseModel):
    title: str
    location: str
    start_date: str
    end_date: str
    available_tickets: int


# Information needed to create a ticket
class TicketCreate(BaseModel):
    event_id: int
    customer_name: str
    customer_email: str


# Initialize database connection
def get_db() -> sqlite3.Connection:
    connection = sqlite3.connect("events.db")
    connection.row_factory = sqlite3.Row
    return connection


# Initialize database table
def init_db():
    connection = get_db()
    with open("schema.sql") as f:
        connection.executescript(f.read())


# Create event
@app.post("/events")
async def create_event(event: EventCreate):
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO events (title, location, start_date, end_date, available_tickets)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            event.title,
            event.location,
            datetime.strptime(event.start_date, "%Y-%m-%d %H:%M:%S"),
            datetime.strptime(event.end_date, "%Y-%m-%d %H:%M:%S"),
            event.available_tickets,
        ),
    )
    connection.commit()
    return {"event_id": cursor.lastrowid}


@app.delete("/events/{event_id}")
def delete_event(event_id: int):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE id=?", (event_id,))
    event = cursor.fetchone()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    cursor.execute("DELETE FROM events WHERE id=?", (event_id,))
    connection.commit()
    connection.close()
    return dict(event)


# Get event by id
@app.get("/events/{event_id}")
async def get_event(event_id: int):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    event = cursor.fetchone()
    if event is None:
        raise HTTPException(
            status_code=404, detail=f"Event with id {event_id} not found."
        )
    return dict(event)


# Get all events
@app.get("/events")
async def get_all_events():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    return [dict(event) for event in events]


# Book ticket
@app.post("/tickets")
async def book_ticket(ticket: TicketCreate):
    connection = get_db()
    cursor = connection.cursor()

    # Get the event
    cursor.execute("SELECT * FROM events WHERE id = ?", (ticket.event_id,))
    event = cursor.fetchone()
    if event is None:
        raise HTTPException(
            status_code=404, detail=f"Event with id {ticket.event_id} not found"
        )

    # Check ticket availability
    if event["available_tickets"] < 1:
        raise HTTPException(status_code=400, detail="No available tickets.")

    # Create the ticket
    cursor.execute(
        """
        INSERT INTO tickets (event_id, customer_name, customer_email)
        VALUES (?, ?, ?)
        """,
        (ticket.event_id, ticket.customer_name, ticket.customer_email),
    )

    # Update the event ticket availability
    cursor.execute(
        """
        UPDATE events SET available_tickets = available_tickets - 1
        WHERE id = ?
        """,
        (ticket.event_id,),
    )

    connection.commit()
    return {"ticket_id": cursor.lastrowid}


# Get event by id
@app.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: int):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    ticket = cursor.fetchone()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return dict(ticket)


def main():
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
