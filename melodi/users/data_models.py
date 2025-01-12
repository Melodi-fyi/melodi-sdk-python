from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Extra


class User(BaseModel):
    externalId: str
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    username: Optional[str] = None
    segments: Optional[dict[str, List[str]]] = {}

class UserSegmentTypeResponse(BaseModel):
    id: int
    name: str

class UserSegmentRespone(BaseModel):
    id: int
    type: UserSegmentTypeResponse
    name: str

class UserResponse(BaseModel):
    id: int
    externalId: str
    email: Optional[str] = None
    name: Optional[str] = None
    username: Optional[str] = None
    segments: List[UserSegmentRespone]


class UsersQueryParams(BaseModel):
  class Config:
    extra = Extra.forbid

  pageSize: int = 50
  pageIndex: int = 0
  projectId: Optional[int] = None
  before: Optional[datetime] = None
  after: Optional[datetime] = None
class UsersPagedResponse(BaseModel):
    count: int
    rows: List[UserResponse]
