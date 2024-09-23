from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, Json

from melodi.threads.data_models import Message, ThreadResponse
from melodi.users.data_models import User


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

    externalUser: Optional[User] = None

    metadata: dict[str, Union[str, int]] = {}

class LogResponse(Log):
    id: int

    input: Optional[LogInputResponse] = None
    output: Optional[LogOutputResponse] = None

    thread: Optional[ThreadResponse] = None

    issueAssociations: List[IssueLogAssociation] = []
    intentAssociations: List[IntentLogAssociation] = []
