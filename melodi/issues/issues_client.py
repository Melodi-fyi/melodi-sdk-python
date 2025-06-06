import logging

import requests
from pydantic import parse_obj_as

from melodi.base_client import BaseClient
from melodi.exceptions import MelodiAPIError
from melodi.issues.data_models import IssueResponse, IssueUpsertRequest
from melodi.logging import _log_melodi_http_errors


class IssuesClient(BaseClient):
    def __init__(self, base_url: str, api_key: str):
        self.api_key = api_key
        self.base_url = base_url

        self.base_endpoint = self.base_url + "/api/external/issues"
        self.endpoint = self.base_endpoint + f"?apiKey={self.api_key}"

        self.logger = logging.getLogger(__name__)

    def upsert(self, issueUpsertRequest: IssueUpsertRequest) -> IssueResponse:
        try:
            response = requests.put(
                self.endpoint, headers=self._get_headers(), json=issueUpsertRequest.dict(by_alias=True)
            )

            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()
            return parse_obj_as(IssueResponse, response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)
