from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel

from melodi.users.data_models import User


class Feedback(BaseModel):
    externalLogId: Optional[str] = None

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
    feedbackType: Optional[Literal['POSITIVE', 'NEGATIVE']] = None
    feedbackText: Optional[str] = None
    externalUserId: Optional[int] = None
    logId: Optional[int] = None
    createdAt: datetime
    updatedAt: datetime