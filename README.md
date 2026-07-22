# 🎙️ Alice - Next-Gen AI Voice Assistant & Chatbot

A sleek, futuristic AI voice and chat assistant powered by **Google Gemini 1.5**, **Pygame**, **SpeechRecognition**, and **pyttsx3**. Featuring a real-time animated audio visualizer, dual voice/text input modes, non-blocking multithreading, and web automation capabilities.

---

## ✨ Features

- **🤖 Google Gemini 1.5 Integration**: High-speed, natural conversational responses with intelligent multi-turn dialogue memory.
- **🎨 Futuristic Cyberpunk GUI**: Sleek dark interface built with Pygame, featuring a glowing pulsing audio visualizer orb that reacts to speech states (`LISTENING`, `THINKING`, `SPEAKING`).
- **🎤 Dual Input Modes**:
  - **Voice Mode**: Real-time microphone listening via `SpeechRecognition`. Triggered by clicking the voice button or pressing `SPACEBAR`.
  - **Text Chat Input**: Type queries directly into the text field with smooth cursor rendering and `ENTER` key dispatch.
- **⚡ Non-Blocking Threading**: Speech recognition, Text-to-Speech (TTS), and Gemini API calls execute asynchronously in background threads to guarantee a 60 FPS smooth GUI experience.
- **🌐 Automation & Web Shortcuts**:
  - Open popular sites ("Open YouTube", "Open Google", "Open GitHub", "Open Wikipedia", "Play Music").
  - Automated web searching ("Search Google for Python tutorials").
  - Date & Time queries ("What time is it?").

---

## 🚀 Getting Started

### Prerequisites
* **Python 3.9+** installed on your system.
* A valid **Google Gemini API Key** (get one free from [Google AI Studio](https://aistudio.google.com/)).

---

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bindan-gooli/Ai-voice-assistant-with-chatbot.git
   cd Ai-voice-assistant-with-chatbot
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API Key**:
   Create a `.env` file in the project root (or copy `.env.example`):
   ```bash
   cp .env.example .env
   ```
   Add your Google Gemini API key:
   ```env
   GOOGLE_API_KEY=your_actual_gemini_api_key_here
   ```

---

## 🎮 Usage

Run the assistant application:
```bash
python assistant.py
```

### Controls & Shortcuts
* **`SPACEBAR` / `🎤 VOICE MODE` Button**: Activates microphone voice recognition.
* **Text Input Box**: Type your query and press `ENTER` to send.
* **`BACKSPACE`**: Delete text input characters.

---

## 🛠️ Tech Stack

* **GUI Framework**: `pygame`
* **Large Language Model**: `google-generativeai` (Gemini 1.5 Flash / Pro)
* **Speech-to-Text (STT)**: `SpeechRecognition`
* **Text-to-Speech (TTS)**: `pyttsx3`
* **Environment Management**: `python-dotenv`

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
