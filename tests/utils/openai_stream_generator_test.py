import unittest
from dataclasses import dataclass
from typing import Optional
from unittest.mock import patch, MagicMock

from melodi.utils.openai_stream_generator import (
    _extract_streamed_openai_response,
    MelodiResponseGeneratorSync,
)
from melodi.utils.openai_utils import OpenAiDefinition


@dataclass
class ChoiceDeltaToolCallFunction:
    """Testing class which mirrors OpenAI's objects."""

    arguments: str
    name: Optional[str]


@dataclass
class ChoiceDeltaToolCall:
    """Testing class which mirrors OpenAI's objects."""

    index: int
    id: Optional[str]
    function: Optional[ChoiceDeltaToolCallFunction]
    index: Optional[int]
    type: Optional[str]
    logprobs: Optional[list] = None
    content_filter_results: Optional[dict] = None
    finish_reason: Optional[str] = None


@dataclass
class ChoiceDelta:
    """Testing class which mirrors OpenAI's objects."""

    content: Optional[str]
    function_call: Optional[str]
    refusal: Optional[str]
    role: Optional[str]
    tool_calls: Optional[list]


@dataclass
class Choice:
    """Testing class which mirrors OpenAI's objects."""

    delta: ChoiceDelta
    finish_reason: Optional[str]
    index: int
    logprobs: Optional[list]
    content_filter_results: dict


@dataclass
class ChatCompletionChunk:
    """Testing class which mirrors OpenAI's objects."""

    id: str
    choices: Optional[list]
    created: int
    model: Optional[str]
    object: Optional[str]
    service_tier: Optional[str]
    system_fingerprint: Optional[str]
    usage: Optional[dict]
    prompt_filter_results: Optional[list] = None


class TestOpenAIStreamExtractorTests(unittest.TestCase):

    openai_mock_response_function_call = [
        ChatCompletionChunk(
            id="",
            choices=[],
            created=0,
            model="",
            object="",
            service_tier=None,
            system_fingerprint=None,
            usage=None,
            prompt_filter_results=[
                {
                    "prompt_index": 0,
                    "content_filter_results": {
                        "hate": {"filtered": False, "severity": "safe"},
                        "jailbreak": {"filtered": False, "detected": False},
                        "self_harm": {"filtered": False, "severity": "safe"},
                        "sexual": {"filtered": False, "severity": "safe"},
                        "violence": {"filtered": False, "severity": "safe"},
                    },
                }
            ],
        ),
        ChatCompletionChunk(
            id="chatcmpl-BbYEdy7cBIbJsbLXouL7Z47t93LUR",
            choices=[
                Choice(
                    delta=ChoiceDelta(
                        content=None,
                        function_call=None,
                        refusal=None,
                        role="assistant",
                        tool_calls=[
                            ChoiceDeltaToolCall(
                                index=0,
                                id="call_nuMz0OzAFocR9il88r5794xN",
                                function=ChoiceDeltaToolCallFunction(
                                    arguments="", name="get_current_weather"
                                ),
                                type="function",
                            )
                        ],
                    ),
                    finish_reason=None,
                    index=0,
                    logprobs=None,
                    content_filter_results={},
                )
            ],
            created=1748289435,
            model="gpt-4.1-2025-04-14",
            object="chat.completion.chunk",
            service_tier=None,
            system_fingerprint="fp_07e970ab25",
            usage=None,
        ),
        ChatCompletionChunk(
            id="chatcmpl-BbYEdy7cBIbJsbLXouL7Z47t93LUR",
            choices=[
                Choice(
                    delta=ChoiceDelta(
                        content=None,
                        function_call=None,
                        refusal=None,
                        role=None,
                        tool_calls=[
                            ChoiceDeltaToolCall(
                                index=0,
                                id=None,
                                function=ChoiceDeltaToolCallFunction(
                                    arguments='{"', name=None
                                ),
                                type=None,
                            )
                        ],
                    ),
                    finish_reason=None,
                    index=0,
                    logprobs=None,
                    content_filter_results={},
                )
            ],
            created=1748289435,
            model="gpt-4.1-2025-04-14",
            object="chat.completion.chunk",
            service_tier=None,
            system_fingerprint="fp_07e970ab25",
            usage=None,
        ),
        ChatCompletionChunk(
            id="chatcmpl-BbYEdy7cBIbJsbLXouL7Z47t93LUR",
            choices=[
                Choice(
                    delta=ChoiceDelta(
                        content=None,
                        function_call=None,
                        refusal=None,
                        role=None,
                        tool_calls=[
                            ChoiceDeltaToolCall(
                                index=0,
                                id=None,
                                function=ChoiceDeltaToolCallFunction(
                                    arguments="location", name=None
                                ),
                                type=None,
                            )
                        ],
                    ),
                    finish_reason=None,
                    index=0,
                    logprobs=None,
                    content_filter_results={},
                )
            ],
            created=1748289435,
            model="gpt-4.1-2025-04-14",
            object="chat.completion.chunk",
            service_tier=None,
            system_fingerprint="fp_07e970ab25",
            usage=None,
        ),
        ChatCompletionChunk(
            id="chatcmpl-BbYEdy7cBIbJsbLXouL7Z47t93LUR",
            choices=[
                Choice(
                    delta=ChoiceDelta(
                        content=None,
                        function_call=None,
                        refusal=None,
                        role=None,
                        tool_calls=[
                            ChoiceDeltaToolCall(
                                index=0,
                                id=None,
                                function=ChoiceDeltaToolCallFunction(
                                    arguments='":"', name=None
                                ),
                                type=None,
                            )
                        ],
                    ),
                    finish_reason=None,
                    index=0,
                    logprobs=None,
                    content_filter_results={},
                )
            ],
            created=1748289435,
            model="gpt-4.1-2025-04-14",
            object="chat.completion.chunk",
            service_tier=None,
            system_fingerprint="fp_07e970ab25",
            usage=None,
        ),
        ChatCompletionChunk(
            id="chatcmpl-BbYEdy7cBIbJsbLXouL7Z47t93LUR",
            choices=[
                Choice(
                    delta=ChoiceDelta(
                        content=None,
                        function_call=None,
                        refusal=None,
                        role=None,
                        tool_calls=[
                            ChoiceDeltaToolCall(
                                index=0,
                                id=None,
                                function=ChoiceDeltaToolCallFunction(
                                    arguments="Paris", name=None
                                ),
                                type=None,
                            )
                        ],
                    ),
                    finish_reason=None,
                    index=0,
                    logprobs=None,
                    content_filter_results={},
                )
            ],
            created=1748289435,
            model="gpt-4.1-2025-04-14",
            object="chat.completion.chunk",
            service_tier=None,
            system_fingerprint="fp_07e970ab25",
            usage=None,
        ),
        ChatCompletionChunk(
            id="chatcmpl-BbYEdy7cBIbJsbLXouL7Z47t93LUR",
            choices=[
                Choice(
                    delta=ChoiceDelta(
                        content=None,
                        function_call=None,
                        refusal=None,
                        role=None,
                        tool_calls=[
                            ChoiceDeltaToolCall(
                                index=0,
                                id=None,
                                function=ChoiceDeltaToolCallFunction(
                                    arguments='"}', name=None
                                ),
                                type=None,
                            )
                        ],
                    ),
                    finish_reason=None,
                    index=0,
                    logprobs=None,
                    content_filter_results={},
                )
            ],
            created=1748289435,
            model="gpt-4.1-2025-04-14",
            object="chat.completion.chunk",
            service_tier=None,
            system_fingerprint="fp_07e970ab25",
            usage=None,
        ),
        ChatCompletionChunk(
            id="chatcmpl-BbYEdy7cBIbJsbLXouL7Z47t93LUR",
            choices=[
                Choice(
                    delta=ChoiceDelta(
                        content=None,
                        function_call=None,
                        refusal=None,
                        role=None,
                        tool_calls=None,
                    ),
                    finish_reason="tool_calls",
                    index=0,
                    logprobs=None,
                    content_filter_results={},
                )
            ],
            created=1748289435,
            model="gpt-4.1-2025-04-14",
            object="chat.completion.chunk",
            service_tier=None,
            system_fingerprint="fp_07e970ab25",
            usage=None,
        ),
    ]

    openai_mock_response = [
        ChatCompletionChunk(
            id="",
            choices=[],
            created=0,
            model="",
            object="",
            service_tier=None,
            system_fingerprint=None,
            usage=None,
            prompt_filter_results=[
                {
                    "prompt_index": 0,
                    "content_filter_results": {
                        "hate": {"filtered": False, "severity": "safe"},
                        "jailbreak": {"filtered": False, "detected": False},
                        "self_harm": {"filtered": False, "severity": "safe"},
                        "sexual": {"filtered": False, "severity": "safe"},
                        "violence": {"filtered": False, "severity": "safe"},
                    },
                }
            ],
        ),
        ChatCompletionChunk(
            id="chatcmpl-BbWigtG2AjFsEEXkAzbBlmiAL8sfz",
            choices=[
                Choice(
                    delta=ChoiceDelta(
                        content="",
                        function_call=None,
                        refusal=None,
                        role="assistant",
                        tool_calls=None,
                    ),
                    finish_reason=None,
                    index=0,
                    logprobs=None,
                    content_filter_results={},
                )
            ],
            created=1748283610,
            model="o4-mini-2025-04-16",
            object="chat.completion.chunk",
            service_tier=None,
            system_fingerprint=None,
            usage=None,
        ),
        ChatCompletionChunk(
            id="chatcmpl-BbWigtG2AjFsEEXkAzbBlmiAL8sfz",
            choices=[
                Choice(
                    delta=ChoiceDelta(
                        content="this",
                        function_call=None,
                        refusal=None,
                        role=None,
                        tool_calls=None,
                    ),
                    finish_reason=None,
                    index=0,
                    logprobs=None,
                    content_filter_results={
                        "hate": {"filtered": False, "severity": "safe"},
                        "self_harm": {"filtered": False, "severity": "safe"},
                        "sexual": {"filtered": False, "severity": "safe"},
                        "violence": {"filtered": False, "severity": "safe"},
                    },
                )
            ],
            created=1748283610,
            model="o4-mini-2025-04-16",
            object="chat.completion.chunk",
            service_tier=None,
            system_fingerprint=None,
            usage=None,
        ),
        ChatCompletionChunk(
            id="chatcmpl-BbWigtG2AjFsEEXkAzbBlmiAL8sfz",
            choices=[
                Choice(
                    delta=ChoiceDelta(
                        content=" is",
                        function_call=None,
                        refusal=None,
                        role=None,
                        tool_calls=None,
                    ),
                    finish_reason=None,
                    index=0,
                    logprobs=None,
                    content_filter_results={
                        "hate": {"filtered": False, "severity": "safe"},
                        "self_harm": {"filtered": False, "severity": "safe"},
                        "sexual": {"filtered": False, "severity": "safe"},
                        "violence": {"filtered": False, "severity": "safe"},
                    },
                )
            ],
            created=1748283610,
            model="o4-mini-2025-04-16",
            object="chat.completion.chunk",
            service_tier=None,
            system_fingerprint=None,
            usage=None,
        ),
        ChatCompletionChunk(
            id="chatcmpl-BbWigtG2AjFsEEXkAzbBlmiAL8sfz",
            choices=[
                Choice(
                    delta=ChoiceDelta(
                        content=" meant",
                        function_call=None,
                        refusal=None,
                        role=None,
                        tool_calls=None,
                    ),
                    finish_reason=None,
                    index=0,
                    logprobs=None,
                    content_filter_results={
                        "hate": {"filtered": False, "severity": "safe"},
                        "self_harm": {"filtered": False, "severity": "safe"},
                        "sexual": {"filtered": False, "severity": "safe"},
                        "violence": {"filtered": False, "severity": "safe"},
                    },
                )
            ],
            created=1748283610,
            model="o4-mini-2025-04-16",
            object="chat.completion.chunk",
            service_tier=None,
            system_fingerprint=None,
            usage=None,
        ),
        ChatCompletionChunk(
            id="chatcmpl-BbWigtG2AjFsEEXkAzbBlmiAL8sfz",
            choices=[
                Choice(
                    delta=ChoiceDelta(
                        content=" to",
                        function_call=None,
                        refusal=None,
                        role=None,
                        tool_calls=None,
                    ),
                    finish_reason=None,
                    index=0,
                    logprobs=None,
                    content_filter_results={
                        "hate": {"filtered": False, "severity": "safe"},
                        "self_harm": {"filtered": False, "severity": "safe"},
                        "sexual": {"filtered": False, "severity": "safe"},
                        "violence": {"filtered": False, "severity": "safe"},
                    },
                )
            ],
            created=1748283610,
            model="o4-mini-2025-04-16",
            object="chat.completion.chunk",
            service_tier=None,
            system_fingerprint=None,
            usage=None,
        ),
        ChatCompletionChunk(
            id="chatcmpl-BbWigtG2AjFsEEXkAzbBlmiAL8sfz",
            choices=[
                Choice(
                    delta=ChoiceDelta(
                        content=" be",
                        function_call=None,
                        refusal=None,
                        role=None,
                        tool_calls=None,
                    ),
                    finish_reason=None,
                    index=0,
                    logprobs=None,
                    content_filter_results={
                        "hate": {"filtered": False, "severity": "safe"},
                        "self_harm": {"filtered": False, "severity": "safe"},
                        "sexual": {"filtered": False, "severity": "safe"},
                        "violence": {"filtered": False, "severity": "safe"},
                    },
                )
            ],
            created=1748283610,
            model="o4-mini-2025-04-16",
            object="chat.completion.chunk",
            service_tier=None,
            system_fingerprint=None,
            usage=None,
        ),
        ChatCompletionChunk(
            id="chatcmpl-BbWigtG2AjFsEEXkAzbBlmiAL8sfz",
            choices=[
                Choice(
                    delta=ChoiceDelta(
                        content=" a",
                        function_call=None,
                        refusal=None,
                        role=None,
                        tool_calls=None,
                    ),
                    finish_reason=None,
                    index=0,
                    logprobs=None,
                    content_filter_results={
                        "hate": {"filtered": False, "severity": "safe"},
                        "self_harm": {"filtered": False, "severity": "safe"},
                        "sexual": {"filtered": False, "severity": "safe"},
                        "violence": {"filtered": False, "severity": "safe"},
                    },
                )
            ],
            created=1748283610,
            model="o4-mini-2025-04-16",
            object="chat.completion.chunk",
            service_tier=None,
            system_fingerprint=None,
            usage=None,
        ),
        ChatCompletionChunk(
            id="chatcmpl-BbWigtG2AjFsEEXkAzbBlmiAL8sfz",
            choices=[
                Choice(
                    delta=ChoiceDelta(
                        content=" streamed",
                        function_call=None,
                        refusal=None,
                        role=None,
                        tool_calls=None,
                    ),
                    finish_reason=None,
                    index=0,
                    logprobs=None,
                    content_filter_results={
                        "hate": {"filtered": False, "severity": "safe"},
                        "self_harm": {"filtered": False, "severity": "safe"},
                        "sexual": {"filtered": False, "severity": "safe"},
                        "violence": {"filtered": False, "severity": "safe"},
                    },
                )
            ],
            created=1748283610,
            model="o4-mini-2025-04-16",
            object="chat.completion.chunk",
            service_tier=None,
            system_fingerprint=None,
            usage=None,
        ),
        ChatCompletionChunk(
            id="chatcmpl-BbWigtG2AjFsEEXkAzbBlmiAL8sfz",
            choices=[
                Choice(
                    delta=ChoiceDelta(
                        content=" response",
                        function_call=None,
                        refusal=None,
                        role=None,
                        tool_calls=None,
                    ),
                    finish_reason=None,
                    index=0,
                    logprobs=None,
                    content_filter_results={
                        "hate": {"filtered": False, "severity": "safe"},
                        "self_harm": {"filtered": False, "severity": "safe"},
                        "sexual": {"filtered": False, "severity": "safe"},
                        "violence": {"filtered": False, "severity": "safe"},
                    },
                )
            ],
            created=1748283610,
            model="o4-mini-2025-04-16",
            object="chat.completion.chunk",
            service_tier=None,
            system_fingerprint=None,
            usage=None,
        ),
        ChatCompletionChunk(
            id="chatcmpl-BbWigtG2AjFsEEXkAzbBlmiAL8sfz",
            choices=[
                Choice(
                    delta=ChoiceDelta(
                        content=None,
                        function_call=None,
                        refusal=None,
                        role=None,
                        tool_calls=None,
                    ),
                    finish_reason="stop",
                    index=0,
                    logprobs=None,
                    content_filter_results={},
                )
            ],
            created=1748283610,
            model="o4-mini-2025-04-16",
            object="chat.completion.chunk",
            service_tier=None,
            system_fingerprint=None,
            usage=None,
        ),
    ]

    def test_extract_streamed_openai_response(self):
        melodi_message, response_id = _extract_streamed_openai_response(
            resource=OpenAiDefinition(
                module="openai",
                object="ChatCompletion",
                method="create",
                type="chat",
                sync=True,
            ),
            chunks=[],
        )
        self.assertIsNone(melodi_message)
        self.assertIsNone(response_id)

        melodi_message, response_id = _extract_streamed_openai_response(
            resource=OpenAiDefinition(
                module="openai",
                object="ChatCompletion",
                method="create",
                type="chat",
                sync=True,
            ),
            chunks=self.openai_mock_response,
        )

        self.assertEqual(
            melodi_message.externalId, "chatcmpl-BbWigtG2AjFsEEXkAzbBlmiAL8sfz"
        )
        self.assertEqual(melodi_message.role, "Assistant")
        self.assertEqual(
            melodi_message.content, "this is meant to be a streamed response"
        )
        self.assertEqual(
            melodi_message.metadata,
            {
                "model": "o4-mini-2025-04-16",
                "finish_reason": "stop",
                "created_at": 1748283610,
            },
        )
        self.assertEqual(response_id, "chatcmpl-BbWigtG2AjFsEEXkAzbBlmiAL8sfz")

    def test_extract_streamed_openai_response_function_tools(self):
        melodi_message, response_id = _extract_streamed_openai_response(
            resource=OpenAiDefinition(
                module="openai",
                object="ChatCompletion",
                method="create",
                type="chat",
                sync=True,
            ),
            chunks=self.openai_mock_response_function_call,
        )

        self.assertEqual(
            melodi_message.externalId, "chatcmpl-BbYEdy7cBIbJsbLXouL7Z47t93LUR"
        )
        self.assertEqual(melodi_message.role, "Assistant")
        self.assertEqual(melodi_message.content, "")
        self.assertEqual(
            melodi_message.metadata,
            {
                "model": "gpt-4.1-2025-04-14",
                "finish_reason": "tool_calls",
                "created_at": 1748289435,
                "tool_calls": '[{"name": "get_current_weather", "arguments": "{\\"location\\":\\"Paris\\"}"}]',
            },
        )
        self.assertEqual(response_id, "chatcmpl-BbYEdy7cBIbJsbLXouL7Z47t93LUR")

    @patch("melodi.utils.openai_stream_generator.create_melodi_thread")
    def test_melodi_response_generator_sync(self, mock_melodi_thread):
        melodi_client_mock = MagicMock()
        result = MelodiResponseGeneratorSync(
            openai_resource=OpenAiDefinition(
                module="openai",
                object="ChatCompletion",
                method="create",
                type="chat",
                sync=True,
            ),
            openai_response=[],
            melodi_client=melodi_client_mock,
            prompt_messages=[],
        )
        self.assertEqual(len(mock_melodi_thread.mock_calls), 0)

        for _ in result:
            pass
        self.assertEqual(len(mock_melodi_thread.mock_calls), 1)
        _, _, kwargs = mock_melodi_thread.mock_calls[0]
        self.assertEqual(kwargs["melodi_client"], melodi_client_mock)
        self.assertEqual(kwargs["melodi_messages"], [None])
        self.assertEqual(kwargs["response_id"], None)
        self.assertEqual(kwargs["prompt_messages"], [])

        result = MelodiResponseGeneratorSync(
            openai_resource=OpenAiDefinition(
                module="openai",
                object="ChatCompletion",
                method="create",
                type="chat",
                sync=True,
            ),
            openai_response=self.openai_mock_response,
            melodi_client=melodi_client_mock,
            prompt_messages=[],
        )
        for _ in result:
            pass
        self.assertEqual(len(mock_melodi_thread.mock_calls), 2)
        _, _, kwargs = mock_melodi_thread.mock_calls[1]
        self.assertEqual(kwargs["melodi_client"], melodi_client_mock)
        self.assertEqual(len(kwargs["melodi_messages"]), 1)
        self.assertEqual(
            kwargs["melodi_messages"][0].externalId,
            "chatcmpl-BbWigtG2AjFsEEXkAzbBlmiAL8sfz",
        )
        self.assertEqual(kwargs["melodi_messages"][0].type, "markdown")
        self.assertEqual(kwargs["melodi_messages"][0].role, "Assistant")
        self.assertEqual(
            kwargs["melodi_messages"][0].content,
            "this is meant to be a streamed response",
        )
        self.assertEqual(kwargs["melodi_messages"][0].jsonContent, None)
        self.assertEqual(
            kwargs["melodi_messages"][0].metadata,
            {
                "model": "o4-mini-2025-04-16",
                "finish_reason": "stop",
                "created_at": 1748283610,
            },
        )
        self.assertEqual(
            kwargs["response_id"], "chatcmpl-BbWigtG2AjFsEEXkAzbBlmiAL8sfz"
        )
        self.assertEqual(kwargs["prompt_messages"], [])

    @patch("melodi.utils.openai_stream_generator.create_melodi_thread")
    def test_melodi_response_generator_async(self, mock_melodi_thread):
        melodi_client_mock = MagicMock()
        result = MelodiResponseGeneratorSync(
            openai_resource=OpenAiDefinition(
                module="openai",
                object="ChatCompletion",
                method="create",
                type="chat",
                sync=False,
            ),
            openai_response=[],
            melodi_client=melodi_client_mock,
            prompt_messages=[],
        )
        self.assertEqual(len(mock_melodi_thread.mock_calls), 0)

        for _ in result:
            pass
        self.assertEqual(len(mock_melodi_thread.mock_calls), 1)
        _, _, kwargs = mock_melodi_thread.mock_calls[0]
        self.assertEqual(kwargs["melodi_client"], melodi_client_mock)
        self.assertEqual(kwargs["melodi_messages"], [None])
        self.assertEqual(kwargs["response_id"], None)
        self.assertEqual(kwargs["prompt_messages"], [])

        result = MelodiResponseGeneratorSync(
            openai_resource=OpenAiDefinition(
                module="openai",
                object="ChatCompletion",
                method="create",
                type="chat",
                sync=False,
            ),
            openai_response=self.openai_mock_response,
            melodi_client=melodi_client_mock,
            prompt_messages=[],
        )
        for _ in result:
            pass
        self.assertEqual(len(mock_melodi_thread.mock_calls), 2)
        _, _, kwargs = mock_melodi_thread.mock_calls[1]
        self.assertEqual(kwargs["melodi_client"], melodi_client_mock)
        self.assertEqual(len(kwargs["melodi_messages"]), 1)
        self.assertEqual(
            kwargs["melodi_messages"][0].externalId,
            "chatcmpl-BbWigtG2AjFsEEXkAzbBlmiAL8sfz",
        )
        self.assertEqual(kwargs["melodi_messages"][0].type, "markdown")
        self.assertEqual(kwargs["melodi_messages"][0].role, "Assistant")
        self.assertEqual(
            kwargs["melodi_messages"][0].content,
            "this is meant to be a streamed response",
        )
        self.assertEqual(kwargs["melodi_messages"][0].jsonContent, None)
        self.assertEqual(
            kwargs["melodi_messages"][0].metadata,
            {
                "model": "o4-mini-2025-04-16",
                "finish_reason": "stop",
                "created_at": 1748283610,
            },
        )
        self.assertEqual(
            kwargs["response_id"], "chatcmpl-BbWigtG2AjFsEEXkAzbBlmiAL8sfz"
        )
        self.assertEqual(kwargs["prompt_messages"], [])


if __name__ == "__main__":
    unittest.main()
