from typing import List

from pydantic import BaseModel, Extra


class BulkUserInternalForProjectRequest(BaseModel):
  class Config:
    extra = Extra.forbid

  projectId: int
  externalUserIds: List[int]


class BulkUserInternalForProjectResponse(BaseModel):
  count: int
