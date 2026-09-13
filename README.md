# AI-Powered Web Assistant

A simple Flask web application that uses **LangChain** and **Google Gemini** to power an AI assistant. The assistant takes a user message, sends it through a structured prompt, and returns a clean, structured JSON response (summary, sentiment, and reply).

> ⚠️ **Status:** This is a work-in-progress project, not a finished product. Core chat functionality works, but several planned features are not implemented yet.

## Features

- Flask backend with a simple web UI (`templates/`, `static/`)
- AI responses generated through **LangChain + Gemini** (`langchain-google-genai`)
- Structured JSON output using a Pydantic schema, containing:
  - `summary` – short summary of the user's message
  - `sentiment` – score from 0 (very negative) to 100 (very positive)
  - `response` – the assistant's reply
- Configurable model parameters (model ID, temperature, max output tokens) via `config.py`
- Basic error handling and response-time tracking on the `/generate` endpoint

## Tech Stack

- **Backend:** Python, Flask
- **AI/LLM:** LangChain, `langchain-google-genai`, Google Generative AI (Gemini)
- **Config:** `python-dotenv` for environment variables
- **Frontend:** HTML/CSS/JS (Flask templates + static files)

## Project Structure

```
AI-powered-Web-Assistant/
├── app.py              # Flask app and API routes
├── model.py            # LangChain + Gemini logic, prompt template, JSON parsing
├── config.py           # API keys and model parameters
├── metadata.json       # Project metadata
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
├── static/             # CSS/JS/static assets
└── ...
```

## How It Works

1. The user submits a message from the web UI.
2. The Flask `/generate` endpoint receives the message and forwards it to `model.py`.
3. A prompt template instructs Gemini to analyze the message and return a JSON object with a summary, sentiment score, and response.
4. LangChain parses the model's output into structured JSON using a Pydantic schema.
5. The result (plus response time) is sent back to the frontend as JSON.

## Getting Started

### Prerequisites

- Python 3.9+
- A Google Gemini API key

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Nadeeshan-n/AI-powered-Web-Assistant-.git
   cd AI-powered-Web-Assistant-
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

4. Run the app:
   ```bash
   python app.py
   ```

5. Open `http://localhost:5000` in your browser.

## API

### `POST /generate`

Request body:
```json
{
  "message": "Your message here",
  "model": "gemini"
}
```

Response:
```json
{
  "summary": "...",
  "sentiment": 75,
  "response": "...",
  "duration": 1.23
}
```

## Current Limitations

- Only the Gemini model is currently supported, even though the code is structured to support multiple LLMs
- No conversation history / memory between requests
- No authentication or rate limiting
- No RAG (retrieval-augmented generation) or agent capabilities yet
- No automated tests

## Planned / Further Implementation

- [ ] Support for additional LLM providers (OpenAI, Claude, etc.)
- [ ] Conversation memory / chat history
- [ ] Retrieval-Augmented Generation (RAG) for document-based Q&A
- [ ] Response caching
- [ ] Agent/tool-calling support
- [ ] Improved frontend UI/UX
- [ ] Deployment setup (Docker, hosting instructions)

## Contributing

This is an evolving personal/learning project. Suggestions and pull requests are welcome as the implementation continues.
