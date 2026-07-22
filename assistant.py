import os
import sys
import time
import math
import queue
import threading
import webbrowser
from datetime import datetime
from dotenv import load_dotenv

import pygame
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# --- INITIALIZATION & CONFIGURATION ---
pygame.init()
pygame.font.init()

# Window Settings
WIDTH, HEIGHT = 900, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alice - Next-Gen AI Voice & Chat Assistant")

# Theme Palette (Cyberpunk / Midnight Dark)
COLOR_BG = (13, 17, 23)
COLOR_CARD = (22, 27, 34)
COLOR_BORDER = (48, 54, 61)
COLOR_CYAN = (0, 229, 255)
COLOR_PURPLE = (156, 39, 176)
COLOR_WHITE = (240, 246, 252)
COLOR_GRAY = (139, 148, 158)
COLOR_MUTED = (72, 79, 88)
COLOR_USER_BUBBLE = (27, 38, 59)
COLOR_ALICE_BUBBLE = (35, 25, 66)

# Fonts
FONT_TITLE = pygame.font.SysFont("Segoe UI, Roboto, Helvetica, Arial", 26, bold=True)
FONT_SUBTITLE = pygame.font.SysFont("Segoe UI, Roboto, Helvetica, Arial", 14)
FONT_BODY = pygame.font.SysFont("Segoe UI, Roboto, Helvetica, Arial", 16)
FONT_BOLD = pygame.font.SysFont("Segoe UI, Roboto, Helvetica, Arial", 16, bold=True)
FONT_SMALL = pygame.font.SysFont("Segoe UI, Roboto, Helvetica, Arial", 13)

# Thread-safe Communication Queues
ui_queue = queue.Queue()
speech_queue = queue.Queue()

# Global State
class AssistantState:
    IDLE = "READY"
    LISTENING = "LISTENING..."
    THINKING = "THINKING (Gemini)..."
    SPEAKING = "SPEAKING..."

current_state = AssistantState.IDLE
chat_history = []  # List of dicts: {"sender": "You"|"Alice", "text": str, "time": str}
running = True

# --- GEMINI AI MODEL SETUP ---
API_KEY = os.getenv("GOOGLE_API_KEY")
gemini_model = None

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "max_output_tokens": 1024,
        }
        gemini_model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction="You are Alice, a highly intelligent, polite, and concise AI voice assistant. Keep answers brief, natural, and easy to speak out loud."
        )
    except Exception as e:
        print(f"[Warning] Failed to initialize Gemini API: {e}")

# --- TEXT-TO-SPEECH (TTS) ENGINE ---
def tts_worker():
    """Background worker for non-blocking Text-to-Speech execution."""
    try:
        tts_engine = pyttsx3.init()
        tts_engine.setProperty('rate', 175)  # Speaking rate
        voices = tts_engine.getProperty('voices')
        if len(voices) > 1:
            tts_engine.setProperty('voice', voices[1].id)  # Prefer female/alternative voice if available
    except Exception as e:
        print(f"[Warning] TTS initialization error: {e}")
        tts_engine = None

    while running:
        try:
            text = speech_queue.get(timeout=0.5)
            if text and tts_engine:
                global current_state
                current_state = AssistantState.SPEAKING
                tts_engine.say(text)
                tts_engine.runAndWait()
                current_state = AssistantState.IDLE
            speech_queue.task_done()
        except queue.Empty:
            continue
        except Exception as e:
            print(f"[Error] TTS Execution Error: {e}")

threading.Thread(target=tts_worker, daemon=True).start()

# --- SPEECH RECOGNITION (STT) ENGINE ---
recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True

def listen_in_background():
    """Worker function to capture audio input from microphone."""
    global current_state
    current_state = AssistantState.LISTENING
    
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            ui_queue.put(("system_msg", "Listening for your voice... Speak now."))
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=10)
            
            current_state = AssistantState.THINKING
            ui_queue.put(("system_msg", "Processing audio speech..."))
            
            query = recognizer.recognize_google(audio)
            if query.strip():
                process_user_request(query, is_voice=True)
            else:
                current_state = AssistantState.IDLE
    except sr.WaitTimeoutError:
        ui_queue.put(("system_msg", "No speech detected. Timed out."))
        current_state = AssistantState.IDLE
    except sr.UnknownValueError:
        ui_queue.put(("system_msg", "Sorry, I couldn't understand that audio."))
        current_state = AssistantState.IDLE
    except Exception as e:
        ui_queue.put(("system_msg", f"Microphone error: {e}"))
        current_state = AssistantState.IDLE

def trigger_voice_input():
    if current_state == AssistantState.IDLE:
        threading.Thread(target=listen_in_background, daemon=True).start()

# --- SPECIAL COMMAND HANDLER & INTENT AUTOMATION ---
def check_special_commands(user_input):
    """Processes system shortcuts and web automation tasks."""
    query = user_input.lower().strip()
    
    # Date & Time Queries
    if "time" in query or "date" in query or "day" in query:
        now = datetime.now()
        time_str = now.strftime("%I:%M %p on %A, %B %d, %Y")
        return f"It is currently {time_str}."
    
    # Web Automation Shortcuts
    if "open youtube" in query:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube for you."
    elif "open google" in query:
        webbrowser.open("https://www.google.com")
        return "Opening Google search."
    elif "open github" in query:
        webbrowser.open("https://github.com")
        return "Opening GitHub."
    elif "open wikipedia" in query:
        webbrowser.open("https://www.wikipedia.org")
        return "Opening Wikipedia."
    elif "play music" in query or "spotify" in query:
        webbrowser.open("https://open.spotify.com")
        return "Opening Spotify player."
    elif query.startswith("search for ") or query.startswith("google "):
        search_term = query.replace("search for ", "").replace("google ", "").strip()
        url = f"https://www.google.com/search?q={search_term}"
        webbrowser.open(url)
        return f"Searching Google for '{search_term}'."

    return None

def process_user_request(user_input, is_voice=False):
    """Handles query evaluation via Gemini AI model or local shortcuts."""
    global current_state
    current_state = AssistantState.THINKING
    timestamp = datetime.now().strftime("%H:%M")
    
    # Add User message to chat history
    prefix = " (Voice)" if is_voice else ""
    chat_history.append({"sender": f"You{prefix}", "text": user_input, "time": timestamp})
    
    def async_response():
        global current_state
        special_reply = check_special_commands(user_input)
        
        if special_reply:
            reply_text = special_reply
        elif gemini_model:
            try:
                # Format conversation history for Gemini multi-turn chat
                chat_context = []
                for item in chat_history[-6:]:
                    role = "user" if item["sender"].startswith("You") else "model"
                    chat_context.append({"role": role, "parts": [item["text"]]})
                
                chat_session = gemini_model.start_chat(history=chat_context[:-1] if len(chat_context) > 1 else [])
                response = chat_session.send_message(user_input)
                reply_text = response.text.strip()
            except Exception as e:
                reply_text = f"API Error: {e}"
        else:
            reply_text = "Google API Key is not configured. Set GOOGLE_API_KEY in your .env file."
        
        # Update UI & Speak
        chat_history.append({"sender": "Alice", "text": reply_text, "time": timestamp})
        speech_queue.put(reply_text)

    threading.Thread(target=async_response, daemon=True).start()

# --- UI RENDER HELPER FUNCTIONS ---
def draw_header(surface):
    # Header Background
    header_rect = pygame.Rect(0, 0, WIDTH, 70)
    pygame.draw.rect(surface, COLOR_CARD, header_rect)
    pygame.draw.line(surface, COLOR_BORDER, (0, 70), (WIDTH, 70), 1)
    
    # Title & Subtitle
    title_txt = FONT_TITLE.render("ALICE", True, COLOR_CYAN)
    sub_txt = FONT_SUBTITLE.render("Next-Gen Voice & Chat AI", True, COLOR_GRAY)
    surface.blit(title_txt, (20, 12))
    surface.blit(sub_txt, (20, 42))

    # Status Pill Indicator
    state_color = COLOR_CYAN if current_state == AssistantState.IDLE else (
        COLOR_PURPLE if current_state == AssistantState.SPEAKING else (255, 193, 7)
    )
    status_box = pygame.Rect(WIDTH - 220, 18, 200, 34)
    pygame.draw.rect(surface, COLOR_BORDER, status_box, border_radius=17)
    pygame.draw.circle(surface, state_color, (WIDTH - 204, 35), 6)
    
    status_txt = FONT_SMALL.render(current_state, True, COLOR_WHITE)
    surface.blit(status_txt, (WIDTH - 190, 26))

def draw_visualizer(surface, frame_count):
    """Renders a futuristic pulsing audio wave visualizer orb."""
    center = (WIDTH // 2, 130)
    base_radius = 35
    
    # Animation pulsation factor
    pulse = math.sin(frame_count * 0.08) * 6
    if current_state in [AssistantState.LISTENING, AssistantState.SPEAKING]:
        pulse += math.sin(frame_count * 0.25) * 12

    # Outer glow rings
    glow_color = COLOR_CYAN if current_state != AssistantState.SPEAKING else COLOR_PURPLE
    for i in range(3, 0, -1):
        r = int(base_radius + pulse + (i * 12))
        alpha = max(10, 80 - (i * 20))
        glow_surface = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*glow_color, alpha), (r, r), r)
        surface.blit(glow_surface, (center[0] - r, center[1] - r))

    # Core Orb
    pygame.draw.circle(surface, COLOR_CARD, center, base_radius + int(pulse // 2))
    pygame.draw.circle(surface, glow_color, center, base_radius + int(pulse // 2), 2)

def wrap_text(text, font, max_width):
    """Wraps text lines to fit within specified pixel width."""
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        test_str = ' '.join(current_line)
        if font.size(test_str)[0] > max_width:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def draw_chat_history(surface):
    chat_box = pygame.Rect(20, 195, WIDTH - 40, HEIGHT - 295)
    pygame.draw.rect(surface, COLOR_BG, chat_box)
    
    # Render last 6 messages nicely formatted
    y_offset = chat_box.bottom - 10
    max_bubble_width = 540

    for msg in reversed(chat_history[-8:]):
        is_user = msg["sender"].startswith("You")
        sender_color = COLOR_CYAN if is_user else COLOR_PURPLE
        bubble_bg = COLOR_USER_BUBBLE if is_user else COLOR_ALICE_BUBBLE
        
        # Prepare wrapped text
        wrapped_lines = wrap_text(msg["text"], FONT_BODY, max_bubble_width - 30)
        bubble_height = len(wrapped_lines) * 22 + 30
        
        y_offset -= bubble_height + 12
        if y_offset < chat_box.top:
            break
            
        x_pos = WIDTH - 50 - max_bubble_width if is_user else 30
        bubble_rect = pygame.Rect(x_pos, y_offset, max_bubble_width, bubble_height)
        
        # Render Bubble Card
        pygame.draw.rect(surface, bubble_bg, bubble_rect, border_radius=12)
        pygame.draw.rect(surface, COLOR_BORDER, bubble_rect, width=1, border_radius=12)
        
        # Sender Label & Timestamp
        header_str = f"{msg['sender']} • {msg['time']}"
        lbl_surface = FONT_SMALL.render(header_str, True, sender_color)
        surface.blit(lbl_surface, (x_pos + 14, y_offset + 8))
        
        # Body Lines
        line_y = y_offset + 26
        for line in wrapped_lines:
            txt_surface = FONT_BODY.render(line, True, COLOR_WHITE)
            surface.blit(txt_surface, (x_pos + 14, line_y))
            line_y += 22

# --- MAIN GUI LOOP ---
def main():
    global running, current_state
    clock = pygame.time.Clock()
    frame_count = 0
    
    input_text = ""
    input_active = True
    system_notification = "Press SPACE or Click Mic to talk. Type below to chat."

    # UI Element Rectangles
    input_box = pygame.Rect(20, HEIGHT - 85, WIDTH - 210, 48)
    mic_btn = pygame.Rect(WIDTH - 175, HEIGHT - 85, 155, 48)

    while running:
        frame_count += 1
        screen.fill(COLOR_BG)

        # Process UI Queue Notifications
        while not ui_queue.empty():
            msg_type, payload = ui_queue.get()
            if msg_type == "system_msg":
                system_notification = payload

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mic_btn.collidepoint(event.pos):
                    trigger_voice_input()
                elif input_box.collidepoint(event.pos):
                    input_active = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not input_text:
                    trigger_voice_input()
                elif event.key == pygame.K_RETURN and input_text.strip():
                    query = input_text.strip()
                    input_text = ""
                    process_user_request(query, is_voice=False)
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if event.unicode and len(input_text) < 120:
                        input_text += event.unicode

        # --- DRAWING COMPONENTS ---
        draw_header(screen)
        draw_visualizer(screen, frame_count)
        draw_chat_history(screen)

        # Status Notification Banner
        notif_txt = FONT_SMALL.render(system_notification, True, COLOR_GRAY)
        screen.blit(notif_txt, (25, HEIGHT - 98))

        # Render Input Box
        box_border_color = COLOR_CYAN if input_active else COLOR_BORDER
        pygame.draw.rect(screen, COLOR_CARD, input_box, border_radius=8)
        pygame.draw.rect(screen, box_border_color, input_box, width=1, border_radius=8)
        
        # Input Text & Blinking Cursor
        display_input = input_text + ("|" if (frame_count // 20) % 2 == 0 else "")
        txt_surf = FONT_BODY.render(display_input if input_text else "Type a message...", True, COLOR_WHITE if input_text else COLOR_MUTED)
        screen.blit(txt_surf, (input_box.x + 14, input_box.y + 14))

        # Render Voice Mic Button
        mic_color = COLOR_PURPLE if current_state == AssistantState.LISTENING else COLOR_CYAN
        pygame.draw.rect(screen, mic_color, mic_btn, border_radius=8)
        mic_txt = FONT_BOLD.render("🎤 VOICE MODE", True, COLOR_BG)
        screen.blit(mic_txt, (mic_btn.x + 18, mic_btn.y + 14))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()