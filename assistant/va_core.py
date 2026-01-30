import os
import webbrowser
from dotenv import load_dotenv
from .speak import speak
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model = "gemini-2.5-flash"

def respond_to_user(prompt):
    try:
        # Call Gemini API
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        text = response.text
        print("[Assistant]:", text)


        return text
    except Exception as e:
        print(f"[AI Error] {e}")
        return None

def search_file(filename, search_path):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

def process_command(send):
    if send is None:
        return "No input provided."

    data_btn = send.lower()

    if "hi nova" in data_btn or "hello nova" in data_btn or "hey nova" in data_btn:
        speak("Hi! I’m Nova, your AI assistant. How can I assist you today?")
        return "Hi! I’m Nova, your AI assistant. How can I assist you?"

    elif "hello" in data_btn:
        speak("Hello! How can I help you today?")
        return "Hello! How can I help you?"

    # Applications
    elif "open notepad" in data_btn:
        os.system("notepad")
        speak("Opening Notepad")
        return "Opening Notepad"

    elif "open chrome" in data_btn:
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(chrome_path):
            os.startfile(chrome_path)
            speak("Opening Chrome")
            return "Opening Chrome"
        else:
            speak("Chrome is not installed in the default location.")
            return "Chrome not found."

    elif "open word" in data_btn:
        word_path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
        if os.path.exists(word_path):
            os.startfile(word_path)
            speak("Opening Microsoft Word")
            return "Opening Word"
        else:
            speak("Word not found in default path")
            return "Word not found."

    elif "open spotify" in data_btn:
        spotify_path = "C:\\Users\\Dell\\AppData\\Roaming\\Spotify\\Spotify.exe"
        if os.path.exists(spotify_path):
            os.startfile(spotify_path)
            speak("Opening Spotify App")
            return "Opening Spotify App"
        else:
            speak("Spotify app not found. Opening Spotify Web.")
            webbrowser.open("https://open.spotify.com/")
            return "Opening Spotify Web"

    elif "open youtube" in data_btn:
        webbrowser.open("https://www.youtube.com/")
        speak("Opening YouTube")
        return "Opening YouTube"

    # Web Search
    elif "search" in data_btn:
        query = data_btn.replace("search", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"Searching for {query} on Google")
            return f"Searching for {query}"
        else:
            return "What do you want me to search?"

    # File System
    elif "find file" in data_btn:
        filename = data_btn.replace("find file", "").strip()
        path = search_file(filename, "C:\\Users\\Dell\\")
        if path:
            os.startfile(path)
            speak(f"Found and opened {filename}")
            return f"Opened file: {filename}"
        else:
            speak("File not found")
            return "File not found"

    elif "open downloads" in data_btn:
        os.startfile("C:\\Users\\Dell\\Downloads")
        speak("Opening Downloads folder")
        return "Opening Downloads"

    elif "open documents" in data_btn:
        os.startfile("C:\\Users\\Dell\\Documents")
        speak("Opening Documents folder")
        return "Opening Documents"

    elif "open desktop" in data_btn:
        os.startfile("C:\\Users\\Dell\\Desktop")
        speak("Opening Desktop")
        return "Opening Desktop"

    elif "run script" in data_btn:
        script_path = "C:\\Users\\Dell\\AIchatbot\\some_script.py"
        if os.path.exists(script_path):
            os.system(f'python "{script_path}"')
            speak("Running your script")
            return "Running script"
        else:
            return "Script not found"

    else:
        try:
            # model = genai.GenerativeModel("gemini-1.5-flash")  # free, fast model
            answer = respond_to_user(send)  # use the function we defined above
            if answer:
                # Don't speak here - user will click Speak button in website
                return answer
            else:
                return "I couldn't get a response from the AI."
        except Exception as e:
            speak("I had trouble reaching the AI service.")
            return f"Error with Gemini response: {str(e)}"
        
if __name__ == "__main__":
    print("Nova AI Assistant (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            speak("Goodbye!")
            break
        response = process_command(user_input)
        print("[Nova]:", response)
