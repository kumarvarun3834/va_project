# Nova - AI Virtual Assistant

A Django-based web application for an intelligent AI virtual assistant powered by Google's Gemini API.

## Features

✨ **Core Features:**
- 🤖 AI-powered responses using Google Gemini API
- 🗣️ Text-to-Speech with manual Speak/Stop control
- 🎤 Speech-to-Text microphone input
- 📝 Markdown formatting support (bold, italic, code)
- 💬 Chat history management
- ✏️ Edit previous chat names
- 🗑️ Delete chat history
- 📋 Proper text formatting with spacing and lists

## Tech Stack

- **Backend:** Django 5.0+
- **Frontend:** HTML5, CSS3, JavaScript
- **AI:** Google Gemini API (gemini-2.5-flash)
- **TTS:** pyttsx3
- **STT:** SpeechRecognition, requests-html
- **Database:** SQLite

## Installation

### Prerequisites
- Python 3.10+
- pip or conda
- Google Gemini API Key

### Setup Instructions

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/nova-ai-assistant.git
cd nova-ai-assistant
```

2. **Create virtual environment:**
```bash
python -m venv env
source env/Scripts/activate  # On Windows
# or
source env/bin/activate  # On macOS/Linux
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create .env file:**
```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

Get your API key from: https://aistudio.google.com/

5. **Run migrations:**
```bash
python manage.py migrate
```

6. **Start the server:**
```bash
python manage.py runserver
```

7. **Open in browser:**
Navigate to `http://localhost:8000`

## Usage

### Text Input
- Type your message in the input field
- Click "Send" or press Enter
- The AI will respond with formatted text

### Voice Input
- Click the 🎤 button to use microphone
- Speak your question clearly
- The response will appear as text

### Text-to-Speech
- Click 🔊 "Speak" button to hear the response
- Click ⏹ "Stop" button to stop speaking
- Button changes color when speaking

### Chat History
- View all previous chats in the sidebar
- Click ✏️ to edit chat name
- Click 🗑️ to delete a chat

## Project Structure

```
va_project/
├── assistant/
│   ├── migrations/          # Database migrations
│   ├── templates/
│   │   └── assistant/
│   │       └── index.html   # Main website
│   ├── admin.py
│   ├── apps.py
│   ├── models.py            # ChatSession, ChatMessage
│   ├── urls.py              # URL routing
│   ├── views.py             # API endpoints
│   ├── va_core.py           # AI logic & command processing
│   ├── speak.py             # Text-to-Speech
│   └── spech_to_text.py     # Speech recognition
├── va_project/
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL config
│   ├── asgi.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── .env                      # Environment variables (create this)
```

## API Endpoints

### POST `/ask/` 
Send a new message to the AI

**Request:**
```json
{
  "command": "What is Python?"
}
```

**Response:**
```json
{
  "response": "Python is a programming language...",
  "session_id": 1
}
```

### POST `/ask/<session_id>/`
Continue an existing chat session

### GET `/sessions/`
Get all chat sessions

**Response:**
```json
{
  "sessions": [
    {"id": 1, "title": "What is Python?"},
    {"id": 2, "title": "Django Tutorial"}
  ]
}
```

### GET `/history/<session_id>/`
Get chat history for a session

### DELETE `/delete-session/<session_id>/`
Delete a chat session

### PUT `/update-session/<session_id>/`
Update chat session name

**Request:**
```json
{
  "title": "New Chat Name"
}
```

## Commands (VA_CORE)

The assistant recognizes special commands:

- "hi nova" / "hello nova" / "hey nova" - Greet the assistant
- "open notepad" - Opens Notepad
- "open chrome" - Opens Chrome browser
- "open word" - Opens Microsoft Word
- "open spotify" - Opens Spotify
- "open youtube" - Opens YouTube
- "search [query]" - Searches on Google
- "find file [filename]" - Finds a file
- "open downloads/documents/desktop" - Opens folders
- Any other text - Sends to Gemini AI for response

## Configuration

### Customize AI Model
Edit `assistant/va_core.py` line 9:
```python
model = "gemini-2.5-flash"  # Change model here
```

### Customize TTS Settings
Edit `assistant/speak.py`:
```python
tts_engine.setProperty('rate', 170)    # Speaking speed
tts_engine.setProperty('volume', 1)    # Volume (0-1)
```

## Troubleshooting

**Issue: "GEMINI_API_KEY not found"**
- Solution: Create `.env` file with your API key

**Issue: "ModuleNotFoundError: No module named 'django'"**
- Solution: Run `pip install -r requirements.txt`

**Issue: Speech recognition not working**
- Solution: Check microphone permissions and internet connection

**Issue: Database errors**
- Solution: Run `python manage.py migrate`

## Future Enhancements

- [ ] User authentication and accounts
- [ ] Multiple language support
- [ ] Chat export to PDF
- [ ] Dark/Light theme toggle
- [ ] File upload support
- [ ] Integration with more APIs

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ by Shivansh**
