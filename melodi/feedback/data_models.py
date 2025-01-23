from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel

from melodi.users.data_models import User, UserResponse


class BaseFeedback(BaseModel):
    feedbackType: Optional[Literal['POSITIVE', 'NEGATIVE']] = None
    feedbackText: Optional[str] = None

class Feedback(BaseFeedback):
    externalThreadId: Optional[str] = None
    externalMessageId: Optional[str] = None

    externalUser: Optional[User] = None

    attributes: Optional[dict[str, str]] = {}

class Attribute(BaseModel):
    id: int
    name: str

class AttributeOption(BaseModel):
    id: int
    name: str
    attribute: Attribute

class FeedbackResponse(BaseFeedback):
    id: int

    externalUserId: Optional[int] = None
    externalUser: Optional[UserResponse] = None

    attributeOptions: List[AttributeOption] = []
    createdAt: datetime
    updatedAt: datetime

class FeedbackCreateOrUpdateRequest(Feedback):
    id: Optional[int] = None