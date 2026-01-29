from pydantic import BaseModel
from typing import Any, Dict, Literal

EventType = Literal["FIELD_SERVICE_TICKET_CREATED", "MANUFACTURING_QUOTE_REQUESTED"]

class Customer(BaseModel):
    account_id: str
    name: str

class Event(BaseModel):
    event_type: EventType
    event_id: str
    timestamp: str
    customer: Customer
    payload: Dict[str, Any]

