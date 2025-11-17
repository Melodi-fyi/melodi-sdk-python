import logging
from typing import List

import requests
from pydantic import parse_obj_as

from melodi.base_client import BaseClient
from melodi.exceptions import MelodiAPIError
from melodi.logging import _log_melodi_http_errors
from melodi.projects.data_models import ProjectResponse


def _empty_project_response() -> ProjectResponse:
    return ProjectResponse(
        id=0,
        name="SAMPLE",
        organizationId=0,
        userId=None,
        isDeleted=False,
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

class ProjectsClient(BaseClient):
    def __init__(self, base_url: str, api_key: str):
        self.api_key = api_key
        self.base_url = base_url

        self.base_endpoint = self.base_url + "/api/external/projects"
        self.endpoint = self.base_endpoint + f"?apiKey={self.api_key}"

        self.logger = logging.getLogger(__name__)

    def get(self) -> List[ProjectResponse]:
        return []

    def get_by_name(self, name: str) -> ProjectResponse:
        return _empty_project_response()

    def create(self, name: str) -> ProjectResponse:
        return _empty_project_response()