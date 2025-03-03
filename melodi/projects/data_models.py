from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProjectResponse(BaseModel):
    id: int
    name: str
    organizationId: int
    userId: Optional[int] = None
    isDeleted: bool
    createdAt: datetime
    updatedAt: datetime