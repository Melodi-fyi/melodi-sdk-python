from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel

from melodi.feedback.data_models import FeedbackResponse
from melodi.intents.data_models import IntentResponse
from melodi.issues.data_models import IssueResponse


class IntentMessageAssociation(BaseModel):
    id: int
    intentId: int
    messageId: int
    userId: Optional[int] = None
    intent: IntentResponse

class IssueMessageAssociation(BaseModel):
    id: int
    issueId: int
    messageId: int
    userId: Optional[int] = None
    issue: IssueResponse

class Message(BaseModel):
    externalId: Optional[str] = None
    type: Literal['markdown', 'json'] = 'markdown'
    role: str
    content: Optional[str] = None
    jsonContent: Optional[Any] = None
    metadata: dict[str, Union[str, int]] = {}

class MessageResponse(Message):
    id: int
    issueAssociations: List[IssueMessageAssociation] = []
    intentAssociations: List[IntentMessageAssociation] = []
    externalFeedback: List[FeedbackResponse] = []
