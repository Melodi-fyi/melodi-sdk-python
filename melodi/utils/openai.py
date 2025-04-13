"""
Melodi: OpenAI API Wrapper with Full Logging

Melodi provides a seamless drop-in replacement for the OpenAI Python SDK,
adding automatic logging with minimal code changes. Simply update your import:

```diff
- import openai
+ from melodi.openai import openai
```

Features:
* TODO
"""

import logging
import os
from typing import Optional, Callable

import openai.resources

from packaging.version import Version
from wrapt import wrap_function_wrapper

from melodi.melodi_client import MelodiClient
from melodi.utils.openai_nonstream_extractor import (
    create_melodi_thread_from_openai_response,
)
from melodi.utils.openai_prompt_parser import _get_melodi_messages_from_openai_prompt
from melodi.utils.openai_stream_generator import (
    MelodiResponseGeneratorSync,
    MelodiResponseGeneratorAsync,
)
from melodi.utils.openai_utils import (
    _is_openai_v1,
    OpenAiDefinition,
    OPENAI_METHODS_V1,
    OPENAI_METHODS_V0,
    _is_streaming_response,
    OpenAiKwargsExtractor,
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

    prompt_messages = _get_melodi_messages_from_openai_prompt(kwargs, openai_resource)
    try:
        openai_response = wrapped(**arg_extractor.get_openai_args())

        if _is_streaming_response(openai_response):
            return MelodiResponseGeneratorSync(
                openai_resource=openai_resource,
                openai_response=openai_response,
                melodi_client=melodi_client,
                prompt_messages=prompt_messages,
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

    prompt_messages = _get_melodi_messages_from_openai_prompt(kwargs, openai_resource)

    try:
        openai_response = await wrapped(**arg_extractor.get_openai_args())

        if _is_streaming_response(openai_response):
            return MelodiResponseGeneratorAsync(
                openai_resource=openai_resource,
                openai_response=openai_response,
                melodi_client=melodi_client,
                prompt_messages=prompt_messages,
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
            self.melodi_client = MelodiClient(api_key=os.getenv("MELODI_API_KEY"))

        return self.melodi_client

    def register_tracing(self):
        resources = OPENAI_METHODS_V1 if _is_openai_v1() else OPENAI_METHODS_V0

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
