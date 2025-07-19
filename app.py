heyyyyyyyy

from flask import Flask, request, render_template, jsonify
from groq import Groq
from murf import Murf
import os
import time

app = Flask(__name__)
chat_history = []

# Replace with your real API keys
GROQ_API_KEY = "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"
MURF_API_KEY = "ap2_3eefbc94-63bb-4c64-a0df-e8b04f3b8f3a"

groq_client = Groq(api_key=GROQ_API_KEY)
murf_client = Murf(api_key=MURF_API_KEY)

def generate_voice(text):
    try:
        print(f"\n🎤 Generating voice for: {text}")
        res = murf_client.text_to_speech.generate(
            text=text,
            voice_id="en-IN-aarav"
        )
        audio_url = res.audio_file
        print(f"✅ Audio URL: {audio_url}")
        return audio_url  # Stream instead of downloading

    except Exception as e:
        print("❌ Error in generate_voice():", e)
        return None

def get_groq_response(user_input):
    try:
        result = groq_client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": "You're a AI assistant named Bhalu, created by Robert Thomas.Be and do what they says and do accordingly. "},#You're a grammar bot named kunjaayi, created by Robert Thomas. Correct the sentence as its a conversation ,ignore the minute errors like capitalise,full stop ,commas like that in the message and focus on the selection of words, explain in a happy vibe ,be short,motivating and concise
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        reply = result.choices[0].message.content.strip()
        return reply
    except Exception as e:
        print("❌ Groq error:", e)
        return "Sorry, I couldn't process that."

@app.route("/", methods=["GET"])
def home():
    return render_template("chat.html", chat_history=chat_history)

@app.route("/", methods=["POST"])
def chat():
    user_input = request.form.get("user_input", "").strip()
    print(f"\n📥 Received input: {user_input}")
    if not user_input:
        return jsonify(reply="", audio=None)

    reply = get_groq_response(user_input)
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "groq", "content": reply})

    audio_url = generate_voice(reply)
    print(f"🔗 Streaming audio from: {audio_url}")

    return jsonify(reply=reply, audio=audio_url)

@app.route("/reset")
def reset():
    global chat_history
    chat_history = []
    return render_template("chat.html", chat_history=chat_history)

if __name__ == "__main__":
    print("\n🚀 Flask running at http://127.0.0.1:5000")
    app.run(debug=True)
