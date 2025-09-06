def detect_tone(user_message: str) -> str:
    msg = user_message.lower()
    if any(word in msg for word in ["sad", "down", "tired", "lonely"]):
        return "empathetic"
    elif any(word in msg for word in ["joke", "funny", "lol", "roast"]):
        return "playful"
    elif any(word in msg for word in ["angry", "mad", "hate"]):
        return "calm-supportive"
    else:
        return "friendly"
