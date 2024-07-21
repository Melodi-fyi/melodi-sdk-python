from typing import Dict, Optional, List

from pydantic import BaseModel, EmailStr

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
    email: EmailStr


class UserFeedback(BaseModel):
    sample: FeedbackSample
    feedback: Feedback
    user: User
