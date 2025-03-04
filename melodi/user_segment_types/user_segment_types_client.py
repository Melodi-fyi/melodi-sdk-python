import logging
from typing import List

import requests
from pydantic import parse_obj_as

from melodi.base_client import BaseClient
from melodi.exceptions import MelodiAPIError
from melodi.logging import _log_melodi_http_errors
from melodi.user_segment_types.data_models import (UserSegmentTypeDefinition,
                                                   UserSegmentTypesQueryParams)


class UserSegmentTypesClient(BaseClient):
    def __init__(self, base_url: str, api_key: str):
        self.api_key = api_key
        self.base_url = base_url

        self.base_endpoint = (
            self.base_url + "/api/external/users/segment-types"
        )
        self.endpoint = (
            self.base_endpoint + f"?apiKey={self.api_key}"
        )

        self.logger = logging.getLogger(__name__)

    def get(self, query_params: UserSegmentTypesQueryParams = UserSegmentTypesQueryParams()) -> List[UserSegmentTypeDefinition]:
        url = self.endpoint

        if (query_params.projectId):
            url = f"{url}&projectId={query_params.projectId}"

        try:
            response = requests.request("GET", url)

            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()

            return parse_obj_as(List[UserSegmentTypeDefinition], response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)
