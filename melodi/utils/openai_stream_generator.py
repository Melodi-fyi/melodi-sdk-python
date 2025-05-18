from collections import defaultdict

from melodi.melodi_client import MelodiClient
from melodi.messages.data_models import Message
from melodi.utils.openai_utils import (
    OpenAiDefinition,
    clean_dict_value,
    _is_openai_v1,
    parse_metadata_value,
)
from melodi.utils.utils import create_melodi_thread


def _extract_streamed_openai_response(resource: OpenAiDefinition, chunks: list):
    if resource.type == "chat":
        completion = defaultdict(str)
    else:
        completion = {"role": "assistant", "content": ""}
    response_id, model, usage, finish_reason, created_at = None, None, None, None, None

    # TODO this does not solve for the usecase of more than 1 versions being returned
    for chunk in chunks:
        if _is_openai_v1():
            chunk = chunk.__dict__

        model = chunk.get("model")
        response_id = chunk.get("id")
        usage = get_streamed_usage_metadata(chunk.get("usage"))
        created_at = chunk.get("created")

        choices = chunk.get("choices", [])
        for choice in choices:
            if _is_openai_v1():
                choice = choice.__dict__

            if resource.type == "chat":
                delta = choice.get("delta")

                # The finish_reason is included only once, in the final one
                finish_reason = choice.get("finish_reason")

                if _is_openai_v1():
                    delta = delta.__dict__

                # The role is included only once
                if delta.get("role") is not None:
                    completion["role"] = delta["role"]

                # The full content is made out of all the chunk contents
                if delta.get("content") is not None:
                    completion["content"] = (
                        delta.get("content")
                        if completion["content"] is None
                        else completion["content"] + delta.get("content")
                    )
                # TODO this is deprecated
                elif delta.get("function_call") is not None:
                    curr = completion["function_call"]
                    function_call_chunk = delta.get("function_call")

                    if not curr:
                        completion["function_call"] = {
                            "name": getattr(function_call_chunk, "name", ""),
                            "arguments": getattr(function_call_chunk, "arguments", ""),
                        }

                    else:
                        curr["name"] = curr["name"] or getattr(
                            function_call_chunk, "name", None
                        )
                        curr["arguments"] += getattr(
                            function_call_chunk, "arguments", ""
                        )
                elif delta.get("tool_calls") is not None:
                    curr = completion["tool_calls"]
                    tool_call_chunk = getattr(
                        delta.get("tool_calls")[0], "function", None
                    )

                    if not curr:
                        completion["tool_calls"] = [
                            {
                                "name": getattr(tool_call_chunk, "name", ""),
                                "arguments": getattr(tool_call_chunk, "arguments", ""),
                            }
                        ]
                    elif getattr(tool_call_chunk, "name") is not None:
                        curr.append(
                            {
                                "name": getattr(tool_call_chunk, "name", None),
                                "arguments": getattr(
                                    tool_call_chunk, "arguments", None
                                ),
                            }
                        )
                    else:
                        curr[-1]["name"] = curr[-1]["name"] or getattr(
                            tool_call_chunk, "name", None
                        )
                        curr[-1]["arguments"] += getattr(
                            tool_call_chunk, "arguments", None
                        )

            if resource.type == "completion":
                completion["content"] += choice.get("text", "")

    message_metadata = {
        "model": model,
        "usage": usage,
        "finish_reason": finish_reason,
        "created_at": created_at,
        "tool_calls": parse_metadata_value(completion.get("tool_calls")),
    }

    melodi_message = Message(
        externalId=response_id,
        role=completion["role"].title(),
        content=completion["content"],
        metadata=clean_dict_value(message_metadata),
    )

    return melodi_message, response_id


def get_streamed_usage_metadata(usage_dict):
    if not usage_dict:
        return None

    if not isinstance(usage_dict, dict):
        usage_dict = usage_dict.__dict__

    return usage_dict


class MelodiResponseGeneratorSync:
    def __init__(
        self,
        *,
        openai_resource: OpenAiDefinition,
        openai_response,
        melodi_client: MelodiClient,
        prompt_messages: list,
    ):
        self.items = []

        self.openai_resource = openai_resource
        self.openai_response = openai_response
        self.melodi_client = melodi_client
        self.prompt_messages = prompt_messages

    def __iter__(self):
        try:
            for i in self.openai_response:
                self.items.append(i)

                yield i
        finally:
            self._finalize()

    def __next__(self):
        try:
            item = self.openai_response.__next__()
            self.items.append(item)

            return item

        except StopIteration:
            self._finalize()

            raise

    def __enter__(self):
        return self.__iter__()

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def _finalize(self):
        melodi_message, response_id = _extract_streamed_openai_response(
            self.openai_resource, self.items
        )

        create_melodi_thread(
            melodi_client=self.melodi_client,
            melodi_messages=[melodi_message],
            response_id=response_id,
            prompt_messages=self.prompt_messages,
        )


class MelodiResponseGeneratorAsync:
    def __init__(
        self,
        *,
        openai_resource: OpenAiDefinition,
        openai_response,
        melodi_client: MelodiClient,
        prompt_messages: list,
    ):
        self.items = []

        self.openai_resource = openai_resource
        self.openai_response = openai_response
        self.melodi_client = melodi_client
        self.prompt_messages = prompt_messages

    async def __aiter__(self):
        try:
            async for i in self.openai_response:
                self.items.append(i)

                yield i
        finally:
            await self._finalize()

    async def __anext__(self):
        try:
            item = await self.openai_response.__anext__()
            self.items.append(item)

            return item

        except StopAsyncIteration:
            await self._finalize()

            raise

    async def __aenter__(self):
        return self.__aiter__()

    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

    async def _finalize(self):
        melodi_message, response_id = _extract_streamed_openai_response(
            self.openai_resource, self.items
        )

        create_melodi_thread(
            melodi_client=self.melodi_client,
            melodi_messages=[melodi_message],
            response_id=response_id,
            prompt_messages=self.prompt_messages,
        )

    async def close(self) -> None:
        """Close the response and release the connection.

        Automatically called if the response body is read to completion.
        """
        await self.openai_response.close()

    async def aclose(self) -> None:
        """Close the response and release the connection.

        Automatically called if the response body is read to completion.
        """
        await self.openai_response.aclose()
