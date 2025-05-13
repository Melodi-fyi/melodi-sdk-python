from datetime import datetime

from pydantic import BaseModel


class IssueResponse(BaseModel):
    id: int
    name: str
    createdAt: datetime


class IssueUpsertRequest(BaseModel):
    projectId: int
    name: str