from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, EmailStr, Field, Json


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

class FeedbackSample(BaseModel):
    project: str
    projectVersion: str
    input: str
    output: str
    metadata: Dict

class Feedback(BaseModel):
    feedbackType: str
    feedbackText: str

class User(BaseModel):
    id: str
    email: Optional[EmailStr] = None

class UserFeedback(BaseModel):
    sample: FeedbackSample
    feedback: Feedback
    user: User

class ExternalUser(BaseModel):
    externalId: str
    email: Optional[EmailStr] = None
    name: Optional[str] = None

class Message(BaseModel):
    externalId: Optional[str] = None
    role: str
    content: str
    metadata: dict[str, Union[str, int]] = {}

class Thread(BaseModel):
    externalId: Optional[str] = None
    projectId: int
    messages: List[Message]
    metadata: dict[str, Union[str, int]] = {}
    externalUser: Optional[ExternalUser] = None

class ThreadResponse(Thread):
    id: int

class IssueLogAssociation(BaseModel):
    id: int
    issueId: int
    logId: int
    userId: int

class IntentLogAssociation(BaseModel):
    id: int
    intentId: int
    logId: int
    userId: int

class LogInput(BaseModel):
    type: Literal['json', 'markdown', 'messages']

    jsonInput: Optional[Json] = Field(default=None, alias='json')
    markdown: Optional[str] = None
    messages: List[Message] = []

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

    input: Optional[LogInput]
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
