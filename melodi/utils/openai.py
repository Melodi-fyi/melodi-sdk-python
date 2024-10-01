from melodi.messages.data_models import Message
from melodi.threads.data_models import Thread
from melodi.users.data_models import User


def thread_object_from_open_ai_messages_response(messages_response, project_id: int, user: User = None, metadata: dict = {}) -> Thread:
  messages = messages_response.data

  melodi_messages = []
  for index, message in enumerate(messages):
    if (index == 0):
      thread_id = message.thread_id
    melodi_messages.append(
        Message(
            externalId=message.id,
            role=message.role,
            content=message.content[0].text.value,
        )
    )

  melodi_messages.reverse()

  thread = Thread(
      projectId=project_id,
      externalId=thread_id,
      messages=melodi_messages,
      metadata=metadata,
      externalUser=user,
  )

  return thread