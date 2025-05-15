from datetime import datetime
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Extra

from melodi.messages.data_models import Message, MessageResponse
from melodi.users.data_models import User, UserResponse


class Thread(BaseModel):
    id: Optional[int] = None
    externalId: Optional[str] = None
    projectId: Optional[int] = None
    projectName: Optional[str] = None
    messages: List[Message]
    metadata: dict[str, Union[str, int]] = {}
    externalUser: Optional[User] = None
    createdAt: Optional[datetime] = None

class ThreadsQueryParams(BaseModel):
  class Config:
    extra = Extra.forbid

  pageSize: int = 50
  pageIndex: int = 0
  projectId: Optional[int] = None
  ids: Optional[List[int]] = None
  externalIds: Optional[List[str]] = None
  userSegmentIds: Optional[List[int]] = None
  issueIds: Optional[List[int]] = None
  intentIds: Optional[List[int]] = None
  search: Optional[str] = None
  hasFeedback: Optional[bool] = None
  feedbackType: Optional[Literal['POSITIVE', 'NEGATIVE']]= None
  attributeOptionIds: Optional[List[int]]
  includeFeedback: Optional[bool] = None
  includeIntents: Optional[bool] = None
  includeIssues: Optional[bool] = None
  before: Optional[datetime] = None
  after: Optional[datetime] = None

class SimpleProject(BaseModel):
    id: int
    name: str

class ThreadResponse(BaseModel):
    id: int
    organizationId: int
    externalId: Optional[str] = None

    project: SimpleProject

    externalUser: Optional[UserResponse] = None

    messages: List[MessageResponse]

    metadata: dict[str, Union[str, int]] = {}

    createdAt: datetime
    updatedAt: datetime

class ThreadsPagedResponse(BaseModel):
    count: int
    rows: List[ThreadResponse]
