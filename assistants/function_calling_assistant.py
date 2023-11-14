import openai
import os
import time
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]

#  tools : Code Interpreter, Retrieval, and Function calling
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def get_current_weather(location, unit="fahrenheit"):
    print('get current weather called')
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": location, "temperature": "10", "unit": "celsius"})
    elif "san francisco" in location.lower():
        return json.dumps({"location": location, "temperature": "72", "unit": "fahrenheit"})
    else:
        return json.dumps({"location": location, "temperature": "22", "unit": "celsius"})


def getNickname(location):
    print('get nickname called')
    """Get the nickname of a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": location, "nickname": "The Big Sushi"})
    elif "san francisco" in location.lower():
        return json.dumps({"location": location, "nickname": "The Golden City"})
    else:
        return json.dumps({"location": location, "nickname": "The Big Apple"})


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

time.sleep(20)

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
