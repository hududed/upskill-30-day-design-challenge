from datetime import datetime

from pydantic import BaseModel


class EventCreate(BaseModel):
    title: str
    location: str
    start_date: datetime
    end_date: datetime
    available_tickets: int


class TicketCreate(BaseModel):
    event_id: int
    customer_name: str
    customer_email: str