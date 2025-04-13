import os
import unittest
from unittest import IsolatedAsyncioTestCase

from melodi.utils.openai import OpenAI, AzureOpenAI, AsyncOpenAI, AsyncAzureOpenAI


class TestOpenAIModules(unittest.TestCase):

    def test_openai_azure(self):
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_API_KEY"),
            api_version="2024-12-01-preview",
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        )

        response = client.chat.completions.create(
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
            model="o3-mini"
        )

        # print(response)
        pass

    def test_openai_azure_stream_response(self):
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_API_KEY"),
            api_version="2025-03-01-preview",
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        )

        stream = client.chat.completions.create(
            model="o3-mini",
            messages=[
                {
                    "role": "user",
                    "content": "Say 'double bubble bath' ten times fast.",
                },
            ],
            stream=True,
            n=1,
            logprobs=True,
            presence_penalty=1,
        )

        for event in stream:
            # print(event)
            pass
        pass


class Test(IsolatedAsyncioTestCase):

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
                    "content": "You are a helpful async assistant and it is the 31st of March 2025.",
                },
                {
                    "role": "user",
                    "content": "I am going to Munich, what should I see?",
                }
            ],
            max_completion_tokens=5000,
            model="o3-mini"
        )

        # print(response)
        pass

    async def test_openai_azure_stream_response(self):
        client = AsyncAzureOpenAI(
            api_key=os.getenv("AZURE_API_KEY"),
            api_version="2025-03-01-preview",
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        )

        stream = await client.chat.completions.create(
            model="o3-mini",
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
        pass


if __name__ == "__main__":
    unittest.main()
