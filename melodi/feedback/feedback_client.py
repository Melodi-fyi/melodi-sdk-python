import logging

import requests
from pydantic import parse_obj_as

from melodi.base_client import BaseClient
from melodi.exceptions import MelodiAPIError
from melodi.feedback.data_models import (Feedback,
                                         FeedbackCreateOrUpdateRequest,
                                         FeedbackResponse)
from melodi.logging import _log_melodi_http_errors


class FeedbackClient(BaseClient):
    def __init__(self, base_url: str, api_key: str):
        self.api_key = api_key
        self.base_url = base_url

        self.base_endpoint = (
            self.base_url + "/api/external/feedback"
        )
        self.endpoint = (
            self.base_endpoint + f"?apiKey={self.api_key}"
        )

        self.logger = logging.getLogger(__name__)

    def create(self, feedback: Feedback) -> FeedbackResponse:
        try:
            createdAtString = None
            if (feedback.createdAt):
                createdAtString = feedback.createdAt.isoformat()
            feedbackJson = feedback.dict(by_alias=True)
            feedbackJson['createdAt'] = createdAtString

            response = requests.request(
                "POST",
                url=self.endpoint,
                json=feedbackJson,
                headers=self._get_headers(),
            )

            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()
            return parse_obj_as(FeedbackResponse, response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def create_or_update(self, update: FeedbackCreateOrUpdateRequest) -> FeedbackResponse:
        try:
            createdAtString = None
            if (update.createdAt):
                createdAtString = update.createdAt.isoformat()
            feedbackJson = update.dict(by_alias=True)
            feedbackJson['createdAt'] = createdAtString

            response = requests.request(
                "PUT",
                url=self.endpoint,
                json=feedbackJson,
                headers=self._get_headers(),
            )

            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()
            return parse_obj_as(FeedbackResponse, response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

