# 🎙️ Alice - Next-Gen AI Voice Assistant & Chatbot

A sleek, futuristic AI voice and chat assistant powered by **Google Gemini 1.5**, **Web Speech API**, **Flask**, **Pygame**, and **SpeechRecognition**. Featuring an interactive Web UI with animated audio visualizer, dual voice/text input modes, non-blocking multithreading, and web automation capabilities.

---

## ✨ Features

- **🌐 Interactive Web Frontend (`app.py`)**: Modern cyberpunk dark interface with glassmorphism, real-time glowing audio visualizer, Web Speech API integration, and Speech Synthesis.
- **🤖 Google Gemini 1.5 Integration**: High-speed, natural conversational responses with multi-turn dialogue memory.
- **🎤 Dual Input Modes**:
  - **Voice Mode**: Real-time microphone listening via Web Speech API / SpeechRecognition.
  - **Text Chat Input**: Type queries directly into the text field with smooth cursor rendering.
- **💻 Desktop App (`assistant.py`)**: Pygame-based desktop voice assistant application.
- **🌐 Automation & Web Shortcuts**:
  - Open popular sites ("Open YouTube", "Open Google", "Open GitHub", "Open Wikipedia", "Play Music").
  - Automated web searching ("Search Google for AI news").
  - Date & Time queries ("What time is it?").

---

## 🚀 Quick Start (Web Frontend)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Gemini API Key
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_actual_gemini_api_key_here
```

### 3. Launch Web App
```bash
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your web browser!

---

## 🖥️ Desktop App (`assistant.py`)

Run the Pygame desktop GUI version:
```bash
python assistant.py
```

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
