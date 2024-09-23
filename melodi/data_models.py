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
