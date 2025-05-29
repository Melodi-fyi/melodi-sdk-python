import unittest
from unittest.mock import patch

from melodi.messages.data_models import Message
from melodi.utils.openai_nonstream_extractor import (
    _get_response_metadata,
    _extract_chat_base_response,
    _get_melodi_messages_from_openai_response, create_melodi_thread_from_openai_response,
)
from melodi.utils.openai_utils import OpenAiDefinition


class TestOpenAINonstreamExtractorTests(unittest.TestCase):
    def test_get_response_metadata(self):
        self.assertEqual(_get_response_metadata({}), {})
        self.assertEqual(
            _get_response_metadata(
                {
                    "usage": {
                        "completion_tokens_details": {
                            "accepted_prediction_tokens": 12,
                            "reasoning_tokens": 34,
                            "rejected_prediction_tokens": 2,
                        },
                        "prompt_tokens_details": {
                            "cached_tokens": 1,
                        },
                        "total_tokens": 67,
                    },
                    "created": 1234,
                    "id": 1111,
                    "model": "openai-mini-v12",
                    "object": "text",
                    "service_tier": "pro",
                    "system_fingerprint": 123,
                }
            ),
            {
                "accepted_prediction_tokens": 12,
                "reasoning_tokens": 34,
                "rejected_prediction_tokens": 2,
                "cached_tokens": 1,
                "total_tokens": 67,
                "created": 1234,
                "id": 1111,
                "model": "openai-mini-v12",
                "object": "text",
                "service_tier": "pro",
                "system_fingerprint": 123,
            },
        )
        self.assertEqual(
            _get_response_metadata(
                {
                    "usage": {
                        "completion_tokens_details": {
                            "reasoning_tokens": 34,
                            "rejected_prediction_tokens": 0,
                        },
                        "prompt_tokens_details": {
                            "cached_tokens": 1,
                        },
                        "total_tokens": 67,
                    },
                    "created": 1234,
                    "id": 1111,
                    "model": "openai-mini-v12",
                    "object": "text",
                    "service_tier": "pro",
                    "system_fingerprint": 123,
                }
            ),
            {
                "reasoning_tokens": 34,
                "rejected_prediction_tokens": 0,
                "cached_tokens": 1,
                "total_tokens": 67,
                "created": 1234,
                "id": 1111,
                "model": "openai-mini-v12",
                "object": "text",
                "service_tier": "pro",
                "system_fingerprint": 123,
            },
        )

    def test_extract_chat_base_response(self):
        self.assertEqual(_extract_chat_base_response("test"), {"content": "test"})

    def test_get_melodi_messages_from_openai_response(self):
        messages, message_id = _get_melodi_messages_from_openai_response(None, None)
        self.assertEqual(messages, [])
        self.assertEqual(message_id, None)

        messages, message_id = _get_melodi_messages_from_openai_response(
            resource=OpenAiDefinition(
                module="openai",
                object="ChatCompletion",
                method="create",
                type="chat",
                sync=True,
            ),
            response=None,
        )
        self.assertEqual(messages, [])
        self.assertEqual(message_id, None)

        messages, message_id = _get_melodi_messages_from_openai_response(
            resource=OpenAiDefinition(
                module="openai",
                object="ChatCompletion",
                method="create",
                type="chat",
                sync=True,
            ),
            response={},
        )
        self.assertEqual(messages, [])
        self.assertEqual(message_id, None)

        messages, message_id = _get_melodi_messages_from_openai_response(
            resource=OpenAiDefinition(
                module="openai",
                object="ChatCompletion",
                method="create",
                type="chat",
                sync=True,
            ),
            response={
                "choices": [
                    {
                        "message": {
                            "content": "Hi",
                            "refusal": None,
                            "role": "new role",
                        },
                        "finish_reason": "stop",
                        "index": 0,
                        "logprobs": [],
                    }
                ],
                "id": "message_1",
            },
        )
        self.assertEqual(
            messages,
            [
                Message(
                    externalId="message_1",
                    role="New Role",
                    content="Hi",
                    jsonContent=None,
                    metadata={
                        "id": "message_1",
                        "type": "response",
                        "role": "new role",
                        "finish_reason": "stop",
                        "index": 0,
                        "logprobs": "[]",
                    },
                )
            ],
        )
        self.assertEqual(message_id, "message_1")

    @patch("melodi.utils.openai_nonstream_extractor.create_melodi_thread")
    def test_create_melodi_thread_from_openai_response(self, melodi_patch):
        create_melodi_thread_from_openai_response(
            openai_resource=None,
            openai_response=None,
            melodi_client=None,
            prompt_messages=[]
        )
        _, _, kwargs = melodi_patch.mock_calls[0]
        self.assertEqual(
            kwargs,
            {
                "melodi_client": None,
                "melodi_messages": [],
                "response_id": None,
                "prompt_messages": [],
            }
        )

        create_melodi_thread_from_openai_response(
            openai_resource=OpenAiDefinition(
                module="openai",
                object="ChatCompletion",
                method="create",
                type="chat",
                sync=True,
            ),
            openai_response={
                "choices": [
                    {
                        "message": {
                            "content": "Hi",
                            "refusal": None,
                            "role": "new role",
                        },
                        "finish_reason": "stop",
                        "index": 0,
                        "logprobs": [],
                    }
                ],
                "id": "message_1",
            },
            melodi_client=None,
            prompt_messages=[]
        )
        _, _, kwargs = melodi_patch.mock_calls[1]
        self.assertEqual(
            kwargs,
            {
                "melodi_client": None,
                "melodi_messages": [
                    Message(
                        externalId="message_1",
                        role="New Role",
                        content="Hi",
                        jsonContent=None,
                        metadata={
                            "id": "message_1",
                            "type": "response",
                            "role": "new role",
                            "finish_reason": "stop",
                            "index": 0,
                            "logprobs": "[]",
                        },
                    )
                ],
                "response_id": "message_1",
                "prompt_messages": [],
            }
        )


if __name__ == "__main__":
    unittest.main()
