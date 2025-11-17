import logging
from datetime import datetime

import requests
from pydantic import parse_obj_as

from melodi.base_client import BaseClient
from melodi.exceptions import MelodiAPIError
from melodi.logging import _log_melodi_http_errors
from melodi.threads.data_models import (SimpleProject, Thread, ThreadResponse,
                                        ThreadsPagedResponse,
                                        ThreadsQueryParams)


def _empty_thread_response() -> ThreadResponse:
    return ThreadResponse(
        id=0,
        organizationId=0,
        project=SimpleProject(id=0, name="SAMPLE"),
        messages=[],
        metadata={},
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )


class ThreadsClient(BaseClient):
    def __init__(self, base_url: str, api_key: str):
        self.api_key = api_key
        self.base_url = base_url

        self.base_endpoint = self.base_url + "/api/external/threads"
        self.endpoint = self.base_endpoint + f"?apiKey={self.api_key}"

        self.logger = logging.getLogger(__name__)


    def create(self, thread: Thread) -> ThreadResponse:
        return _empty_thread_response()

    def create_or_update(self, thread: Thread) -> ThreadResponse:
        return _empty_thread_response()

    def get(self, query_params: ThreadsQueryParams = ThreadsQueryParams()) -> ThreadsPagedResponse:
        return ThreadsPagedResponse(
            count=0,
            rows=[]
        )
