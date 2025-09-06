from flask import Flask, request, jsonify, render_template
from utils.openRouter import call_openrouter
from utils.memory import get_user_profile,save_memory, get_recent_memories
from utils.tone import detect_tone
import uuid


app = Flask("STANVERSE-FUTURE-AI")


# ---------------- Home route ----------------


@app.route("/")
def index():
    return render_template("chat-bot-ui.html")

# ---------------- Chat route ----------------


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_id = data.get("user_id")
        user_message = data.get("message")
        if not user_id:
            user_id = str(uuid.uuid4())
        #print(user_id)
        # Fetch user profile and recent memories
        user_profile = get_user_profile(user_id)
        user_profile_data = {k: v for k, v in user_profile.items() if k != '_id'}
        memory_summary = get_recent_memories(user_id)
        tone = detect_tone(user_message)
        system_prompt = "You are STANVERSE FUTURE AI — a supportive best friend. Stay natural and empathetic."
        # Prepare LLM messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": (
                f"Profile: {user_profile_data}\n"
                f"Memory: {memory_summary}\nTone: {tone}\nUser: \"{user_message}\""
            )}
        ]

        # Call OpenRouter LLM
        response = call_openrouter(messages, temperature=0.9, usage=True)
        content = response["choices"][0]["message"]["content"]
        # Save memory
        save_memory(user_id, user_message, content, tone)

        return jsonify({"reply": content, "tone": tone, "user_id": user_id})
    except Exception as e:
        print("error",e)
        return jsonify({"reply": "I hit wall. Please try after some time", "tone": "", "user_id": user_id})


# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run()
