import json
import logging
import types
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import openai.resources
from packaging.version import Version

logger = logging.getLogger(__name__)


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


OPENAI_CLIENTS_V0 = [
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

OPENAI_CLIENTS_V1 = [
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
    # Responses API support
    OpenAiDefinition(
        module="openai.resources.responses.responses",
        object="Responses",
        method="create",
        type="response",
        sync=True,
        min_version="1.80.0",  # Responses API was added in recent versions
    ),
    OpenAiDefinition(
        module="openai.resources.responses.responses",
        object="AsyncResponses",
        method="create",
        type="response",
        sync=False,
        min_version="1.80.0",
    ),
    OpenAiDefinition(
        module="openai.resources.responses.responses",
        object="Responses",
        method="parse",
        type="response",
        sync=True,
        min_version="1.80.0",
    ),
    OpenAiDefinition(
        module="openai.resources.responses.responses",
        object="AsyncResponses",
        method="parse",
        type="response",
        sync=False,
        min_version="1.80.0",
    ),
]

NON_STREAM_MESSAGE_KEYS = [
    "created",
    "id",
    "model",
    "object",
    "service_tier",
    "system_fingerprint",
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

# Responses API specific keys
RESPONSE_MESSAGE_KEYS = [
    "id",
    "created_at",
    "model",
    "object",
    "status",
    "output_text",
    "instructions",
    "metadata",
    "background",
    "max_output_tokens",
    "previous_response_id",
    "reasoning",
    "service_tier",
    "text",
    "truncation",
    "user",
    "parallel_tool_calls",
    "temperature",
    "tool_choice",
    "tools",
    "top_p",
]

RESPONSE_OUTPUT_MESSAGE_KEYS = [
    "id",
    "content",
    "role",
    "type",
]

RESPONSE_USAGE_KEYS = [
    "input_tokens",
    "output_tokens",
    "total_tokens",
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


def parse_metadata_value(input_value):
    input_value = strip_openai_objects(input_value)

    if isinstance(input_value, int) or isinstance(input_value, str):
        return input_value

    if isinstance(input_value, float):
        return str(input_value)

    if isinstance(input_value, list) or isinstance(input_value, dict):
        return json.dumps(input_value)

    logger.info(f"Could not parse metadata value: {input_value}")
    return None


def strip_openai_objects(input_value):
    if (
        input_value is None
        or isinstance(input_value, int)
        or isinstance(input_value, str)
        or isinstance(input_value, float)
    ):
        return input_value

    if isinstance(input_value, list):
        return [strip_openai_objects(element) for element in input_value]

    if isinstance(input_value, dict):
        return {key: strip_openai_objects(value) for key, value in input_value.items()}

    input_value = input_value.__dict__
    return {key: strip_openai_objects(value) for key, value in input_value.items()}
