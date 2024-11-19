from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, Extra

from melodi.messages.data_models import Message, MessageWithFeedback
from melodi.users.data_models import User, UserResponse


class Thread(BaseModel):
    id: Optional[int] = None
    externalId: Optional[str] = None
    projectId: Optional[int] = None
    projectName: Optional[str] = None
    messages: List[Message]
    metadata: dict[str, Union[str, int]] = {}
    externalUser: Optional[User] = None

class ThreadsQueryParams(BaseModel):
  class Config:
    extra = Extra.forbid

  pageSize: int = 50
  pageIndex: int = 0
  projectId: Optional[int] = None
  userSegmentIds: Optional[List[int]] = None
  search: Optional[str] = None
  hasFeedback: Optional[bool] = None
  includeFeedback: Optional[bool] = None
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

class ThreadResponseWithFeedback(ThreadResponse):
    messages: List[MessageWithFeedback]

class ThreadsWithFeedbackPagedResponse(BaseModel):
    count: int
    rows: List[ThreadResponseWithFeedback]
