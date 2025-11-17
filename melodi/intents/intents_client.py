import logging
from datetime import datetime

import requests
from pydantic import parse_obj_as

from melodi.base_client import BaseClient
from melodi.exceptions import MelodiAPIError
from melodi.intents.data_models import IntentResponse, IntentUpsertRequest
from melodi.logging import _log_melodi_http_errors


def _empty_intent_response() -> IntentResponse:
    return IntentResponse(
        id=0,
        name="SAMPLE",
        createdAt=datetime.now(),
    )


class IntentsClient(BaseClient):
    def __init__(self, base_url: str, api_key: str):
        self.api_key = api_key
        self.base_url = base_url

        self.base_endpoint = self.base_url + "/api/external/intents"
        self.endpoint = self.base_endpoint + f"?apiKey={self.api_key}"

        self.logger = logging.getLogger(__name__)

    def upsert(self, intentUpsertRequest: IntentUpsertRequest) -> IntentResponse:
        return _empty_intent_response()