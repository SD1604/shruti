"""
Wrapper around the Gemini API for chat generation (Synthesizer, Citation
Validator, Query Refiner all call this).
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

_client = None
MODEL = "gemini-3.5-flash-lite"


def get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return _client


def generate_answer(prompt: str) -> str:
    client = get_client()
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )
    return response.text