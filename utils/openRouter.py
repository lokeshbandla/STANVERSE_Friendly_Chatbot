import requests, json
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = os.getenv("OPENROUTER_API_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

def call_openrouter(messages: list, temperature: float = 0.9, usage: bool = False) -> dict:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": temperature,
        "max_tokens":1200
    }
    if usage:
        payload["usage"] = {"include": True}
    resp = requests.post(API_URL, headers=headers, json=payload,verify=False)
    return resp.json()
