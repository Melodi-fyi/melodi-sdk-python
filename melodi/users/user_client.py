import logging

import requests
from pydantic import parse_obj_as

from melodi.base_client import BaseClient
from melodi.exceptions import MelodiAPIError
from melodi.logging import _log_melodi_http_errors
from melodi.users.data_models import User, UserResponse


class UserClient(BaseClient):
    def __init__(self, base_url: str, api_key: str):
        self.api_key = api_key
        self.base_url = base_url

        self.base_endpoint = (
            self.base_url + "/api/external/users"
        )
        self.endpoint = (
            self.base_endpoint + f"?apiKey={self.api_key}"
        )

        self.logger = logging.getLogger(__name__)

    def create_or_update(self, user: User) -> UserResponse:
        url = f"{self.base_endpoint}?apiKey={self.api_key}"

        try:
            response = requests.put(
                url, headers=self._get_headers(), json=user.dict(by_alias=True)
            )

            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()
            return parse_obj_as(UserResponse, response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def update(self, user: User) -> User:
        url = f"{self.base_endpoint}/{user.externalId}?apiKey={self.api_key}"

        try:
            response = requests.patch(
                url, headers=self._get_headers(), json=user.dict(by_alias=True)
            )

            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()
            return parse_obj_as(UserResponse, response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)
