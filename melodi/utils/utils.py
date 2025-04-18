import logging
import os

from melodi.threads.data_models import Thread
from melodi.utils.openai_utils import time_now

logger = logging.getLogger("melodi")


def handle_melodi_failure(value):
    def decorate(wrapped_func):
        def applicator(*args, **kwargs):
            try:
                return wrapped_func(*args, **kwargs)
            except Exception as e:
                logger.error(f"{value}: {repr(e)}")
                return

        return applicator

    return decorate


@handle_melodi_failure("Could not create a Melodi thread")
def create_melodi_thread(melodi_client, melodi_messages, response_id, prompt_messages):
    logger.info("Creating Melodi thread ...")
    thread_metadata = {
        "created": time_now(as_string=True),
        "response_id": response_id,
    }
    # Create Melodi thread
    thread = Thread(
        projectId=os.getenv("MELODI_PROJECT_ID"),
        externalId=response_id,
        messages=prompt_messages + melodi_messages,
        metadata=thread_metadata,
    )
    melodi_client.threads.create(thread)
    logger.info("Done creating Melodi thread.")


@handle_melodi_failure("Could not create a Melodi thread")
def create_error_melodi_thread(melodi_client, prompt_messages, model, exception):
    logger.warning("Creating Melodi error thread ...")
    metadata = {
        "completion_tokens": 0,
        "prompt_tokens": 0,
        "total_tokens": 0,
        "openai_error": exception,
        "created": time_now(as_string=True),
    }
    if model:
        metadata["model"] = model
    melodi_error_thread = Thread(
        projectId=os.getenv("MELODI_PROJECT_ID"),
        messages=prompt_messages,
        metadata=metadata,
    )
    melodi_client.threads.create(melodi_error_thread)
    logger.warning("Done creating Melodi error thread.")
