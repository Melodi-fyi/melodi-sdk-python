from typing import List

from pydantic import BaseModel, Extra


class BulkUserInternalForProjectRequest(BaseModel):
  class Config:
    extra = Extra.forbid

  projectId: int
  externalUserIds: List[int]


class UserInternalForProjectResponse(BaseModel):
  organizationId: int
  projectId: int
  externalUserId: int
  setByUserId: int
