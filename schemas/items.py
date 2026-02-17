from pydantic import BaseModel
from datetime import datetime

class ItemCreate(BaseModel):
    title: str
    short_description: str
    detailed_description: str
    category: str
    status: str
    location: str
    event_time: datetime
    reporter_id: int
