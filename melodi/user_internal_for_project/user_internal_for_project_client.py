import logging
from typing import List

import requests
from pydantic import parse_obj_as

from melodi.base_client import BaseClient
from melodi.exceptions import MelodiAPIError
from melodi.logging import _log_melodi_http_errors
from melodi.user_internal_for_project.data_models import (
    BulkUserInternalForProjectRequest, BulkUserInternalForProjectResponse)


class UserInternalForProjectClient(BaseClient):
    def __init__(self, base_url: str, api_key: str):
        self.api_key = api_key
        self.base_url = base_url

        self.base_endpoint = (
            self.base_url + "/api/external/user-internal-for-project/bulk"
        )
        self.endpoint = (
            self.base_endpoint + f"?apiKey={self.api_key}"
        )

        self.logger = logging.getLogger(__name__)

    def set_users_internal(self, project_id: int, user_ids: List[int]) -> BulkUserInternalForProjectResponse:
        url = self.endpoint

        request = BulkUserInternalForProjectRequest(
            projectId=project_id,
            externalUserIds=user_ids
        )

        try:
            response = requests.request("POST", url, json=request.dict(by_alias=True))

            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()

            return parse_obj_as(BulkUserInternalForProjectResponse, response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def set_users_not_internal(self, project_id: int, user_ids: List[int]) -> None:
        url = self.endpoint

        request = BulkUserInternalForProjectRequest(
            projectId=project_id,
            externalUserIds=user_ids
        )

        try:
            response = requests.request("DELETE", url, json=request.dict(by_alias=True))

            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()

            return None
        except MelodiAPIError as e:
            raise MelodiAPIError(e)
