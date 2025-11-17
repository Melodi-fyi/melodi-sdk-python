import logging
from typing import List

import requests
from pydantic import parse_obj_as

from melodi.base_client import BaseClient
from melodi.exceptions import MelodiAPIError
from melodi.logging import _log_melodi_http_errors
from melodi.user_internal_for_project.data_models import (
    BulkUserInternalForProjectRequest, BulkUserInternalForProjectResponse)


def _empty_bulk_user_internal_for_project_response() -> BulkUserInternalForProjectResponse:
    return BulkUserInternalForProjectResponse(
        count=0,
    )


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
        return BulkUserInternalForProjectResponse(
            count=0,
        )

    def set_users_not_internal(self, project_id: int, user_ids: List[int]) -> None:
        return None
