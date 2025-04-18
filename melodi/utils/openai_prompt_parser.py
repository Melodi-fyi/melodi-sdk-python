from openai import NotGiven

from melodi.messages.data_models import Message
from melodi.utils.openai_utils import (
    GENERATION_PARAMETERS_DEFAULTS,
    parse_metadata_value,
    OpenAiDefinition,
)


def _get_melodi_messages_from_openai_prompt(
    kwargs: dict, openai_resource: OpenAiDefinition
):
    """Convert the OpenAI prompt in Melodi messages."""
    if openai_resource.type == "completion":
        prompt = kwargs.get("prompt", {})
    elif openai_resource.type == "chat":
        prompt = _extract_chat_prompt(kwargs)
    else:
        # Currently only chat and completion objects are supported
        return []

    if not prompt.get("messages"):
        return []

    generation_metadata = _get_generation_metadata(kwargs)

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
                content=message["content"],
                metadata=message_metadata,
            )
        )

    return melodi_messages


def _get_generation_metadata(kwargs: dict):
    """Accessed 3/31/25: https://platform.openai.com/docs/api-reference/chat/create"""
    generation_metadata = dict()
    for key_param, key_default_value in GENERATION_PARAMETERS_DEFAULTS.items():
        value = kwargs.get(key_param)

        if value is None or isinstance(value, NotGiven):
            if key_default_value is not None:
                generation_metadata[key_param] = key_default_value
        else:
            generation_metadata[key_param] = parse_metadata_value(value)

    return generation_metadata


def _extract_chat_prompt(kwargs: dict):
    """Return prompt messages and potential function calls for the prompt."""
    prompt = dict()

    for key in ["function_call", "functions", "tools"]:
        if not kwargs.get(key):
            continue

        prompt[key] = parse_metadata_value(kwargs.get(key))

    prompt_messages = [
        _process_prompt_message(message) for message in kwargs.get("messages", [])
    ]
    prompt["messages"] = prompt_messages
    return prompt


def _process_prompt_message(message):
    if not isinstance(message, dict):
        return message

    processed_message = {**message}

    content = processed_message.get("content")
    if not isinstance(content, list):
        return processed_message

    processed_content = []

    for content_part in content:
        if content_part.get("type") == "input_audio":
            # Not supported
            pass
        else:
            processed_content.append(content_part)

    processed_message["content"] = processed_content

    return processed_message
