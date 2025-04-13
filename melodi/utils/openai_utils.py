from dataclasses import dataclass
from typing import Optional

import types
import openai.resources
from packaging.version import Version

from datetime import datetime, timezone


class OpenAiKwargsExtractor:
    def __init__(
        self,
        **kwargs,
    ):
        self.kwargs = kwargs

    def get_openai_args(self):
        return self.kwargs


@dataclass
class OpenAiDefinition:
    module: str
    object: str
    method: str
    type: str
    sync: bool
    min_version: Optional[str] = None


OPENAI_METHODS_V0 = [
    OpenAiDefinition(
        module="openai",
        object="ChatCompletion",
        method="create",
        type="chat",
        sync=True,
    ),
    OpenAiDefinition(
        module="openai",
        object="Completion",
        method="create",
        type="completion",
        sync=True,
    ),
]

# TODO this and the above needs thorough testing
OPENAI_METHODS_V1 = [
    OpenAiDefinition(
        module="openai.resources.chat.completions",
        object="Completions",
        method="create",
        type="chat",
        sync=True,
    ),
    OpenAiDefinition(
        module="openai.resources.completions",
        object="Completions",
        method="create",
        type="completion",
        sync=True,
    ),
    OpenAiDefinition(
        module="openai.resources.chat.completions",
        object="AsyncCompletions",
        method="create",
        type="chat",
        sync=False,
    ),
    OpenAiDefinition(
        module="openai.resources.completions",
        object="AsyncCompletions",
        method="create",
        type="completion",
        sync=False,
    ),
]

COMPLETION_CHOICE_KEYS = [
    "finish_reason",
    "index",
    "logprobs",
]

COMPLETION_CHOICE_MESSAGE_KEYS = [
    "content",
    "refusal",
    "role",
    "annotations",
    "function_call",
    "tool_calls",
]

COMPLETION_USAGE_KEYS = [
    "completion_tokens",
    "prompt_tokens",
    "total_tokens",
]

COMPLETION_USAGE_TOKENS_KEYS = [
    "accepted_prediction_tokens",
    "reasoning_tokens",
    "rejected_prediction_tokens",
]

COMPLETION_USAGE_PROMPT_TOKENS_KEYS = [
    "cached_tokens",
]

GENERATION_PARAMETERS_DEFAULTS = {
    "frequency_penalty": 0,
    "logit_bias": None,
    "logprobs": False,
    "max_completion_tokens": None,
    "max_tokens": None,
    "modalities": None,
    "n": 1,
    "parallel_tool_calls": True,
    "prediction": None,
    "presence_penalty": 0,
    "reasoning_effort": "medium",
    "response_format": None,
    "seed": None,
    "service_tier": "auto",
    "stop": None,
    "store": False,
    "stream": False,
    "stream_options": None,
    "temperature": 1,
    "tool_choice": None,
    "top_logprobs": None,
    "top_p": 1,
    "user": None,
    "web_search_options": None,
    "metadata": None,
}


def time_now(user_timezone=timezone.utc, as_string: bool = False):
    if as_string:
        return str(datetime.now(user_timezone))

    return datetime.now(user_timezone)


def _is_openai_v1():
    return Version(openai.__version__) >= Version("1.0.0")


def _is_streaming_response(response):
    return (
        isinstance(response, types.GeneratorType)
        or isinstance(response, types.AsyncGeneratorType)
        or (_is_openai_v1() and isinstance(response, openai.Stream))
        or (_is_openai_v1() and isinstance(response, openai.AsyncStream))
    )


def clean_dict_value(d):
    if not isinstance(d, dict):
        return d if d else False  # use a custom test if needed
    return {key: v for key, value in d.items() if (v := clean_dict_value(value))}
