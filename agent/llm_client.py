"""
A thin wrapper around the Groq API. Keeping this separate (rather than
calling Groq directly inside the Synthesizer node) means if we ever swap
providers later, only this one file needs to change.
"""

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

_client = None


def get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=os.environ["GROQ_API_KEY"])
    return _client


def generate_answer(prompt: str) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content