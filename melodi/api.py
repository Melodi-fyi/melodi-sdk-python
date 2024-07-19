import json
import logging
import os
import re
from typing import Optional

import requests

from .data_models import (BakeoffSample, BinarySample, Feedback,
                          FeedbackSample, Item, User, UserFeedback)
from .exceptions import MelodiAPIError


class MelodiClient:
    def __init__(self, api_key: Optional[str] = None, verbose=False):
        self.api_key = api_key or os.environ.get("MELODI_API_KEY")

        if not self.api_key:
            raise MelodiAPIError(
                "API key not found. Set the MELODI_API_KEY environment "
                "variable or pass it as an argument."
            )

        self.experiments_base_endpoint = (
            "https://app.melodi.fyi/api/external/experiments"
        )
        self.experiments_endpoint = (
            self.experiments_base_endpoint + f"?apiKey={self.api_key}"
        )

        self.log_item_base_endpoint = "https://app.melodi.fyi/api/external/logs"
        self.log_item_endpoint = self.log_item_base_endpoint + \
            f"?apiKey={self.api_key}"

        self.create_feedback_base_endpoint = "https://app.melodi.fyi/api/external/feedback"
        self.create_feedback_endpoint = (
            self.create_feedback_base_endpoint + f"?apiKey={self.api_key}"
        )

        self.logger = logging.getLogger(__name__)

        if verbose:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.ERROR)

    @staticmethod
    def _get_headers():
        return {"Content-Type": "application/json"}

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

        if response and response.status_code == 200:
            try:
                feedback_url = response.json().get("feedbackUrl")
                match = re.search(r"(\d+)$", feedback_url)
                exp_id = int(match.group(1))
                self.logger.info(
                    f"Experiment ID: {exp_id}",
                )
            except MelodiAPIError as e:
                raise MelodiAPIError(f"{e}")
        else:
            self.logger.error("Failed to extract experiment ID")

        return {"feedbackUrl": feedback_url, "experimentId": exp_id}

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
        request_data = {"experiment": {
            "name": name,
            "instructions": instructions,
            "project": project,
        }}

        return self._send_create_experiment_request(request_data=request_data)

    def create_log(self, item: Item):
        res = requests.request(
            "POST",
            url=self.log_item_endpoint,
            json=item.dict(),
            headers=self._get_headers(),
        )

        return res

    def create_feedback(self, sample: FeedbackSample, feedback: Feedback, user: User):
        user_feedback = UserFeedback(
            sample=sample, feedback=feedback, user=user)

        res = requests.request(
            "POST",
            url=self.create_feedback_endpoint,
            json=user_feedback.dict(),
            headers=self._get_headers(),
        )

        return res

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
            response = requests.post(endpoint, json=sample.dict())
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
        comparison = {"samples": [sample_1.dict(), sample_2.dict()]}
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
