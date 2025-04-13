from melodi.messages.data_models import Message
from melodi.utils.openai_utils import (
    OpenAiDefinition,
    _is_openai_v1,
    COMPLETION_CHOICE_MESSAGE_KEYS,
    COMPLETION_CHOICE_KEYS,
    COMPLETION_USAGE_KEYS,
    COMPLETION_USAGE_TOKENS_KEYS,
    COMPLETION_USAGE_PROMPT_TOKENS_KEYS,
)
from melodi.utils.utils import create_melodi_thread


def create_melodi_thread_from_openai_response(
    openai_resource: OpenAiDefinition,
    openai_response,
    melodi_client,
    prompt_messages: list,
):
    melodi_messages, response_id = _get_melodi_messages_from_openai_response(
        openai_resource,
        (openai_response and openai_response.__dict__)
        if _is_openai_v1()
        else openai_response,
    )
    create_melodi_thread(
        melodi_client=melodi_client,
        melodi_messages=melodi_messages,
        response_id=response_id,
        prompt_messages=prompt_messages,
    )


def _get_melodi_messages_from_openai_response(resource: OpenAiDefinition, response):
    if response is None:
        return [], None

    response_contents = []
    if resource.type == "completion":
        choices = response.get("choices", [])
        if len(choices) > 0:
            choice = choices[-1]
            response_contents = (
                [_extract_chat_base_response(choice.text)]
                if _is_openai_v1()
                else [_extract_chat_base_response(choice.get("text"))]
            )
    elif resource.type == "chat":
        choices = response.get("choices", [])
        # If multiple choices were generated, we'll show all of them in the UI as a list.
        if len(choices) >= 1:
            response_contents = [
                _extract_chat_response(choice.__dict__)
                if _is_openai_v1()
                else _extract_chat_base_response(choice.get("message"))
                for choice in choices
            ]

    response_metadata = _get_response_metadata(response)
    melodi_messages = []
    for message_dict in response_contents:
        content = message_dict.pop("content")
        metadata = {"type": "response"}
        metadata.update(**message_dict)
        metadata.update(**response_metadata)

        melodi_messages.append(
            Message(
                externalId=metadata.get("id"),
                role=metadata.get("role").title(),
                content=content,
                metadata=metadata,
            )
        )
    return melodi_messages, response.get("id")


def _extract_chat_base_response(content: str):
    """Extracts the content from the response."""
    return {
        "content": content,
    }


def _extract_chat_response(choice_dict: dict):
    """Extracts the message content from an OpenAI choice."""
    message_dict = choice_dict.get("message", {}).__dict__
    if not message_dict:
        return {}

    response = {}
    for message_key in COMPLETION_CHOICE_MESSAGE_KEYS:
        value = message_dict.get(message_key)
        if not value:
            continue

        response[message_key] = value

    for choice_key in COMPLETION_CHOICE_KEYS:
        value = choice_dict.get(choice_key)
        if not value:
            continue

        response[choice_key] = value
    return response


def _get_response_metadata(response):
    # TODO extract this
    response_keys = [
        "created",
        "id",
        "model",
        "object",
        "service_tier",
        "system_fingerprint",
    ]

    usage_dict = response.get("usage", {}).__dict__
    completion_tokens_dict = usage_dict.get("completion_tokens_details", {}).__dict__
    prompt_tokens_dict = usage_dict.get("prompt_tokens_details", {}).__dict__

    metadata = {}
    for key in response_keys:
        value = response.get(key)
        if not value:
            continue

        metadata[key] = value

    for key in COMPLETION_USAGE_KEYS:
        value = usage_dict.get(key)
        if not value:
            continue

        metadata[key] = value

    for key in COMPLETION_USAGE_TOKENS_KEYS:
        value = completion_tokens_dict.get(key)
        if not value:
            continue

        metadata[key] = value

    for key in COMPLETION_USAGE_PROMPT_TOKENS_KEYS:
        value = prompt_tokens_dict.get(key)
        if not value:
            continue

        metadata[key] = value

    return metadata
