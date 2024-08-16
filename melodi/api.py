import json
import logging
import os
import re
from typing import List, Optional

import requests
from pydantic.tools import parse_obj_as
from requests.models import Response

from .data_models import (BakeoffSample, BinarySample, Comparisons, Feedback,
                          FeedbackResponse, IntentLogAssociation,
                          IssueLogAssociation, Log, LogResponse,
                          ProjectResponse, Samples, Thread, ThreadResponse)
from .exceptions import MelodiAPIError


class MelodiClient:
    def __init__(self, api_key: Optional[str] = None, verbose=False):
        self.api_key = api_key or os.environ.get("MELODI_API_KEY")

        if not self.api_key:
            raise MelodiAPIError(
                "API key not found. Set the MELODI_API_KEY environment "
                "variable or pass it as an argument."
            )

        self.base_url = os.environ.get("MELODI_BASE_URL_OVERRIDE") or "https://app.melodi.fyi"

        self.experiments_base_endpoint = (
            self.base_url + "/api/external/experiments"
        )
        self.experiments_endpoint = (
            self.experiments_base_endpoint + f"?apiKey={self.api_key}"
        )

        self.create_feedback_base_endpoint = (
            self.base_url + "/api/external/feedback"
        )
        self.create_feedback_endpoint = (
            self.create_feedback_base_endpoint + f"?apiKey={self.api_key}"
        )

        self.logs_base_endpoint = self.base_url + "/api/external/logs"
        self.logs_endpont = self.logs_base_endpoint + f"?apiKey={self.api_key}"

        self.threads_base_endpoint = self.base_url + "/api/external/threads"
        self.threads_endpoint = self.threads_base_endpoint + f"?apiKey={self.api_key}"

        self.issue_log_associations_base_endpoint = self.base_url + "/api/external/issue-log-associations"
        self.issue_log_associations_endpoint = self.issue_log_associations_base_endpoint + f"?apiKey={self.api_key}"

        self.intent_log_associations_base_endpoint = self.base_url + "/api/external/intent-log-associations"
        self.intent_log_associations_endpoint = self.intent_log_associations_base_endpoint + f"?apiKey={self.api_key}"

        self.projects_base_endpoint = self.base_url + "/api/external/projects"
        self.projects_endpoint = self.projects_base_endpoint + f"?apiKey={self.api_key}"

        self.logger = logging.getLogger(__name__)

        if verbose:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.ERROR)

    @staticmethod
    def _get_headers():
        return {"Content-Type": "application/json"}

    def _log_melodi_http_errors(self, response: Response):
        if (response.status_code == 400):
            try:
                responseJson = response.json()
                if (responseJson["errors"]):
                    for error in responseJson["errors"]:
                        self.logger.error(f"Bad Request response from Melodi API: {error}")
            except:
                pass

    def _send_create_experiment_request(self, request_data):
        response = None

        try:
            response = requests.post(
                self.experiments_endpoint,
                headers=self._get_headers(),
                json=request_data,
            )
            response.raise_for_status()
            self.logger.info("Successfully created Melodi experiment.")

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to create Melodi experiment: {e}")
            self.logger.error(f"Response: {response.json()}")

        if response and response.status_code == 200:
            try:
                feedback_url = response.json().get("feedbackUrl")
                match = re.search(r"(\d+)$", feedback_url)
                exp_id = int(match.group(1))
                self.logger.info(
                    f"Experiment ID: {exp_id}",
                )
                return {"feedbackUrl": feedback_url, "experimentId": exp_id}
            except MelodiAPIError as e:
                raise MelodiAPIError(f"{e}")
        else:
            self.logger.error("Failed to extract experiment ID")



    def load_samples(self, file_path: str, experiment_type: str) -> list:
        res = []
        self.logger.info(msg=f"Loading samples from: {file_path}")

        if experiment_type == "binary":
            self.logger.info(f"Experiment type = binary")
            with open(file_path, "r") as file:
                for line in file:
                    json_object = json.loads(line.strip())

                    if "response" not in json_object:
                        raise Exception(
                            f'Sample {json_object} is missing "response" ' f"attribute."
                        )

                    res.append(json_object)

        elif experiment_type == "bake_off":
            self.logger.info(f"Experiment type = bake-off")
            with open(file_path, "r") as file:
                for line in file:
                    json_object = json.loads(line.strip())
                    samples = json_object["samples"]

                    for sample in samples:
                        if "response" not in sample:
                            raise Exception(
                                f'Sample {sample} is missing "response" ' f"attribute."
                            )

                        elif "version" not in sample:
                            raise Exception(
                                f'Sample {sample} is missing "version" ' f"attribute."
                            )

                    res.append(json_object)

        self.logger.info(msg=f"Loaded {len(res)} samples")

        return res

    def get_experiments(self):
        return requests.request("GET", self.experiments_endpoint)

    def create_experiment(self, name: str, instructions: str, project: str):
        request_data = {
            "experiment": {
                "name": name,
                "instructions": instructions,
                "project": project,
            }
        }

        return self._send_create_experiment_request(request_data=request_data)

    def create_experiment_with_samples(
        self,
        name: str,
        samples: Samples,
        instructions: str = None,
        project: str = None,
        version: str = None,
    ):
        request_data = {
            "experiment": {
                "name": name,
                "instructions": instructions,
                "project": project,
                "version": version
            },
            "samples": samples
        }

        return self._send_create_experiment_request(request_data=request_data)

    def create_experiment_with_comparisons(
        self,
        name: str,
        comparisons: Comparisons,
        instructions: str = None,
        project: str = None,
        version: str = None,
    ):
        request_data = {
            "experiment": {
                "name": name,
                "instructions": instructions,
                "project": project,
                "version": version
            },
            "comparisons": comparisons
        }

        return self._send_create_experiment_request(request_data=request_data)

    def create_log(self, log: Log) -> LogResponse:
        try:
            response = requests.post(
                self.logs_endpont,
                headers=self._get_headers(),
                json=log.dict(by_alias=True),
            )

            self._log_melodi_http_errors(response)
            response.raise_for_status()
            return parse_obj_as(LogResponse, response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def create_feedback(self, feedback: Feedback) -> FeedbackResponse:
        try:
            response = requests.request(
                "POST",
                url=self.create_feedback_endpoint,
                json=feedback.dict(by_alias=True),
                headers=self._get_headers(),
            )


            self._log_melodi_http_errors(response)
            response.raise_for_status()
            return parse_obj_as(FeedbackResponse, response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def create_binary_evaluation_experiment(
        self,
        name: str,
        samples: list,
        instructions: Optional[str] = None,
        project: Optional[str] = None,
    ) -> None:
        if not name:
            raise ValueError("Experiment name is required.")

        request_data = {
            "experiment": {
                "name": name,
                "instructions": instructions,
                "project": project,
            },
            "samples": samples,
        }

        return self._send_create_experiment_request(request_data=request_data)

    def create_bake_off_evaluation_experiment(
        self,
        name: str,
        comparisons: list,
        instructions: Optional[str] = None,
        project: Optional[str] = None,
    ) -> None:
        if not name:
            raise ValueError("Experiment name is required.")

        request_data = {
            "experiment": {
                "name": name,
                "instructions": instructions,
                "project": project,
            },
            "comparisons": comparisons,
        }

        return self._send_create_experiment_request(request_data=request_data)

    def log_binary_sample(self, experiment_id: int, sample: BinarySample) -> None:
        endpoint = f"{self.experiments_base_endpoint}/{experiment_id}/samples?apiKey={self.api_key}"

        try:
            response = requests.post(endpoint, json=sample.dict(by_alias=True))
            response.raise_for_status()
            return response
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def log_bake_off_comparison(
        self,
        experiment_id: int,
        sample_1: BakeoffSample,
        sample_2: BakeoffSample,
    ) -> None:
        comparison = {"samples": [sample_1.dict(by_alias=True), sample_2.dict(by_alias=True)]}
        endpoint = f"{self.experiments_base_endpoint}/{experiment_id}/comparisons?apiKey={self.api_key}"

        try:
            response = requests.post(
                endpoint, headers=self._get_headers(), json=comparison
            )
            response.raise_for_status()
            return response
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def make_shareable(self, experiment_id: int) -> Optional[str]:
        url = f"{self.experiments_base_endpoint}/{experiment_id}/shareable-link?apiKey={self.api_key}"

        response = requests.post(url)

        return (
            response.json().get("shareableLink")
            if response.status_code == 200
            else None
        )

    def create_thread(self, thread: Thread) -> ThreadResponse:
        url = self.threads_endpoint

        try:
            response = requests.post(
                url, headers=self._get_headers(), json=thread.dict(by_alias=True)
            )
            self._log_melodi_http_errors(response)
            response.raise_for_status()
            return parse_obj_as(Thread, response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def get_log(self, log_id: int) -> LogResponse:
        url = f"{self.logs_base_endpoint}/{log_id}?apiKey={self.api_key}"

        try:
            response = requests.request("GET", url)

            self._log_melodi_http_errors(response)
            response.raise_for_status()
            return parse_obj_as(LogResponse, response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def add_issue_to_log(self, issue_id: int, log_id: int) -> IssueLogAssociation:
        url = self.issue_log_associations_endpoint

        try:
            response = requests.post(
                url, headers=self._get_headers(), json={"issueId": issue_id, "logId": log_id}
            )

            self._log_melodi_http_errors(response)
            response.raise_for_status()
            return response.json()
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def remove_issue_from_log(self, issue_id: int, log_id: int) -> None:
        log = self.get_log(log_id)

        for issue_association in log.issueAssociations:
            if (issue_association.issueId == issue_id):
                issue_log_association_id = issue_association.id
                break

        if not issue_log_association_id:
            raise MelodiAPIError(f"Issue {issue_id} is not associated to log {log_id}")

        url = f"{self.issue_log_associations_base_endpoint}/{issue_log_association_id}?apiKey={self.api_key}"

        try:
            response = requests.delete(
                url, headers=self._get_headers()
            )

            self._log_melodi_http_errors(response)
            response.raise_for_status()
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def add_intent_to_log(self, intent_id: int, log_id: int) -> IntentLogAssociation:
        url = self.intent_log_associations_endpoint

        try:
            response = requests.post(
                url, headers=self._get_headers(), json={"intentId": intent_id, "logId": log_id}
            )

            self._log_melodi_http_errors(response)
            response.raise_for_status()
            return response.json()
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def remove_intent_from_log(self, intent_id: int, log_id: int) -> None:
        log = self.get_log(log_id)

        for intent_association in log.intentAssociations:
            if (intent_association.intentId == intent_id):
                intent_log_association_id = intent_association.id
                break

        if not intent_log_association_id:
            raise MelodiAPIError(f"Intent {intent_id} is not associated to log {log_id}")

        url = f"{self.intent_log_associations_base_endpoint}/{intent_log_association_id}?apiKey={self.api_key}"

        try:
            response = requests.delete(
                url, headers=self._get_headers()
            )

            self._log_melodi_http_errors(response)
            response.raise_for_status()
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def list_projects(self) -> List[ProjectResponse]:
        try:
            response = requests.request("GET", self.projects_endpoint)

            self._log_melodi_http_errors(response)
            response.raise_for_status()

            return parse_obj_as(List[ProjectResponse], response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def create_project(self, name: str) -> ProjectResponse:
        url = self.projects_endpoint

        try:
            response = requests.post(
                url, headers=self._get_headers(), json={"name": name}
            )

            self._log_melodi_http_errors(response)
            response.raise_for_status()
            return parse_obj_as(ProjectResponse, response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)
