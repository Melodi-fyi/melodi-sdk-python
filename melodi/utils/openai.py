"""
Melodi: OpenAI API Wrapper with Full Logging

Melodi provides a seamless drop-in replacement for the OpenAI Python SDK,
adding automatic logging with minimal code changes. Simply update your import:

```diff
- import openai
+ from melodi.openai import openai
```
"""

import logging
import os
from typing import Callable, Optional

from packaging.version import Version
from wrapt import wrap_function_wrapper

from melodi.melodi_client import MelodiClient
from melodi.utils.openai_nonstream_extractor import (
    create_melodi_thread_from_openai_response,
)
from melodi.utils.openai_prompt_parser import _get_melodi_messages_from_openai_prompt
from melodi.utils.openai_responses_extractor import (
    create_melodi_thread_from_responses_response,
)
from melodi.utils.openai_responses_prompt_parser import (
    get_melodi_messages_from_responses_prompt,
)
from melodi.utils.openai_responses_stream_generator import (
    MelodiResponsesGeneratorAsync,
    MelodiResponsesGeneratorSync,
)
from melodi.utils.openai_stream_generator import (
    MelodiResponseGeneratorAsync,
    MelodiResponseGeneratorSync,
)
from melodi.utils.openai_utils import (
    OPENAI_CLIENTS_V0,
    OPENAI_CLIENTS_V1,
    OpenAiDefinition,
    OpenAiKwargsExtractor,
    _is_openai_v1,
    _is_streaming_response,
)
from melodi.utils.utils import create_error_melodi_thread

try:
    import openai
except ImportError:
    raise ModuleNotFoundError("OpenAI not installed, please run: 'pip install openai'")

try:
    from openai import AsyncAzureOpenAI, AsyncOpenAI, AzureOpenAI, OpenAI  # noqa: F401
except ImportError:
    AsyncAzureOpenAI = None
    AsyncOpenAI = None
    AzureOpenAI = None
    OpenAI = None

logger = logging.getLogger("melodi")


def melodi_openai_wrapper(func):
    def melodi_wrapper(open_ai_definitions, initialize):
        def wrapper(wrapped, instance, args, kwargs):
            return func(
                open_ai_definitions,
                initialize,
                wrapped,
                kwargs,
            )

        return wrapper

    return melodi_wrapper


@melodi_openai_wrapper
def _wrap(
    openai_resource: OpenAiDefinition,
    melodi_initialize_func: Callable,
    wrapped: Callable,
    kwargs: dict,
):
    melodi_client = melodi_initialize_func()
    arg_extractor = OpenAiKwargsExtractor(**kwargs)

    # Choose the appropriate prompt parser based on API type
    if openai_resource.type == "response":
        prompt_messages = get_melodi_messages_from_responses_prompt(
            kwargs, openai_resource
        )
    else:
        prompt_messages = _get_melodi_messages_from_openai_prompt(
            kwargs, openai_resource
        )

    try:
        openai_response = wrapped(**arg_extractor.get_openai_args())

        if _is_streaming_response(openai_response):
            try:
                # Choose the appropriate streaming generator based on API type
                if openai_resource.type == "response":
                    return MelodiResponsesGeneratorSync(
                        openai_resource=openai_resource,
                        openai_response=openai_response,
                        melodi_client=melodi_client,
                        prompt_messages=prompt_messages,
                    )
                else:
                    return MelodiResponseGeneratorSync(
                        openai_resource=openai_resource,
                        openai_response=openai_response,
                        melodi_client=melodi_client,
                        prompt_messages=prompt_messages,
                    )
            except Exception as ex:
                logger.error(
                    f"Could not create Melodi thread out of streamed response: {repr(ex)}"
                )
        else:
            # Choose the appropriate response handler based on API type
            if openai_resource.type == "response":
                create_melodi_thread_from_responses_response(
                    openai_resource=openai_resource,
                    openai_response=openai_response,
                    prompt_messages=prompt_messages,
                    melodi_client=melodi_client,
                )
            else:
                create_melodi_thread_from_openai_response(
                    openai_resource=openai_resource,
                    openai_response=openai_response,
                    prompt_messages=prompt_messages,
                    melodi_client=melodi_client,
                )

        return openai_response
    except Exception as ex:
        logger.warning(ex)
        create_error_melodi_thread(
            melodi_client=melodi_client,
            prompt_messages=prompt_messages,
            model=kwargs.get("model"),
            exception=str(ex),
        )
        raise ex


@melodi_openai_wrapper
async def _wrap_async(
    openai_resource: OpenAiDefinition,
    melodi_initialize_func: Callable,
    wrapped: Callable,
    kwargs: dict,
):
    melodi_client = melodi_initialize_func()
    arg_extractor = OpenAiKwargsExtractor(**kwargs)

    # Choose the appropriate prompt parser based on API type
    if openai_resource.type == "response":
        prompt_messages = get_melodi_messages_from_responses_prompt(
            kwargs, openai_resource
        )
    else:
        prompt_messages = _get_melodi_messages_from_openai_prompt(
            kwargs, openai_resource
        )

    try:
        openai_response = await wrapped(**arg_extractor.get_openai_args())

        if _is_streaming_response(openai_response):
            try:
                # Choose the appropriate streaming generator based on API type
                if openai_resource.type == "response":
                    return MelodiResponsesGeneratorAsync(
                        openai_resource=openai_resource,
                        openai_response=openai_response,
                        melodi_client=melodi_client,
                        prompt_messages=prompt_messages,
                    )
                else:
                    return MelodiResponseGeneratorAsync(
                        openai_resource=openai_resource,
                        openai_response=openai_response,
                        melodi_client=melodi_client,
                        prompt_messages=prompt_messages,
                    )
            except Exception as ex:
                logger.error(
                    f"Could not create Melodi thread out of streamed response: {repr(ex)}"
                )
        else:
            # Choose the appropriate response handler based on API type
            if openai_resource.type == "response":
                create_melodi_thread_from_responses_response(
                    openai_resource=openai_resource,
                    openai_response=openai_response,
                    prompt_messages=prompt_messages,
                    melodi_client=melodi_client,
                )
            else:
                create_melodi_thread_from_openai_response(
                    openai_resource=openai_resource,
                    openai_response=openai_response,
                    prompt_messages=prompt_messages,
                    melodi_client=melodi_client,
                )

        return openai_response
    except Exception as ex:
        logger.warning(ex)
        create_error_melodi_thread(
            melodi_client=melodi_client,
            prompt_messages=prompt_messages,
            model=kwargs.get("model"),
            exception=str(ex),
        )
        raise ex


class OpenAIMelodi:
    melodi_client: Optional[MelodiClient] = None

    def initialize(self):
        if self.melodi_client is None:
            self.melodi_client = MelodiClient(
                api_key=os.getenv("MELODI_API_KEY"), verbose=True
            )

        return self.melodi_client

    def register_tracing(self):
        resources = OPENAI_CLIENTS_V1 if _is_openai_v1() else OPENAI_CLIENTS_V0

        for resource in resources:
            if resource.min_version is not None and Version(
                openai.__version__
            ) < Version(resource.min_version):
                continue

            wrap_function_wrapper(
                module=resource.module,
                name=f"{resource.object}.{resource.method}",
                wrapper=_wrap(
                    open_ai_definitions=resource,
                    initialize=self.initialize,
                )
                if resource.sync
                else _wrap_async(
                    open_ai_definitions=resource,
                    initialize=self.initialize,
                ),
            )


modifier = OpenAIMelodi()
modifier.register_tracing()
