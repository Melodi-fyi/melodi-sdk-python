import unittest

from melodi.messages.data_models import Message
from melodi.utils.openai_prompt_parser import (
    _process_prompt_message,
    _extract_chat_prompt,
    _get_generation_metadata,
    _get_melodi_messages_from_openai_prompt,
)
from melodi.utils.openai_utils import OpenAiDefinition


class TestOpenAIPromptParserTests(unittest.TestCase):
    def test_process_prompt_message(self):
        self.assertIsNone(_process_prompt_message(None))
        self.assertEqual(_process_prompt_message("test"), "test")
        self.assertEqual(_process_prompt_message({}), {})
        self.assertEqual(
            _process_prompt_message({"content": "test"}), {"content": "test"}
        )
        self.assertEqual(
            _process_prompt_message({"content": "test"}), {"content": "test"}
        )
        self.assertEqual(
            _process_prompt_message(
                {
                    "content": [
                        {"type": "input_audio", "message": "should be ignored"},
                        {"type": "not_audio", "message": "should be added"},
                    ]
                }
            ),
            {
                "content": [
                    {"type": "not_audio", "message": "should be added"},
                ]
            },
        )

    def test_extract_chat_prompt(self):
        self.assertEqual(_extract_chat_prompt({}), {"messages": []})
        self.assertEqual(_extract_chat_prompt({"messages": []}), {"messages": []})
        self.assertEqual(
            _extract_chat_prompt(
                {
                    "messages": [
                        {
                            "content": [
                                {"type": "not_audio", "message": "should be added"},
                            ]
                        }
                    ]
                }
            ),
            {
                "messages": [
                    {
                        "content": [
                            {"type": "not_audio", "message": "should be added"},
                        ]
                    }
                ]
            },
        )
        self.assertEqual(
            _extract_chat_prompt({"messages": ["hello"]}),
            {"messages": ["hello"]},
        )
        # TODO add unit tests for function_calls, functions, tools

    def test_get_generation_metadata(self):
        self.assertEqual(
            _get_generation_metadata({}),
            {
                "frequency_penalty": 0,
                "logprobs": False,
                "n": 1,
                "parallel_tool_calls": True,
                "presence_penalty": 0,
                "reasoning_effort": "medium",
                "service_tier": "auto",
                "store": False,
                "stream": False,
                "temperature": 1,
                "top_p": 1,
            },
        )

        self.assertEqual(
            _get_generation_metadata({"logprobs": True, "other_key": False, "n": 4}),
            {
                "frequency_penalty": 0,
                "logprobs": True,
                "n": 4,
                "parallel_tool_calls": True,
                "presence_penalty": 0,
                "reasoning_effort": "medium",
                "service_tier": "auto",
                "store": False,
                "stream": False,
                "temperature": 1,
                "top_p": 1,
            },
        )

    def test_get_melodi_messages_from_openai_prompt(self):
        self.assertEqual(
            _get_melodi_messages_from_openai_prompt(
                kwargs={},
                openai_resource=OpenAiDefinition(
                    module="openai",
                    object="Completion",
                    method="create",
                    type="completion",
                    sync=True,
                ),
            ),
            [],
        )
        self.assertEqual(
            _get_melodi_messages_from_openai_prompt(
                kwargs={},
                openai_resource=OpenAiDefinition(
                    module="openai",
                    object="Completion",
                    method="create",
                    type="test",
                    sync=True,
                ),
            ),
            [],
        )
        self.assertEqual(
            _get_melodi_messages_from_openai_prompt(
                kwargs={"prompt": {}},
                openai_resource=OpenAiDefinition(
                    module="openai",
                    object="Completion",
                    method="create",
                    type="completion",
                    sync=True,
                ),
            ),
            [],
        )

        self.assertEqual(
            _get_melodi_messages_from_openai_prompt(
                kwargs={
                    "prompt": {
                        "messages": [{"role": "test_role", "content": "Hello World"}]
                    }
                },
                openai_resource=OpenAiDefinition(
                    module="openai",
                    object="Completion",
                    method="create",
                    type="completion",
                    sync=True,
                ),
            ),
            [
                Message(
                    externalId=f"input_0",
                    role="Test_Role",
                    content="Hello World",
                    metadata={
                        "type": "input_message",
                        "frequency_penalty": 0,
                        "logprobs": 0,
                        "n": 1,
                        "parallel_tool_calls": 1,
                        "presence_penalty": 0,
                        "reasoning_effort": "medium",
                        "service_tier": "auto",
                        "store": 0,
                        "stream": 0,
                        "temperature": 1,
                        "top_p": 1,
                    },
                )
            ],
        ),

        self.assertEqual(
            _get_melodi_messages_from_openai_prompt(
                kwargs={
                    "prompt": {
                        "messages": [{"role": "test_role", "content": "Hello World"}, {"role": "system", "content": "Hello World Back"}]
                    },
                    "temperature": 4
                },
                openai_resource=OpenAiDefinition(
                    module="openai",
                    object="Completion",
                    method="create",
                    type="completion",
                    sync=True,
                ),
            ),
            [
                Message(
                    externalId=f"input_0",
                    role="Test_Role",
                    content="Hello World",
                    metadata={
                        "type": "input_message",
                        "frequency_penalty": 0,
                        "logprobs": 0,
                        "n": 1,
                        "parallel_tool_calls": 1,
                        "presence_penalty": 0,
                        "reasoning_effort": "medium",
                        "service_tier": "auto",
                        "store": 0,
                        "stream": 0,
                        "temperature": 4,
                        "top_p": 1,
                    },
                ),
                Message(
                    externalId=f"input_1",
                    role="System",
                    content="Hello World Back",
                    metadata={
                        "type": "input_message",
                        "frequency_penalty": 0,
                        "logprobs": 0,
                        "n": 1,
                        "parallel_tool_calls": 1,
                        "presence_penalty": 0,
                        "reasoning_effort": "medium",
                        "service_tier": "auto",
                        "store": 0,
                        "stream": 0,
                        "temperature": 4,
                        "top_p": 1,
                    },
                )
            ],
        )

        self.assertEqual(
            _get_melodi_messages_from_openai_prompt(
                kwargs={
                    "prompt": {
                        "messages": [{"role": "test_role", "content": "Hello World"},
                                     {"role": "system", "content": "Hello World Back"}]
                    },
                    "temperature": 4
                },
                openai_resource=OpenAiDefinition(
                    module="openai",
                    object="Completion",
                    method="create",
                    type="chat",
                    sync=True,
                ),
            ),
            [],
        )

        self.assertEqual(
            _get_melodi_messages_from_openai_prompt(
                kwargs={
                    "messages": [
                        {"role": "test_role", "content": "Hello World"},
                        {"role": "system", "content": "Hello World Back"}
                    ],
                    "temperature": 4,
                    "frequency_penalty": 2,
                },
                openai_resource=OpenAiDefinition(
                    module="openai",
                    object="Completion",
                    method="create",
                    type="chat",
                    sync=True,
                ),
            ),
            [
                Message(
                    externalId=f"input_0",
                    role="Test_Role",
                    content="Hello World",
                    metadata={
                        "type": "input_message",
                        "frequency_penalty": 2,
                        "logprobs": 0,
                        "n": 1,
                        "parallel_tool_calls": 1,
                        "presence_penalty": 0,
                        "reasoning_effort": "medium",
                        "service_tier": "auto",
                        "store": 0,
                        "stream": 0,
                        "temperature": 4,
                        "top_p": 1,
                    },
                ),
                Message(
                    externalId=f"input_1",
                    role="System",
                    content="Hello World Back",
                    metadata={
                        "type": "input_message",
                        "frequency_penalty": 2,
                        "logprobs": 0,
                        "n": 1,
                        "parallel_tool_calls": 1,
                        "presence_penalty": 0,
                        "reasoning_effort": "medium",
                        "service_tier": "auto",
                        "store": 0,
                        "stream": 0,
                        "temperature": 4,
                        "top_p": 1,
                    },
                )
            ],
        )


if __name__ == "__main__":
    unittest.main()
