import os
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import pygame
import webbrowser
from datetime import datetime, timedelta
import threading

# Initialize pygame
pygame.init()

# Screen properties
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alice - Your AI Assistant")

# Colors and fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (173, 216, 230)
FONT = pygame.font.Font(None, 32)
LARGE_FONT = pygame.font.Font(None, 48)

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Initialize speech recognizer
r = sr.Recognizer()

# Display lines for conversation history
display_lines = []

# Original code setup
genai.configure(api_key="AIzaSyDMBd_OnBIhLBpD7LT8ZP2v5ixyK0ZyNRI")

generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

history = []

def listen_for_input():
    """Listens for user input using the microphone."""
    with sr.Microphone() as source:
        print("Listening for input...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said: {}".format(text))
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def speak_response(text):
    engine.say(text)
    engine.runAndWait()

def open_website(url):
    """Opens a website in the default web browser."""
    webbrowser.open(url)

def check_special_requests(user_input):
    user_input_lower = user_input.lower()
    if "date" in user_input_lower or "time" in user_input_lower:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"The current date and time is {current_time}."
    elif "play music" in user_input_lower:
        open_website("https://www.gaana.com")
        return "Playing music."
    elif "open google" in user_input_lower:
        open_website("https://www.google.com")
        return "Opening Google."
    elif "open youtube" in user_input_lower:
        open_website("https://www.youtube.com")
        return "Opening YouTube."
    elif "open" in user_input_lower and "website" in user_input_lower:
        start_index = user_input_lower.find("open") + len("open")
        end_index = len(user_input_lower)
        website_url = user_input[start_index:end_index].strip()
        if not website_url.startswith("http"):
            website_url = "http://" + website_url
        open_website(website_url)
        return f"Opening website: {website_url}"
    return None

# Function to draw buttons
def draw_button(text, rect, color, screen, font):
    pygame.draw.rect(screen, color, rect)
    label = font.render(text, True, BLACK)
    screen.blit(label, (rect.x + 10, rect.y + 5))

# Function to detect the keyword "Hello Alice"
def keyword_listener():
    global running
    while running:
        with sr.Microphone() as source:
            try:
                print("Listening for the keyword 'Hello Alice'...")
                audio = r.listen(source, timeout=1, phrase_time_limit=5)
                command = r.recognize_google(audio).lower()
                if "hello alice" in command:
                    print("Keyword 'Hello Alice' detected, activating voice input...")
                    voice_input = listen_for_input()
                    if voice_input:
                        display_lines.append(f"You (voice): {voice_input}")
                        handle_user_input(voice_input)
            except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
                continue

# Main function to handle the pygame window
def main():
    input_box = pygame.Rect(50, HEIGHT - 50, 700, 32)
    text_button = pygame.Rect(50, HEIGHT - 100, 150, 40)
    voice_button = pygame.Rect(220, HEIGHT - 100, 150, 40)
    clock = pygame.time.Clock()
    user_text = ''
    global running
    running = True

    # Start keyword listener in a separate thread
    threading.Thread(target=keyword_listener, daemon=True).start()

    while running:
        screen.fill(WHITE)

        # Display previous conversation
        y_offset = 20
        for line in display_lines[-10:]:  # Show the last 10 lines
            draw_text(screen, line, (50, y_offset), FONT)
            y_offset += 30

        # Draw buttons
        draw_button("Text Input", text_button, BLUE, screen, FONT)
        draw_button("Voice Input", voice_button, BLUE, screen, FONT)

        # Draw the input box
        pygame.draw.rect(screen, BLACK, input_box, 2)
        txt_surface = FONT.render(user_text, True, BLACK)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_button.collidepoint(event.pos):
                    if user_text.strip():
                        display_lines.append(f"You: {user_text}")
                        handle_user_input(user_text)
                        user_text = ''
                elif voice_button.collidepoint(event.pos):
                    voice_input = listen_for_input()
                    if voice_input:
                        display_lines.append(f"You (voice): {voice_input}")
                        handle_user_input(voice_input)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and user_text.strip():
                    display_lines.append(f"You: {user_text}")
                    handle_user_input(user_text)
                    user_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Function to handle user input processing
def handle_user_input(user_input):
    global display_lines
    special_response = check_special_requests(user_input)
    if special_response:
        display_lines.append(f"Alice: {special_response}")
        speak_response(special_response)
    else:
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(user_input).text
        display_lines.append(f"Alice: {response}")
        speak_response(response)
        history.append({"role": "user", "parts": [user_input]})
        history.append({"role": "model", "parts": [response]})

# Function to draw text to the screen
def draw_text(surface, text, pos, font, color=BLACK):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (pos[0], pos[1] + i * (font.get_height() + 5)))

if _name_ == "_main_":
    main()