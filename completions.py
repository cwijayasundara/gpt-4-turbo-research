import openai
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]

print(openai.api_key)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "What are some of the key events that happened in Janurary 2023?",
        }
    ],
    model="gpt-4-1106-preview",
)

print(completion.choices[0].message.content)

#  gpt-3.5-turbo-1106 does not know details on 2023 so the below are hallucinations
completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "What are some of the key events that happened Janurary 2023 for New Zealand Prime Minister "
                       "Jacinda Ardern?",
        }
    ],
    model="gpt-3.5-turbo-1106",
)

print(completion.choices[0].message.content)


