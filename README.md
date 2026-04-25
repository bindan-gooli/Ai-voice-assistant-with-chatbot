# Alice - AI Voice Assistant with Chatbot

An intelligent, multi-modal AI voice assistant built with Python that combines speech recognition, text-to-speech, and Google's Gemini API for natural conversations. Features both voice and text input with a graphical user interface powered by Pygame.

## Features

- 🎤 **Voice Input & Output**: Real-time speech recognition and text-to-speech capabilities
- 💬 **AI Chatbot**: Powered by Google Gemini 1.5 Pro for intelligent conversations
- 🖥️ **GUI Interface**: User-friendly Pygame interface with text and voice buttons
- 🎯 **Keyword Activation**: Activate voice input by saying "Hello Alice"
- 🌐 **Web Integration**: Open websites and play music directly from voice commands
- ⏰ **Smart Responses**: Handle special requests like date/time queries
- 💾 **Conversation History**: Maintains chat history for context-aware responses
- 🔒 **Safety Settings**: Configurable content safety filters

## Prerequisites

Before running this application, ensure you have:

- Python 3.8 or higher
- Microphone and speakers
- A Google Gemini API key (get one at [Google AI Studio](https://aistudio.google.com/))
- For Linux: `alsa-utils` and `python3-dev` packages

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/bindan-gooli/Ai-voice-assistant-with-chatbot.git
cd Ai-voice-assistant-with-chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install google-generativeai
pip install SpeechRecognition
pip install pyttsx3
pip install pygame
```

### 3. System Dependencies (Linux)

```bash
sudo apt-get install python3-dev
sudo apt-get install alsa-utils
```

## Configuration

### Set Up Google API Key

**Option 1: Environment Variable (Recommended)**

Export the API key as an environment variable:

```bash
export GOOGLE_API_KEY="your_api_key_here"
python assistant.py
```

**Option 2: Create .env File**

Create a `.env` file in the project directory:

```
GOOGLE_API_KEY=your_api_key_here
```

Then run:

```bash
python assistant.py
```

## Usage

### Running the Application

```bash
python assistant.py
```

### Interface Guide

1. **Text Input Button**: Click to enable text mode, type your message, and press Enter or click the button again
2. **Voice Input Button**: Click to start listening for voice commands
3. **Keyword Activation**: Say "Hello Alice" to activate voice input at any time

### Example Commands

- "What is the current date and time?"
- "Play music"
- "Open YouTube"
- "Open Google"
- "Tell me a joke"
- "What is Python?"

## GUI Controls

| Control | Action |
|---------|--------|
| Text Input Box | Type your message |
| Text Input Button | Submit text message |
| Voice Input Button | Record voice message |
| Keyboard Return | Submit text message |
| Keyboard Backspace | Delete character |
| Window Close | Exit application |

## Special Features

### Auto-Wake Keywords
- **"Hello Alice"**: Automatically activates voice listening mode

### Built-in Commands
- **Date/Time**: Ask about current date and time
- **Music**: Request to play music (opens Gaana)
- **Google**: Open Google search
- **YouTube**: Open YouTube
- **Custom URLs**: "Open [website]" to visit any website

## Project Structure

```
Ai-voice-assistant-with-chatbot/
├── assistant.py              # Main application file
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .gitignore               # Git ignore file
```

## Architecture

### Key Components

1. **Speech Recognition Module**: Uses Google Speech Recognition API
2. **Text-to-Speech**: pyttsx3 for voice output
3. **AI Model**: Google Gemini 1.5 Pro for conversations
4. **GUI**: Pygame-based graphical interface
5. **Threading**: Background keyword listener thread

### Data Flow

```
User Input (Voice/Text)
    ↓
Preprocessing & Special Request Check
    ↓
If Special: Execute Command → TTS
If General: Send to Gemini API → Get Response → Display & TTS
    ↓
Update Chat History
```

## Configuration Settings

### Gemini Model Settings

```python
generation_config = {
    "temperature": 0,              # Deterministic responses
    "top_p": 0.95,                # Nucleus sampling
    "top_k": 40,                  # Top-k sampling
    "max_output_tokens": 8192,    # Max response length
    "response_mime_type": "text/plain",
}
```

### Safety Settings

- Harassment: BLOCK_NONE
- Hate Speech: BLOCK_MEDIUM_AND_ABOVE
- Dangerous Content: BLOCK_MEDIUM_AND_ABOVE

## Troubleshooting

### Issue: "GOOGLE_API_KEY environment variable is not set"

**Solution**: Set the environment variable before running:

```bash
export GOOGLE_API_KEY="your_api_key"
python assistant.py
```

### Issue: Microphone Not Working

**Solution**: 
- Check if microphone is connected and detected
- Run `lsof -i :` to check audio conflicts
- On Linux: Install `alsa-utils` → `sudo apt-get install alsa-utils`

### Issue: Speech Recognition Fails

**Solution**:
- Ensure internet connection (Google Speech API requires it)
- Speak clearly and loudly
- Reduce background noise
- Increase `phrase_time_limit` in the code if needed

### Issue: Text-to-Speech Not Working

**Solution**:
- Check if speakers are working
- On Linux: Install voice packages → `sudo apt-get install espeak`
- Try different voices by modifying `engine.setProperty('voice', voices[0].id)`

### Issue: Pygame Window Won't Load

**Solution**:
- Ensure display server is running (in containers, use X11 forwarding)
- Try: `export SDL_VIDEODRIVER=dummy` for headless mode

## Requirements

```
google-generativeai>=0.3.0
SpeechRecognition>=3.10.0
pyttsx3>=2.90
pygame>=2.1.0
```

## Performance Tips

1. **Reduce display lines**: Modify `display_lines[-10:]` in `main()` function
2. **Adjust FPS**: Change `clock.tick(30)` value (lower = less CPU usage)
3. **Optimize audio timeout**: Modify `phrase_time_limit` for faster/slower recognition

## API Rate Limits

Google Gemini API has usage quotas. Monitor your usage at [Google Cloud Console](https://console.cloud.google.com/).

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open a GitHub issue.

## Acknowledgments

- Google Generative AI (Gemini API)
- SpeechRecognition library
- Pygame community
- pyttsx3 contributors

## Roadmap

- [ ] Support for multiple languages
- [ ] Conversation history export
- [ ] Custom wake word configuration
- [ ] Integration with more services (Spotify, WhatsApp, etc.)
- [ ] Wake word detection optimization
- [ ] Offline mode support
- [ ] Mobile app version

---

**Created by**: [bindan-gooli](https://github.com/bindan-gooli)

**Last Updated**: 2026-04-25

