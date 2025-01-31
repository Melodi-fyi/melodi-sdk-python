from datetime import datetime

from pydantic import BaseModel


class IntentResponse(BaseModel):
    id: int
    name: str
    createdAt: datetime
