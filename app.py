import os
import sys
import webbrowser
from datetime import datetime
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")

# Setup Gemini AI
API_KEY = os.getenv("GOOGLE_API_KEY")
gemini_model = None

def init_gemini(api_key=None):
    global gemini_model
    key = api_key or os.getenv("GOOGLE_API_KEY")
    if key:
        try:
            genai.configure(api_key=key)
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.95,
                "max_output_tokens": 1024,
            }
            gemini_model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                system_instruction="You are Alice, a highly intelligent, polite, and concise AI voice assistant. Keep answers brief, natural, engaging, and easy to speak out loud."
            )
            return True
        except Exception as e:
            print(f"[Error] Gemini Init Error: {e}")
            return False
    return False

init_gemini()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/config", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        data = request.json or {}
        new_key = data.get("api_key", "").strip()
        if new_key:
            success = init_gemini(new_key)
            return jsonify({"success": success, "message": "API key updated successfully." if success else "Invalid API Key."})
        return jsonify({"success": False, "message": "No key provided."})
    
    return jsonify({"has_api_key": gemini_model is not None})

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_message = data.get("message", "").strip()
    history = data.get("history", [])

    if not user_message:
        return jsonify({"reply": "Please provide a valid message."}), 400

    query = user_message.lower()

    # Special Command Shortcuts
    if "date" in query or "time" in query or "day" in query:
        now = datetime.now()
        time_str = now.strftime("%I:%M %p on %A, %B %d, %Y")
        return jsonify({"reply": f"It is currently {time_str}.", "action": None})

    if "open youtube" in query:
        webbrowser.open("https://www.youtube.com")
        return jsonify({"reply": "Opening YouTube for you.", "action": "open_url", "url": "https://www.youtube.com"})
    
    if "open google" in query:
        webbrowser.open("https://www.google.com")
        return jsonify({"reply": "Opening Google search.", "action": "open_url", "url": "https://www.google.com"})

    if "open github" in query:
        webbrowser.open("https://github.com")
        return jsonify({"reply": "Opening GitHub.", "action": "open_url", "url": "https://github.com"})

    if "play music" in query or "spotify" in query:
        webbrowser.open("https://open.spotify.com")
        return jsonify({"reply": "Opening Spotify.", "action": "open_url", "url": "https://open.spotify.com"})

    if query.startswith("search for ") or query.startswith("google "):
        search_term = query.replace("search for ", "").replace("google ", "").strip()
        url = f"https://www.google.com/search?q={search_term}"
        webbrowser.open(url)
        return jsonify({"reply": f"Searching Google for '{search_term}'.", "action": "open_url", "url": url})

    # Query Gemini Model
    if not gemini_model:
        return jsonify({"reply": "Gemini API key is missing. Please configure your API key in the settings drawer."}), 200

    try:
        # Build chat history context
        formatted_history = []
        for item in history[-6:]:
            role = "user" if item.get("sender") == "user" else "model"
            formatted_history.append({"role": role, "parts": [item.get("text", "")]})

        chat_session = gemini_model.start_chat(history=formatted_history[:-1] if len(formatted_history) > 1 else [])
        response = chat_session.send_message(user_message)
        return jsonify({"reply": response.text.strip(), "action": None})
    except Exception as e:
        return jsonify({"reply": f"AI Engine Error: {str(e)}", "action": None}), 500

if __name__ == "__main__":
    print("🚀 Starting Alice Web Assistant on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
