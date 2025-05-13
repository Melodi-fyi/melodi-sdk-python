import logging

import requests
from pydantic import parse_obj_as

from melodi.base_client import BaseClient
from melodi.exceptions import MelodiAPIError
from melodi.intents.data_models import IntentResponse, IntentUpsertRequest
from melodi.logging import _log_melodi_http_errors


class IntentsClient(BaseClient):
    def __init__(self, base_url: str, api_key: str):
        self.api_key = api_key
        self.base_url = base_url

        self.base_endpoint = self.base_url + "/api/external/intents"
        self.endpoint = self.base_endpoint + f"?apiKey={self.api_key}"

        self.logger = logging.getLogger(__name__)

    def upsert(self, intentUpsertRequest: IntentUpsertRequest) -> IntentResponse:
        try:
            response = requests.put(
                self.endpoint, headers=self._get_headers(), json=intentUpsertRequest.dict(by_alias=True)
            )

            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()
            return parse_obj_as(IntentResponse, response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)
