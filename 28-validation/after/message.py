from dataclasses import dataclass, field
from enum import StrEnum, auto
from typing import Callable


class MessageType(StrEnum):
    TICKET_BOOKED = auto()
    EVENT_CREATED = auto()


@dataclass
class Message:
    type: MessageType
    message: str = ""
    data: object | None = None


MessageHandlerFn = Callable[[Message], None]


@dataclass
class MessageSystem:
    handlers: dict[str, list[MessageHandlerFn]] = field(default_factory=dict)

    def attach(self, type: MessageType, handler: MessageHandlerFn):
        if type not in self.handlers:
            self.handlers[type] = []
        self.handlers[type].append(handler)

    def detach(self, type: MessageType, handler: MessageHandlerFn):
        if type not in self.handlers:
            return
        self.handlers[type].remove(handler)

    def post(self, event: Message):
        type = event.type
        if type not in self.handlers:
            return
        for handler in self.handlers[type]:
            handler(event)
