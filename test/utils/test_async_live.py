import os
import unittest
from unittest import IsolatedAsyncioTestCase

from melodi.utils.openai import AsyncAzureOpenAI


class TestAsyncWrapper(IsolatedAsyncioTestCase):

    @unittest.skip
    async def test_openai_azure_async(self):
        client = AsyncAzureOpenAI(
            api_key=os.getenv("AZURE_API_KEY"),
            api_version="2024-12-01-preview",
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        )

        response = await client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": "I am going to Paris, what should I see?",
                }
            ],
            max_completion_tokens=5000,
            model="o4-mini"
        )

    @unittest.skip
    async def test_openai_azure_stream_response(self):
        client = AsyncAzureOpenAI(
            api_key=os.getenv("AZURE_API_KEY"),
            api_version="2025-03-01-preview",
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        )

        stream = await client.chat.completions.create(
            model="o4-mini",
            messages=[
                {
                    "role": "user",
                    "content": "Say 'double bubble bath' 5 times fast.",
                },
            ],
            stream=True,
            n=1,
        )

        async for event in stream:
            # print(event)
            pass

    @unittest.skip
    async def test_azure_openai_streaming_function_tools(self):
        client = AsyncAzureOpenAI(
            api_key=os.getenv("AZURE_API_KEY"),
            api_version="2025-03-01-preview",
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        )

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
                    },
                }
            }
        ]

        stream = await client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": "What's the weather like in Brussels today?"}],
            tools=tools,
            stream=True
        )

        async for event in stream:
            pass

    # @unittest.skip
    async def test_azure_openai_function_tools(self):
        client = AsyncAzureOpenAI(
            api_key=os.getenv("AZURE_API_KEY"),
            api_version="2024-12-01-preview",
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        )

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
                    },
                }
            }
        ]
        messages = [{"role": "user", "content": "What's the weather like in Athens today?"}]
        completion = await client.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )


if __name__ == "__main__":
    unittest.main()
