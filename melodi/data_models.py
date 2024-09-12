from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import (BaseModel, EmailStr, Field, Json, ValidationError,
                      root_validator)


class Sample(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    response: str

class Samples(BaseModel):
    samples: List[Sample]

class ComparisonSample(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    response: str
    version: str

class Comparisons(BaseModel):
    samples: List[ComparisonSample]

class BinarySample(BaseModel):
    response: str
    title: Optional[str] = None

class BakeoffSample(BaseModel):
    version: str
    response: str
    message: Optional[str] = None
    title: Optional[str] = None

class Item(BaseModel):
    projectName: str
    versionName: str
    data: Dict

class ExternalUser(BaseModel):
    externalId: str
    email: Optional[EmailStr] = None
    name: Optional[str] = None

class Message(BaseModel):
    externalId: Optional[str] = None
    type: Literal['markdown', 'json'] = 'markdown'
    role: str
    content: Optional[str] = None
    jsonContent: Optional[Any] = None
    metadata: dict[str, Union[str, int]] = {}

class Thread(BaseModel):
    externalId: Optional[str] = None
    projectId: Optional[int] = None
    projectName: Optional[str] = None
    messages: List[Message]
    metadata: dict[str, Union[str, int]] = {}
    externalUser: Optional[ExternalUser] = None

    @root_validator
    def validate_gpa_and_fees(cls, values):
        projectId = values.get('projectId')
        projectName = values.get('projectName')
        assert projectId or projectName, "Must include projectId or projectName"
        return values

class ThreadResponse(Thread):
    id: int

class ThreadsPagedResponse(BaseModel):
    count: int
    rows: List[ThreadResponse]

class ThreadsQueryParams(BaseModel):
  pageSize: int = 50
  pageIndex: int = 0
  projectId: Optional[int] = None
  before: Optional[datetime] = None
  after: Optional[datetime] = None

class IssueLogAssociation(BaseModel):
    id: int
    issueId: int
    messageId: int
    userId: int

class IntentLogAssociation(BaseModel):
    id: int
    intentId: int
    messageId: int
    userId: int

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

class MessageResponse(Message):
    id: int
    issueAssociations: List[IssueMessageAssociation]
    intentAssociations: List[IntentMessageAssociation]

class LogInput(BaseModel):
    type: Literal['json', 'markdown', 'messages']

    jsonInput: Optional[Json] = Field(default=None, alias='json')
    markdown: Optional[str] = None
    messages: Optional[List[Message]] = None

class LogInputResponse(LogInput):
    id: int

class LogOutput(BaseModel):
    type: Literal['json', 'markdown', 'message']

    jsonOutput: Optional[Json] = Field(default=None, alias='json')
    markdown: Optional[str] = None
    message: Optional[Message] = None

class LogOutputResponse(LogOutput):
    id: int

class Log(BaseModel):
    projectId: int

    externalId: Optional[str] = None
    externalThreadId: Optional[str] = None

    input: Optional[LogInput] = None
    output: LogOutput

    externalUser: Optional[ExternalUser] = None

    metadata: dict[str, Union[str, int]] = {}

class LogResponse(Log):
    id: int

    input: Optional[LogInputResponse] = None
    output: Optional[LogOutputResponse] = None

    thread: Optional[ThreadResponse] = None

    issueAssociations: List[IssueLogAssociation] = []
    intentAssociations: List[IntentLogAssociation] = []

class Feedback(BaseModel):
    externalLogId: Optional[str] = None

    externalThreadId: Optional[str] = None
    externalMessageId: Optional[str] = None

    log: Optional[Log] = None

    feedbackType: Literal['POSITIVE', 'NEGATIVE']
    feedbackText: Optional[str] = None

    externalUser: Optional[ExternalUser] = None

class FeedbackResponse(Feedback):
    id: int
    feedbackType: Literal['POSITIVE', 'NEGATIVE']
    feedbackText: Optional[str] = None
    isDeleted: bool
    externalUserId: Optional[int] = None
    logId: Optional[int] = None
    createdAt: datetime
    updatedAt: datetime

class ProjectResponse(BaseModel):
    id: int
    name: str
    organizationId: int
    userId: Optional[int] = None
    isDefault: bool
    isDeleted: bool
    chainId: Optional[int] = None
    chainDisplayOrder: Optional[int] = None
    useCase: Optional[str] = None
    notes: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime