"""
OpenAI Responses API streaming generator for Melodi integration.
"""

import logging

from melodi.utils.openai_utils import OpenAiDefinition
from melodi.utils.utils import create_melodi_thread, handle_melodi_failure

logger = logging.getLogger("melodi")


class MelodiResponsesGeneratorSync:
    """Synchronous streaming generator for Responses API."""

    def __init__(
        self,
        openai_resource: OpenAiDefinition,
        openai_response,
        melodi_client,
        prompt_messages: list,
    ):
        self.openai_resource = openai_resource
        self.openai_response = openai_response
        self.melodi_client = melodi_client
        self.prompt_messages = prompt_messages
        self.collected_events = []
        self.response_id = None
        self.final_response = None

    def __iter__(self):
        return self

    def __next__(self):
        try:
            event = next(self.openai_response)
            self._process_event(event)
            return event
        except StopIteration:
            # Stream ended, create Melodi thread
            self._create_melodi_thread_from_stream()
            raise

    def _process_event(self, event):
        """Process a streaming event and collect relevant data."""
        self.collected_events.append(event)

        # Extract response ID if available
        if hasattr(event, "response_id") and event.response_id:
            self.response_id = event.response_id
        elif hasattr(event, "id") and event.id:
            self.response_id = event.id

    @handle_melodi_failure("Could not create Melodi thread from Responses stream")
    def _create_melodi_thread_from_stream(self):
        """Create a Melodi thread from collected streaming events."""
        if not self.collected_events:
            return

        # Reconstruct response from events
        response_data = self._reconstruct_response_from_events()

        if response_data:
            from melodi.utils.openai_responses_extractor import (
                _get_melodi_messages_from_responses_response,
            )

            melodi_messages, response_id = _get_melodi_messages_from_responses_response(
                resource=self.openai_resource, response=response_data
            )

            create_melodi_thread(
                melodi_client=self.melodi_client,
                melodi_messages=melodi_messages,
                response_id=response_id or self.response_id,
                prompt_messages=self.prompt_messages,
            )

    def _reconstruct_response_from_events(self):
        """Reconstruct a complete response from streaming events."""
        response_data = {
            "id": self.response_id,
            "object": "response",
            "output": [],
            "usage": {},
        }

        current_message = None
        current_content = ""

        for event in self.collected_events:
            event_type = getattr(event, "type", "")

            if event_type == "response.created":
                # Response started
                if hasattr(event, "response"):
                    response_data.update(self._event_to_dict(event.response))

            elif event_type == "response.output_item.added":
                # New output item started
                if hasattr(event, "output_item"):
                    current_message = self._event_to_dict(event.output_item)
                    current_content = ""

            elif event_type == "response.text.delta":
                # Text content delta
                if hasattr(event, "delta"):
                    current_content += event.delta

            elif event_type == "response.text.done":
                # Text content completed
                if current_message:
                    if "content" not in current_message:
                        current_message["content"] = []
                    current_message["content"].append(
                        {"type": "output_text", "text": current_content}
                    )

            elif event_type == "response.output_item.done":
                # Output item completed
                if current_message:
                    response_data["output"].append(current_message)
                    current_message = None

            elif event_type == "response.done":
                # Response completed
                if hasattr(event, "response"):
                    response_data.update(self._event_to_dict(event.response))

        # Add any remaining message
        if current_message:
            if current_content:
                if "content" not in current_message:
                    current_message["content"] = []
                current_message["content"].append(
                    {"type": "output_text", "text": current_content}
                )
            response_data["output"].append(current_message)

        return response_data

    def _event_to_dict(self, obj):
        """Convert event object to dictionary."""
        if obj is None:
            return {}

        if isinstance(obj, dict):
            return obj

        # Handle Pydantic models and other objects
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        elif hasattr(obj, "dict"):
            return obj.dict()
        elif hasattr(obj, "__dict__"):
            return obj.__dict__
        else:
            return {"value": str(obj)}


class MelodiResponsesGeneratorAsync:
    """Asynchronous streaming generator for Responses API."""

    def __init__(
        self,
        openai_resource: OpenAiDefinition,
        openai_response,
        melodi_client,
        prompt_messages: list,
    ):
        self.openai_resource = openai_resource
        self.openai_response = openai_response
        self.melodi_client = melodi_client
        self.prompt_messages = prompt_messages
        self.collected_events = []
        self.response_id = None

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            event = await self.openai_response.__anext__()
            self._process_event(event)
            return event
        except StopAsyncIteration:
            # Stream ended, create Melodi thread
            await self._create_melodi_thread_from_stream()
            raise

    def _process_event(self, event):
        """Process a streaming event and collect relevant data."""
        self.collected_events.append(event)

        # Extract response ID if available
        if hasattr(event, "response_id") and event.response_id:
            self.response_id = event.response_id
        elif hasattr(event, "id") and event.id:
            self.response_id = event.id

    @handle_melodi_failure("Could not create Melodi thread from async Responses stream")
    async def _create_melodi_thread_from_stream(self):
        """Create a Melodi thread from collected streaming events."""
        if not self.collected_events:
            return

        # Reconstruct response from events
        response_data = self._reconstruct_response_from_events()

        if response_data:
            from melodi.utils.openai_responses_extractor import (
                _get_melodi_messages_from_responses_response,
            )

            melodi_messages, response_id = _get_melodi_messages_from_responses_response(
                resource=self.openai_resource, response=response_data
            )

            create_melodi_thread(
                melodi_client=self.melodi_client,
                melodi_messages=melodi_messages,
                response_id=response_id or self.response_id,
                prompt_messages=self.prompt_messages,
            )

    def _reconstruct_response_from_events(self):
        """Reconstruct a complete response from streaming events."""
        # Same logic as sync version
        response_data = {
            "id": self.response_id,
            "object": "response",
            "output": [],
            "usage": {},
        }

        current_message = None
        current_content = ""

        for event in self.collected_events:
            event_type = getattr(event, "type", "")

            if event_type == "response.created":
                if hasattr(event, "response"):
                    response_data.update(self._event_to_dict(event.response))

            elif event_type == "response.output_item.added":
                if hasattr(event, "output_item"):
                    current_message = self._event_to_dict(event.output_item)
                    current_content = ""

            elif event_type == "response.text.delta":
                if hasattr(event, "delta"):
                    current_content += event.delta

            elif event_type == "response.text.done":
                if current_message:
                    if "content" not in current_message:
                        current_message["content"] = []
                    current_message["content"].append(
                        {"type": "output_text", "text": current_content}
                    )

            elif event_type == "response.output_item.done":
                if current_message:
                    response_data["output"].append(current_message)
                    current_message = None

            elif event_type == "response.done":
                if hasattr(event, "response"):
                    response_data.update(self._event_to_dict(event.response))

        # Add any remaining message
        if current_message:
            if current_content:
                if "content" not in current_message:
                    current_message["content"] = []
                current_message["content"].append(
                    {"type": "output_text", "text": current_content}
                )
            response_data["output"].append(current_message)

        return response_data

    def _event_to_dict(self, obj):
        """Convert event object to dictionary."""
        if obj is None:
            return {}

        if isinstance(obj, dict):
            return obj

        # Handle Pydantic models and other objects
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        elif hasattr(obj, "dict"):
            return obj.dict()
        elif hasattr(obj, "__dict__"):
            return obj.__dict__
        else:
            return {"value": str(obj)}
