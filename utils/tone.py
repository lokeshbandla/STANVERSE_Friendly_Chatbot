def detect_tone(user_message: str) -> str:
    """
    Detects user's emotional tone based on keywords.
    Returns one of: empathetic, playful, calm-supportive, hyped, friendly
    """
    msg = user_message.lower()

    # 🎭 Tone dictionaries
    sad_words = ["sad", "down", "tired", "lonely",
                 "depressed", "upset", "bored", "cry", "broken"]
    playful_words = ["joke", "funny", "lol", "roast",
                     "haha", "lmao", "prank", "meme", "banter"]
    angry_words = ["angry", "mad", "hate",
                   "annoyed", "furious", "pissed", "rage"]
    hype_words = ["excited", "hyped", "awesome", "amazing",
                  "great", "fantastic", "let’s go", "woohoo", "victory"]
    casual_words = ["hey", "hi", "hello",
                    "what’s up", "sup", "yo", "ok", "cool"]

    # 🔎 Intensity detection
    if any(word in msg for word in sad_words):
        if "very" in msg or "really" in msg or "so" in msg:
            return "deep-empathetic"
        return "empathetic"

    elif any(word in msg for word in playful_words):
        return "playful"

    elif any(word in msg for word in angry_words):
        if "very" in msg or "really" in msg or "so" in msg:
            return "de-escalating"
        return "calm-supportive"

    elif any(word in msg for word in hype_words):
        return "hyped"

    elif any(word in msg for word in casual_words):
        return "casual"

    # 🟢 Default
    return "friendly"
