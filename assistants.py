import openai
import os
from dotenv import load_dotenv
from openai import OpenAI
import time

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]

print(openai.api_key)

#  tools : Code Interpreter, Retrieval, and Function calling
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Step 1: Create an Assistant
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview"
)

# Step 2: Create a thread
thread = client.beta.threads.create()

# Step 3: Add a Message to a Thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)

# Step 4: Run the Assistant

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe. The user has a premium account."
)

# Step 5: Display the Assistant's Response
run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
)

time.sleep(10)

messages = client.beta.threads.messages.list(
    thread_id=thread.id
)
print("answer to the first question is ", messages.data[0].content)

# Step 6: Add another Message to a Thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `5x + 10 = 40`. Can you help me? "
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe. The user has a premium account."
)

run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
)

time.sleep(10)

messages = client.beta.threads.messages.list(
    thread_id=thread.id
)
print("answer to the 2nd question is ", messages.data[0].content)
