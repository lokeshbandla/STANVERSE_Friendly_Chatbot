import requests, json
from pathlib import Path

with open(Path(__file__).parent.parent / "config.json") as f:
    config = json.load(f)

API_KEY = config["OPENROUTER_API_KEY"]
API_URL = config["OPENROUTER_API_URL"]
MODEL_NAME = config["MODEL_NAME"]

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
    resp = requests.post(API_URL, headers=headers, json=payload)
    return resp.json()
