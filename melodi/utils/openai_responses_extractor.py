"""
OpenAI Responses API response extractor for Melodi integration.
"""

from melodi.messages.data_models import Message
from melodi.utils.openai_utils import (
    RESPONSE_MESSAGE_KEYS,
    RESPONSE_OUTPUT_MESSAGE_KEYS,
    RESPONSE_USAGE_KEYS,
    OpenAiDefinition,
    parse_metadata_value,
)
from melodi.utils.utils import create_melodi_thread, handle_melodi_failure


@handle_melodi_failure("Could not create a Melodi thread from Responses API")
def create_melodi_thread_from_responses_response(
    openai_resource: OpenAiDefinition,
    openai_response,
    melodi_client,
    prompt_messages: list,
):
    """Create a Melodi thread from a Responses API response."""
    melodi_messages, response_id = _get_melodi_messages_from_responses_response(
        resource=openai_resource, response=openai_response
    )
    create_melodi_thread(
        melodi_client=melodi_client,
        melodi_messages=melodi_messages,
        response_id=response_id,
        prompt_messages=prompt_messages,
    )


def _get_melodi_messages_from_responses_response(resource: OpenAiDefinition, response):
    """Extract Melodi messages from a Responses API response."""
    if response is None:
        return [], None

    response_dict = _to_dict(response)

    # Extract output messages from the response
    output_items = response_dict.get("output", [])
    response_contents = []

    for output_item in output_items:
        output_item_dict = _to_dict(output_item)
        output_type = output_item_dict.get("type", "")

        if output_type == "message":
            # Standard message output
            response_contents.append(_extract_responses_message(output_item_dict))
        elif output_type in ["web_search_call", "file_search_call", "function_call"]:
            # Tool calls - we can log these as metadata
            response_contents.append(_extract_tool_call(output_item_dict))
        elif output_type == "reasoning_item":
            # Reasoning traces from o1-style models
            response_contents.append(_extract_reasoning_item(output_item_dict))
        # Add more output types as needed

    # If no message outputs, create a summary from output_text
    if not response_contents and response_dict.get("output_text"):
        response_contents = [
            {"content": response_dict.get("output_text"), "role": "assistant"}
        ]

    response_metadata = _get_responses_metadata(response_dict)

    melodi_messages = []
    for message_dict in response_contents:
        if len(response_contents) > 1:
            id_suffix = f"-output-{len(melodi_messages)}"
        else:
            id_suffix = ""

        content = message_dict.pop("content", None)
        metadata = {"type": "response"}
        metadata.update(**message_dict)
        metadata.update(**response_metadata)

        melodi_messages.append(
            Message(
                externalId=f"{metadata.get('id', 'response')}{id_suffix}",
                role=metadata.get("role", "assistant").title(),
                content=content,
                metadata=metadata,
            )
        )

    return melodi_messages, response_dict.get("id")


def _extract_responses_message(output_item: dict):
    """Extract message content from a Responses API message output."""
    message_data = {}

    # Extract basic message info
    for key in RESPONSE_OUTPUT_MESSAGE_KEYS:
        value = output_item.get(key)
        if value is not None:
            message_data[key] = parse_metadata_value(value)

    # Extract content from the content array
    content_items = output_item.get("content", [])
    content_parts = []

    for content_item in content_items:
        content_item_dict = _to_dict(content_item)
        content_type = content_item_dict.get("type", "")

        if content_type == "output_text":
            text = content_item_dict.get("text", "")
            if text:
                content_parts.append(text)
        elif content_type == "output_audio":
            # Handle audio output
            content_parts.append("[Audio response]")
        elif content_type == "output_image":
            # Handle image output
            content_parts.append("[Image response]")
        # Add more content types as needed

    message_data["content"] = " ".join(content_parts) if content_parts else ""
    return message_data


def _extract_tool_call(output_item: dict):
    """Extract tool call information for logging."""
    tool_data = {
        "content": f"[Tool call: {output_item.get('type', 'unknown')}]",
        "role": "assistant",
        "tool_type": output_item.get("type"),
        "tool_status": output_item.get("status"),
    }

    # Add tool-specific information
    if output_item.get("type") == "web_search_call":
        tool_data["content"] = "[Web search performed]"
    elif output_item.get("type") == "file_search_call":
        tool_data["content"] = "[File search performed]"
    elif output_item.get("type") == "function_call":
        function_name = output_item.get("name", "unknown")
        tool_data["content"] = f"[Function call: {function_name}]"
        tool_data["function_name"] = function_name

    return tool_data


def _extract_reasoning_item(output_item: dict):
    """Extract reasoning traces from o1-style models."""
    reasoning_data = {
        "content": "[Reasoning trace]",
        "role": "assistant",
        "reasoning_type": output_item.get("type"),
    }

    # Extract reasoning content if available
    content = output_item.get("content", "")
    if content:
        reasoning_data["content"] = f"[Reasoning: {content[:100]}...]"

    return reasoning_data


def _get_responses_metadata(response: dict):
    """Extract metadata from a Responses API response."""
    metadata = {}

    # Extract top-level response metadata
    for key in RESPONSE_MESSAGE_KEYS:
        value = response.get(key)
        if value is not None:
            metadata[key] = parse_metadata_value(value)

    # Extract usage information
    usage_dict = _to_dict(response.get("usage", {}))
    for key in RESPONSE_USAGE_KEYS:
        value = usage_dict.get(key)
        if value is not None:
            metadata[key] = parse_metadata_value(value)

    # Extract usage details if available
    usage_details = usage_dict.get("output_tokens_details", {})
    if usage_details:
        for key, value in usage_details.items():
            if value is not None:
                metadata[f"output_tokens_{key}"] = parse_metadata_value(value)

    return metadata


def _to_dict(input_value):
    """Convert input to dictionary format."""
    if input_value is None:
        return None

    if isinstance(input_value, dict):
        return input_value

    # Handle Pydantic models and other objects with __dict__
    if hasattr(input_value, "__dict__"):
        return input_value.__dict__

    # Handle objects with model_dump method (Pydantic v2)
    if hasattr(input_value, "model_dump"):
        return input_value.model_dump()

    # Handle objects with dict method (Pydantic v1)
    if hasattr(input_value, "dict"):
        return input_value.dict()

    # Fallback for other types
    return {"value": str(input_value)}
