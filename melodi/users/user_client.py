import logging

import requests
from pydantic import parse_obj_as

from melodi.base_client import BaseClient
from melodi.exceptions import MelodiAPIError
from melodi.logging import _log_melodi_http_errors
from melodi.users.data_models import (User, UserResponse, UsersPagedResponse,
                                      UsersQueryParams)


def _empty_user_response() -> UserResponse:
    return UserResponse(
        id=0,
        externalId="SAMPLE",
        email=None,
        name=None,
        username=None,
        segments=[]
    )

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

    def get(self, query_params: UsersQueryParams = UsersQueryParams()) -> UsersPagedResponse:
        return UsersPagedResponse(
            count=0,
            rows=[]
        )

    def create_or_update(self, user: User) -> UserResponse:
        return _empty_user_response()

    def update(self, user: User) -> User:
        return user
