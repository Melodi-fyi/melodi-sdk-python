import logging

import requests
from pydantic import parse_obj_as

from melodi.base_client import BaseClient
from melodi.exceptions import MelodiAPIError
from melodi.logging import _log_melodi_http_errors
from melodi.threads.data_models import (Thread, ThreadResponse,
                                        ThreadsPagedResponse,
                                        ThreadsQueryParams,
                                        ThreadsWithFeedbackPagedResponse)


class ThreadsClient(BaseClient):
    def __init__(self, base_url: str, api_key: str):
        self.api_key = api_key
        self.base_url = base_url

        self.base_endpoint = self.base_url + "/api/external/threads"
        self.endpoint = self.base_endpoint + f"?apiKey={self.api_key}"

        self.logger = logging.getLogger(__name__)


    def create(self, thread: Thread) -> ThreadResponse:
        createdAtString = None
        if (thread.createdAt):
            createdAtString = thread.createdAt.isoformat()
        threadjson = thread.dict(by_alias=True)
        threadjson['createdAt'] = createdAtString

        try:
            response = requests.post(
                self.endpoint, headers=self._get_headers(), json=threadjson
            )
            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()
            return parse_obj_as(ThreadResponse, response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def create_or_update(self, thread: Thread) -> ThreadResponse:
        createdAtString = None
        if (thread.createdAt):
            createdAtString = thread.createdAt.isoformat()
        threadjson = thread.dict(by_alias=True)
        threadjson['createdAt'] = createdAtString

        try:
            response = requests.put(
                self.endpoint, headers=self._get_headers(), json=threadjson
            )
            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()
            return parse_obj_as(ThreadResponse, response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)

    def get(self, query_params: ThreadsQueryParams = ThreadsQueryParams()) -> ThreadsPagedResponse | ThreadsWithFeedbackPagedResponse:
        url = f"{self.endpoint}&pageIndex={query_params.pageIndex}&pageSize={query_params.pageSize}"

        if (query_params.projectId):
            url = f"{url}&projectId={query_params.projectId}"
        if (query_params.ids):
            for threadId in query_params.ids:
                url = f"{url}&ids={threadId}"
        if (query_params.externalIds):
            for externalId in query_params.externalIds:
                url = f"{url}&externalIds={externalId}"
        if (query_params.before):
            url = f"{url}&before={query_params.before.isoformat()}"
        if (query_params.after):
            url = f"{url}&after={query_params.after.isoformat()}"
        if (query_params.search):
            url = f"{url}&search={query_params.search}"
        if (query_params.userSegmentIds):
            for userSegmentId in query_params.userSegmentIds:
                url = f"{url}&userSegmentIds={userSegmentId}"
        if (query_params.issueIds):
            for issueId in query_params.issueIds:
                url = f"{url}&issueIds={issueId}"
        if (query_params.intentIds):
            for intentId in query_params.intentIds:
                url = f"{url}&intentId={intentId}"
        if (query_params.hasFeedback):
            url = f"{url}&hasFeedback={query_params.hasFeedback}"
        if (query_params.includeFeedback):
            url = f"{url}&includeFeedback={query_params.includeFeedback}"

        try:
            response = requests.request("GET", url)

            _log_melodi_http_errors(self.logger, response)
            response.raise_for_status()

            if (query_params.includeFeedback):
                return parse_obj_as(ThreadsWithFeedbackPagedResponse, response.json())

            return parse_obj_as(ThreadsPagedResponse, response.json())
        except MelodiAPIError as e:
            raise MelodiAPIError(e)
