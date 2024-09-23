from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel


class IssueMessageAssociation(BaseModel):
    id: int
    issueId: int
    messageId: int
    userId: int

class IntentMessageAssociation(BaseModel):
    id: int
    intentId: int
    messageId: int
    userId: int

class Message(BaseModel):
    externalId: Optional[str] = None
    type: Literal['markdown', 'json'] = 'markdown'
    role: str
    content: Optional[str] = None
    jsonContent: Optional[Any] = None
    metadata: dict[str, Union[str, int]] = {}

class MessageResponse(Message):
    id: int
    issueAssociations: List[IssueMessageAssociation]
    intentAssociations: List[IntentMessageAssociation]