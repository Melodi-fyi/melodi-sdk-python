#!/usr/bin/env python3
"""
Example: Using OpenAI Responses API with Melodi Logging

This example demonstrates how to use the newer OpenAI Responses API
with automatic Melodi logging.
"""

import asyncio
import os

from melodi.utils.openai import openai


def basic_responses_example():
    """Basic example using the Responses API."""
    print("=== Basic Responses API Example ===")

    # Simple text input
    response = openai.responses.create(
        model="gpt-4o-mini",
        input="Explain quantum computing in one sentence.",
    )

    print(f"Response: {response.output_text}")
    print(f"Response ID: {response.id}")
    print(f"Tokens used: {response.usage.total_tokens if response.usage else 'N/A'}")


def multimodal_example():
    """Example with multimodal input and tools."""
    print("\n=== Multimodal + Tools Example ===")

    response = openai.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "What's the latest news about AI?"},
                ],
            }
        ],
        tools=[{"type": "web_search"}],
    )

    print(f"Response: {response.output_text[:200]}...")
    print(f"Number of output items: {len(response.output)}")

    # Show tool usage
    for item in response.output:
        if hasattr(item, "type"):
            print(f"Output type: {item.type}")


def streaming_example():
    """Example with streaming responses."""
    print("\n=== Streaming Example ===")

    stream = openai.responses.create(
        model="gpt-4o-mini",
        input="Write a short poem about programming.",
        stream=True,
    )

    print("Streaming response: ", end="", flush=True)
    for event in stream:
        if hasattr(event, "type") and event.type == "response.text.delta":
            print(event.delta, end="", flush=True)
    print()  # New line after streaming


async def async_example():
    """Example with async/await."""
    print("\n=== Async Example ===")

    # Create async client
    async_client = openai.AsyncOpenAI()

    response = await async_client.responses.create(
        model="gpt-4o-mini",
        input="What are the benefits of async programming?",
    )

    print(f"Async response: {response.output_text}")


def reasoning_example():
    """Example with reasoning models."""
    print("\n=== Reasoning Model Example ===")

    try:
        response = openai.responses.create(
            model="o4-mini",  # Reasoning model
            input="Solve this step by step: If a train travels 60 mph for 2.5 hours, how far does it go?",
            reasoning={"effort": "medium"},
        )

        print(f"Reasoning response: {response.output_text}")

        # Check if reasoning trace is available
        for item in response.output:
            if hasattr(item, "type") and item.type == "reasoning_item":
                print("Reasoning trace captured in Melodi")
                break
    except Exception as e:
        print(f"Reasoning model not available: {e}")


def main():
    """Run all examples."""
    print("OpenAI Responses API + Melodi Examples")
    print("=" * 50)

    # Check environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not set - examples will fail")
    if not os.getenv("MELODI_API_KEY"):
        print("⚠️  MELODI_API_KEY not set - logging will fail")

    try:
        basic_responses_example()
        multimodal_example()
        streaming_example()

        # Run async example
        asyncio.run(async_example())

        reasoning_example()

        print("\n✅ All examples completed!")
        print("Check your Melodi dashboard to see the logged conversations.")

    except Exception as e:
        print(f"❌ Example failed: {e}")
        print("Make sure you have valid API keys set in your environment.")


if __name__ == "__main__":
    main()
