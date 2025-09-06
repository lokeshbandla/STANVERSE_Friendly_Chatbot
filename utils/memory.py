import json
from pymongo import MongoClient
from datetime import datetime
import os


client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]

users_col = db["users"]
memories_col = db["memories"]

def get_user_profile(user_id: str) -> dict:
    user = users_col.find_one({"user_id": user_id})
    if not user:
        user = {
            "user_id": user_id,
            "interests": [],
            "favorites": {},
            "last_emotion": "neutral",
            "created_at": datetime.utcnow()
        }
        users_col.insert_one(user)
    return user

def update_user_profile(user_id: str, updates: dict):
    users_col.update_one({"user_id": user_id}, {"$set": updates}, upsert=True)

def save_memory(user_id: str, user_message: str, reply: str, emotion: str):
    memories_col.insert_one({
        "user_id": user_id,
        "text": user_message,
        "reply": reply,
        "emotion": emotion,
        "timestamp": datetime.utcnow()
    })
    users_col.update_one({"user_id": user_id}, {"$set": {"last_emotion": emotion}})

def get_recent_memories(user_id: str, limit: int = 100) -> str:
    chats = memories_col.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
    return " | ".join([f"({c['emotion']}) {c['text']}" for c in chats])
