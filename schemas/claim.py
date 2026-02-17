from pydantic import BaseModel
from datetime import datetime

class ClaimCreate(BaseModel):
    item_id: int
    claimer_id: int
    claim_description: str
    claim_location: str
    claim_time: datetime
