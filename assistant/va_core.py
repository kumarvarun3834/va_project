import os
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model = "gemini-2.5-flash"


# ================= AI =================
def respond_to_user(prompt):
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"[AI Error] {e}")
        return None


# ================= HELPERS =================
def extract_number(text):
    match = re.findall(r"\d+", text)
    return "".join(match) if match else None


# ================= COMMAND PROCESSOR =================
def process_command(send):
    if not send:
        return {"type": "error", "message": "No input provided."}

    data = send.lower().strip()

    # ===== Greetings =====
    if any(x in data for x in ["hi nova", "hello nova", "hey nova"]):
        return {
            "type": "text",
            "message": "Hi! I’m Nova. How can I assist you?"
        }

    elif data == "hello":
        return {
            "type": "text",
            "message": "Hello! How can I help you?"
        }

    # ===== OPEN ACTIONS =====
    elif any(x in data for x in ["open youtube", "launch youtube"]):
        return {
            "type": "action",
            "command": "open_url",
            "url": "https://www.youtube.com/"
        }

    elif any(x in data for x in ["open spotify", "launch spotify"]):
        return {
            "type": "action",
            "command": "spotify"
        }

    elif any(x in data for x in ["open whatsapp", "launch whatsapp"]):
        return {
            "type": "action",
            "command": "whatsapp"
        }

    elif any(x in data for x in ["open chrome", "launch chrome", "open browser"]):
        return {
            "type": "action",
            "command": "open_url",
            "url": "https://www.google.com"
        }

    # ===== PHONE CALL =====
    elif data.startswith(("call ", "dial ")):
        number = extract_number(data)

        if not number:
            return {
                "type": "text",
                "message": "No number provided."
            }

        return {
            "type": "action",
            "command": "call",
            "number": number
        }

    # ===== MAPS =====
    elif data.startswith(("navigate ", "map ", "directions to ")):
        place = (
            data.replace("navigate", "")
                .replace("map", "")
                .replace("directions to", "")
                .strip()
        )

        if not place:
            return {
                "type": "text",
                "message": "Where do you want to go?"
            }

        return {
            "type": "action",
            "command": "maps",
            "place": place
        }

    # ===== SEARCH =====
    elif data.startswith(("search ", "google ")):
        query = (
            data.replace("search", "")
                .replace("google", "")
                .strip()
        )

        if not query:
            return {
                "type": "text",
                "message": "What do you want me to search for?"
            }

        return {
            "type": "action",
            "command": "search",
            "query": query
        }

    # ===== DEFAULT → AI =====
    else:
        answer = respond_to_user(send)

        if answer:
            return {
                "type": "text",
                "message": answer
            }

        return {
            "type": "error",
            "message": "I couldn't get a response from the AI."
        }