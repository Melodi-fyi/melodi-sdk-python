from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Extra


class UserSegmentTypesQueryParams(BaseModel):
  class Config:
    extra = Extra.forbid

  projectId: Optional[int] = None

class UserSegmentDefinition(BaseModel):
    id: int
    name: str

    organizationId: int
    projectId: Optional[int] = None
    userSegmentTypeId: int

    createdAt: datetime
    updatedAt: datetime

class UserSegmentTypeDefinition(BaseModel):
    id: int
    name: str

    organizationId: int
    projectId: Optional[int] = None

    segments: List[UserSegmentDefinition]

    createdAt: datetime
    updatedAt: datetime
