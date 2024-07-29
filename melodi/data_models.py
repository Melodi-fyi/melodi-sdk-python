from typing import Dict, List, Optional

from pydantic import BaseModel, EmailStr, Union


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
class Message(BaseModel):
    role: str
    content: str
    metadata: dict[str, Union[str, int]]

class Thread(BaseModel):
    externalId: Optional[str] = None
    projectId: int
    messages: List[Message]
    metadata: dict[str, Union[str, int]]
    externalUser: Optional[User]