import logging
from typing import List

import requests
from pydantic import parse_obj_as

from melodi.base_client import BaseClient
from melodi.exceptions import MelodiAPIError
from melodi.logging import _log_melodi_http_errors
from melodi.projects.data_models import ProjectResponse


class ProjectsClient(BaseClient):
    def __init__(self, base_url: str, api_key: str):
        self.api_key = api_key
        self.base_url = base_url

        self.base_endpoint = self.base_url + "/api/external/projects"
        self.endpoint = self.base_endpoint + f"?apiKey={self.api_key}"

        self.logger = logging.getLogger(__name__)

    def get(self) -> List[ProjectResponse]:
        try:
            response = requests.request("GET", self.endpoint)

            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()

            return parse_obj_as(List[ProjectResponse], response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def get_by_name(self, name: str) -> ProjectResponse:
        try:
            response = requests.request("GET", f"{self.endpoint}&name={name}")

            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()

            projects = parse_obj_as(List[ProjectResponse], response.json())

            if (len(projects) > 0):
                return projects[0]
            else:
                return None

        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def create(self, name: str) -> ProjectResponse:
        try:
            response = requests.post(
                self.endpoint, headers=self._get_headers(), json={"name": name}
            )

            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()
            return parse_obj_as(ProjectResponse, response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)
