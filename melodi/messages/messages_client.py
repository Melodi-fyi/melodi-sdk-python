import logging

import requests
from pydantic import parse_obj_as

from melodi.base_client import BaseClient
from melodi.exceptions import MelodiAPIError
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
        url = self.issue_message_associations_endpoint

        try:
            response = requests.post(
                url, headers=self._get_headers(), json={"issueId": issue_id, "messageId": message_id}
            )

            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()
            return response.json()
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def remove_issue_from_message(self, issue_id: int, message_id: int) -> None:
        message = self.get(message_id)

        for issue_association in message.issueAssociations:
            if (issue_association.issueId == issue_id):
                issue_message_association_id = issue_association.id
                break

        if not issue_message_association_id:
            raise MelodiAPIError(f"Issue {issue_id} is not associated to message {message_id}")

        url = f"{self.issue_message_associations_base_endpoint}/{issue_message_association_id}?apiKey={self.api_key}"

        try:
            response = requests.delete(
                url, headers=self._get_headers()
            )

            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def add_intent_to_message(self, intent_id: int, message_id: int) -> IntentMessageAssociation:
        url = self.intent_message_associations_endpoint

        try:
            response = requests.post(
                url, headers=self._get_headers(), json={"intentId": intent_id, "messageId": message_id}
            )

            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()
            return response.json()
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def remove_intent_from_message(self, intent_id: int, message_id: int) -> None:
        message = self.get(message_id)

        for intent_association in message.intentAssociations:
            if (intent_association.intentId == intent_id):
                intent_message_association_id = intent_association.id
                break

        if not intent_message_association_id:
            raise MelodiAPIError(f"Intent {intent_id} is not associated to log {message_id}")

        url = f"{self.intent_message_associations_base_endpoint}/{intent_message_association_id}?apiKey={self.api_key}"

        try:
            response = requests.delete(
                url, headers=self._get_headers()
            )

            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

