"""
OpenAI Responses API prompt parser for Melodi integration.
"""

from openai import NotGiven

from melodi.messages.data_models import Message
from melodi.utils.openai_utils import (
    GENERATION_PARAMETERS_DEFAULTS,
    OpenAiDefinition,
    parse_metadata_value,
)
from melodi.utils.utils import handle_melodi_failure


@handle_melodi_failure("Could not parse OpenAI Responses API prompt attributes")
def get_melodi_messages_from_responses_prompt(
    kwargs: dict, openai_resource: OpenAiDefinition
):
    """Convert the OpenAI Responses API prompt to Melodi messages."""
    if openai_resource.type != "response":
        return []

    prompt = _extract_responses_prompt(kwargs)

    if not prompt.get("messages"):
        return []

    generation_metadata = _get_responses_generation_metadata(kwargs)

    prompt_messages = prompt.pop("messages")
    message_metadata = {
        "type": "input_message",
    }
    message_metadata.update(**prompt)
    message_metadata.update(**generation_metadata)

    melodi_messages = []
    for message in prompt_messages:
        melodi_messages.append(
            Message(
                externalId=f"input_{len(melodi_messages)}",
                role=message["role"].title(),
                content=_extract_message_content(message["content"]),
                metadata=message_metadata,
            )
        )

    return melodi_messages


def _extract_responses_prompt(kwargs: dict):
    """Extract prompt information from Responses API kwargs."""
    prompt = dict()

    # Extract tools, instructions, and other metadata
    for key in ["tools", "instructions", "reasoning", "metadata"]:
        if not kwargs.get(key):
            continue
        prompt[key] = parse_metadata_value(kwargs.get(key))

    # Handle input parameter which can be string or list of messages
    input_param = kwargs.get("input")
    if isinstance(input_param, str):
        # Simple string input
        prompt_messages = [{"role": "user", "content": input_param}]
    elif isinstance(input_param, list):
        # List of message objects
        prompt_messages = [
            _process_responses_message(message) for message in input_param
        ]
    else:
        prompt_messages = []

    prompt["messages"] = prompt_messages
    return prompt


def _process_responses_message(message):
    """Process a single message from the Responses API input."""
    if not isinstance(message, dict):
        return message

    processed_message = {**message}

    # Handle different content formats in Responses API
    content = processed_message.get("content")
    if isinstance(content, list):
        # Multi-modal content (text, images, etc.)
        processed_content = []
        for content_part in content:
            if isinstance(content_part, dict):
                # Handle different content types
                content_type = content_part.get("type", "")
                if content_type in ["input_text", "text"]:
                    processed_content.append(content_part.get("text", ""))
                elif content_type in ["input_image", "image_url"]:
                    # Store image reference for metadata
                    processed_content.append(
                        f"[Image: {content_part.get('image_url', 'unknown')}]"
                    )
                elif content_type in ["input_audio", "audio"]:
                    # Store audio reference for metadata
                    processed_content.append("[Audio content]")
                else:
                    # Other content types
                    processed_content.append(str(content_part))
            else:
                processed_content.append(str(content_part))

        processed_message["content"] = " ".join(processed_content)
    elif isinstance(content, str):
        # Simple string content
        processed_message["content"] = content
    else:
        # Fallback for other content types
        processed_message["content"] = str(content) if content else ""

    return processed_message


def _extract_message_content(content):
    """Extract content from a message, handling various formats."""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        # Join multiple content parts
        return " ".join(str(part) for part in content if part)
    else:
        return str(content) if content else ""


def _get_responses_generation_metadata(kwargs: dict):
    """Extract generation metadata from Responses API kwargs."""
    generation_metadata = dict()

    # Responses API specific parameters
    responses_params = {
        "model": None,
        "temperature": 1.0,
        "top_p": 1.0,
        "max_output_tokens": None,
        "stream": False,
        "store": True,
        "parallel_tool_calls": True,
        "tool_choice": "auto",
        "background": False,
        "service_tier": "auto",
        "truncation": "auto",
        "user": None,
    }

    for key_param, key_default_value in responses_params.items():
        value = kwargs.get(key_param)

        if value is None or isinstance(value, NotGiven):
            if key_default_value is not None:
                generation_metadata[key_param] = key_default_value
        else:
            generation_metadata[key_param] = parse_metadata_value(value)

    # Also include traditional generation parameters for compatibility
    for key_param, key_default_value in GENERATION_PARAMETERS_DEFAULTS.items():
        if key_param not in generation_metadata:
            value = kwargs.get(key_param)
            if value is None or isinstance(value, NotGiven):
                if key_default_value is not None:
                    generation_metadata[key_param] = key_default_value
            else:
                generation_metadata[key_param] = parse_metadata_value(value)

    return generation_metadata
