from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProjectResponse(BaseModel):
    id: int
    name: str
    organizationId: int
    userId: Optional[int] = None
    isDefault: bool
    isDeleted: bool
    createdAt: datetime
    updatedAt: datetime