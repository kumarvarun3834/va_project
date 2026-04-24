import os
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


# ================= COMMAND PROCESSOR =================
def process_command(send):
    if not send:
        return {"type": "error", "message": "No input provided."}

    data = send.lower().strip()

    # ===== Greetings =====
    if any(x in data for x in ["hi nova", "hello nova", "hey nova"]):
        return {"type": "text", "message": "Hi! I’m Nova. How can I assist you?"}

    elif data == "hello":
        return {"type": "text", "message": "Hello! How can I help you?"}

    # ===== Web-safe Actions =====
    elif "open youtube" in data:
        return {
            "type": "action",
            "command": "open_url",
            "url": "https://www.youtube.com/"
        }

    elif "open spotify" in data:
        return {
            "type": "action",
            "command": "spotify"
        }

    elif "open whatsapp" in data:
        return {
            "type": "action",
            "command": "whatsapp"
        }

    elif "call" in data:
        # basic number extraction
        number = "".join(filter(str.isdigit, data))
        return {
            "type": "action",
            "command": "call",
            "number": number if number else None
        }

    elif "navigate" in data or "map" in data:
        place = data.replace("navigate", "").replace("map", "").strip()
        return {
            "type": "action",
            "command": "maps",
            "place": place
        }

    elif "search" in data:
        query = data.replace("search", "").strip()
        return {
            "type": "action",
            "command": "search",
            "query": query
        }

    # ===== Default → AI =====
    else:
        answer = respond_to_user(send)

        if answer:
            return {
                "type": "text",
                "message": answer
            }
        else:
            return {
                "type": "error",
                "message": "I couldn't get a response from the AI."
            }