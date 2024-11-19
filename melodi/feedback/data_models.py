from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel

from melodi.users.data_models import User, UserResponse


class Feedback(BaseModel):
    externalThreadId: Optional[str] = None
    externalMessageId: Optional[str] = None

    feedbackType: Optional[Literal['POSITIVE', 'NEGATIVE']] = None
    feedbackText: Optional[str] = None

    externalUser: Optional[User] = None

    attributes: Optional[dict[str, str]] = {}

class Attribute(BaseModel):
    id: int
    name: str

class AttributeOption(BaseModel):
    id: int
    name: str
    attribute: Attribute

class FeedbackResponse(Feedback):
    id: int

    externalUserId: Optional[int] = None
    externalUser: Optional[UserResponse] = None

    attributes: List[AttributeOption] = []
    createdAt: datetime
    updatedAt: datetime