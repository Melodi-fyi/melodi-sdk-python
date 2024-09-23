import logging
import os
from typing import Optional

from melodi.experiments.experiments_client import ExperimentsClient
from melodi.feedback.feedback_client import FeedbackClient
from melodi.messages.messages_client import MessagesClient
from melodi.projects.projects_client import ProjectsClient
from melodi.threads.threads_client import ThreadsClient
from melodi.users.user_client import UserClient

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

        self.logger = logging.getLogger(__name__)

        self.threads = ThreadsClient(base_url=self.base_url, api_key=self.api_key)
        self.projects = ProjectsClient(base_url=self.base_url, api_key=self.api_key)
        self.feedback = FeedbackClient(base_url=self.base_url, api_key=self.api_key)
        self.users = UserClient(base_url=self.base_url, api_key=self.api_key)
        self.messages = MessagesClient(base_url=self.base_url, api_key=self.api_key)
        self.experiments = ExperimentsClient(base_url=self.base_url, api_key=self.api_key)

        if verbose:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.ERROR)

    @staticmethod
    def _get_headers():
        return {"Content-Type": "application/json"}

