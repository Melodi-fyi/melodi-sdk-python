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
    chainId: Optional[int] = None
    chainDisplayOrder: Optional[int] = None
    useCase: Optional[str] = None
    notes: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime