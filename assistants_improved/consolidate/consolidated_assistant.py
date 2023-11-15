import json
import openai
import os
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]


def show_json(obj):
    print(json.loads(obj.model_dump_json()))


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Upload the file
file = client.files.create(
    file=open(
        "docs/2023q3-alphabet-earnings-release.pdf",
        "rb",
    ),
    purpose="assistants",
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


function_get_current_whether = {
    "name": "get_current_weather",
    "description": "Get the current weather in a given location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA",
            },
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["location"],
    },
}

# create Assistant
assistant = client.beta.assistants.create(
    name="consolidated assistant",
    instructions="You are an expert in function calling and extracting information."
                 "Use the provided functions to answer questions."
                 "You can also use the retrieval tool to find information."
                 "You can also use the code interpreter to run code.",
    tools=[
        {"type": "code_interpreter"},
        {"type": "retrieval"},
        {"type": "function",
         "function": function_get_current_whether},
    ],
    model="gpt-4-1106-preview",
    file_ids=[file.id],
)

ASSISTANT_ID = assistant.id


def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )


def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(ASSISTANT_ID, thread, user_input)
    return thread, run


def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()


def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(5)
    return run


# function calling assistant
thread, run = create_thread_and_run(
    "What's the weather in San Francisco?"
)


def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")


run = wait_on_run(run, thread)
pretty_print(get_response(thread))

# retrieval assistant
thread, run = create_thread_and_run(
    "What is Deepmind working on?"
)


def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")


run = wait_on_run(run, thread)
pretty_print(get_response(thread))


# code interpreter assistant
thread, run = create_thread_and_run(
    "I need to solve the equation `3x + 11 = 14`. Can you help me?"
)


def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

run = wait_on_run(run, thread)
pretty_print(get_response(thread))
