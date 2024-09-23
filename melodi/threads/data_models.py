from datetime import datetime
from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel, Extra, root_validator

from melodi.users.data_models import User, UserResponse


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

class Thread(BaseModel):
    id: Optional[int] = None
    externalId: Optional[str] = None
    projectId: Optional[int] = None
    projectName: Optional[str] = None
    messages: List[Message]
    metadata: dict[str, Union[str, int]] = {}
    externalUser: Optional[User] = None

    @root_validator
    def validate_project_fields(cls, values):
        projectId = values.get('projectId')
        projectName = values.get('projectName')
        assert projectId or projectName, "Must include projectId or projectName"
        return values

class ThreadsQueryParams(BaseModel):
  class Config:
    extra = Extra.forbid

  pageSize: int = 50
  pageIndex: int = 0
  projectId: Optional[int] = None
  userSegmentIds: Optional[List[int]] = None
  search: Optional[str] = None
  before: Optional[datetime] = None
  after: Optional[datetime] = None

class ThreadResponse(Thread):
    id: int
    externalUser: Optional[UserResponse] = None
    createdAt: datetime
    updatedAt: datetime

class ThreadsPagedResponse(BaseModel):
    count: int
    rows: List[ThreadResponse]