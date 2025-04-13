import datetime
from pydantic import BaseModel


class EventSchema(BaseModel):
    user_id: str
    event_type: str
    timestamp: str
    payload: dict
