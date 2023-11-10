import openai
import os
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]

# st.header("OpenAI Code Interpreter Assistant! ")

#  tools : Code Interpreter, Retrieval, and Function calling
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

assistant = client.beta.assistants.create(
    instructions="You are a weather bot. Use the provided functions to answer questions.",
    model="gpt-4-1106-preview",
    tools=[{
        "type": "function",
        "function": {
            "name": "getCurrentWeather",
            "description": "Get the weather in location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
                    "unit": {"type": "string", "enum": ["c", "f"]}
                },
                "required": ["location"]
            }
        }
    }, {
        "type": "function",
        "function": {
            "name": "getNickname",
            "description": "Get the nickname of a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
                },
                "required": ["location"]
            }
        }
    }]
)

thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "What's the weather in San Francisco?",
        }
    ]
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe. The user has a premium account."
)

time.sleep(60)

run_steps = client.beta.threads.runs.steps.list(
    thread_id=thread.id,
    run_id=run.id
)

if run_steps.data[0].status == "completed":
    print("The run was successful!")
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    for message in messages.data:
        role = message.role.upper()
        content = message.content[0].text.value
        print(f"{role}: {content}")