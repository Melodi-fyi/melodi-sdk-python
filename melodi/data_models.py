from typing import Optional
from pydantic import BaseModel


class BinarySample(BaseModel):
    response: str
    title: Optional[str] = None


class BakeoffSample(BaseModel):
    promptLabel: str
    response: str
    message: Optional[str] = None
    title: Optional[str] = None
