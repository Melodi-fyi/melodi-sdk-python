import logging

import requests
from pydantic import parse_obj_as

from melodi.base_client import BaseClient
from melodi.exceptions import MelodiAPIError
from melodi.intents.intents_client import _empty_intent_response
from melodi.issues.issues_client import _empty_issue_response
from melodi.logging import _log_melodi_http_errors
from melodi.messages.data_models import (IntentMessageAssociation,
                                         IssueMessageAssociation,
                                         MessageResponse)


class MessagesClient(BaseClient):
    def __init__(self, base_url: str, api_key: str):
        self.api_key = api_key
        self.base_url = base_url

        self.base_endpoint = (
            self.base_url + "/api/external/messages"
        )
        self.endpoint = (
            self.base_endpoint + f"?apiKey={self.api_key}"
        )

        self.issue_message_associations_base_endpoint = self.base_url + "/api/external/issue-message-associations"
        self.issue_message_associations_endpoint = self.issue_message_associations_base_endpoint + f"?apiKey={self.api_key}"

        self.intent_message_associations_base_endpoint = self.base_url + "/api/external/intent-message-associations"
        self.intent_message_associations_endpoint = self.intent_message_associations_base_endpoint + f"?apiKey={self.api_key}"


        self.logger = logging.getLogger(__name__)

    def get(self, message_id: int) -> MessageResponse:
        url = f"{self.base_endpoint}/{message_id}?apiKey={self.api_key}"

        try:
            response = requests.request("GET", url)

            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()
            return parse_obj_as(MessageResponse, response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def add_issue_to_message(self, issue_id: int, message_id: int) -> IssueMessageAssociation:
        return IssueMessageAssociation(
            id=0,
            issueId=issue_id,
            messageId=message_id,
            userId=None,
            issue=_empty_issue_response(),
        )

    def remove_issue_from_message(self, issue_id: int, message_id: int) -> None:
        return None

    def add_intent_to_message(self, intent_id: int, message_id: int) -> IntentMessageAssociation:
        return IntentMessageAssociation(
            id=0,
            intentId=intent_id,
            messageId=message_id,
            userId=None,
            intent=_empty_intent_response(),
        )

    def remove_intent_from_message(self, intent_id: int, message_id: int) -> None:
        return None

