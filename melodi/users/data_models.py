from typing import List, Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    externalId: str
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    username: Optional[str] = None
    segments: Optional[dict[str, str]] = {}

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
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    username: Optional[str] = None
    segments: List[UserSegmentRespone]