from ..data_models import ExternalUser, Log, LogInput, LogOutput, Message


def log_object_from_open_ai_messages_response(messages_response, project_id: int, external_user: ExternalUser = None, metadata: dict = {}) -> Log:
  messages = messages_response.data

  input_messages = []
  for index, message in enumerate(messages):
      if index == 0:
          thread_id = message.thread_id
          output_message = Message(
              externalId=message.id,
              role=message.role,
              content=message.content[0].text.value,
          )
      else:
          input_messages.append(
              Message(
                  externalId=message.id,
                  role=message.role,
                  content=message.content[0].text.value,
              )
          )

  log = Log(
      projectId=project_id,
      externalThreadId=thread_id,

      input=LogInput(
          type="messages",
          messages=input_messages,
      ),
      output=LogOutput(
          type="message",
          message=output_message,
      ),

      metadata=metadata,

      externalUser=external_user,
  )

  return log