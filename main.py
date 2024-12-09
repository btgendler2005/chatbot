
import os
import openai

# Set your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

client = openai.OpenAI(
    api_key=openai.api_key, 
)

assistant = client.beta.assistants.create(
    name="Sports Assistant",
    instructions="You are a personal sports assistant. Write and run code to answer sports related questions for someone who has minimal sports knowledge.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4",
)

thread = client.beta.threads.create()

# Take user input
name = input("Please enter your name: ")
user_input = input("Please enter your sports related question: ")

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=user_input,
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as {name}. The user has a premium account.",
)


if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)

    for message in messages:
        assert message.content[0].type == "text"
        if message.role == "assistant":
            print(str({message.content[0].text.value}).encode('utf8').decode('unicode_escape').replace('}', '').replace('{', ''))
    client.beta.assistants.delete(assistant.id)