import logging
from datetime import datetime

import requests
from pydantic import parse_obj_as

from melodi.base_client import BaseClient
from melodi.exceptions import MelodiAPIError
from melodi.feedback.data_models import (Feedback,
                                         FeedbackCreateOrUpdateRequest,
                                         FeedbackResponse)
from melodi.logging import _log_melodi_http_errors


def _empty_feedback_response() -> FeedbackResponse:
    return FeedbackResponse(
        id=0,
        projectId=0,
        attributeOptions=[],
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )


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
        return _empty_feedback_response()

    def create_or_update(self, update: FeedbackCreateOrUpdateRequest) -> FeedbackResponse:
        return _empty_feedback_response()
