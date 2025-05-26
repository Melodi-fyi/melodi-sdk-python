import os
import unittest

from melodi.utils.openai import OpenAI, AzureOpenAI, AsyncOpenAI, AsyncAzureOpenAI


class TestOpenAIModules(unittest.TestCase):

    @unittest.skip
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
            model="o4-mini"
        )

    @unittest.skip
    def test_openai_azure_extensive_keys(self):
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
                    "content": "I am going to play basketball for the first time, what should I see?",
                }
            ],
            frequency_penalty=1.4,
            logit_bias={34: 89},
            # logprobs=True,
            max_completion_tokens=5000,
            metadata={"this is": "custom"},
            model="gpt-4o-mini",
            n=2,
            presence_penalty=0.3,
            response_format={"type": "text"},
            seed=1996,
            service_tier="default",
            stop="don't stop me now",
            store=True,
            # top_logprobs=2,
            top_p=0.5,
            user="itsmemario",
        )

    @unittest.skip
    def test_azure_openai_function_tools(self):
        client = AzureOpenAI(
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
        messages = [{"role": "user", "content": "What's the weather like in Boston today?"}]
        completion = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        print(completion)

    @unittest.skip
    def test_logprobs(self):
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_API_KEY"),
            api_version="2024-12-01-preview",
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        )
        completion = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "user", "content": "Hello logprobs!"}
            ],
            logprobs=True,
            top_logprobs=2
        )

    @unittest.skip
    def test_azure_openai_streaming_function_tools(self):
        client = AzureOpenAI(
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

        stream = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": "What's the weather like in Paris today?"}],
            tools=tools,
            stream=True
        )

        for event in stream:
            print(event)
        pass

    @unittest.skip
    def test_openai_azure_stream_response(self):
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_API_KEY"),
            api_version="2025-03-01-preview",
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        )

        stream = client.chat.completions.create(
            model="o4-mini",
            messages=[
                {
                    "role": "user",
                    "content": "Say 'double bubble bath' ten times fast.",
                },
            ],
            stream=True,
            n=1,
        )

        for event in stream:
            # print(event)
            pass
        pass


if __name__ == "__main__":
    unittest.main()
