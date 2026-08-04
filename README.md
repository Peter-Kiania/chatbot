# Python Chatbot

A small web chatbot built with FastAPI and the OpenAI Responses API.

## Setup

1. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the project:

   ```powershell
   pip install -e ".[dev]"
   ```

3. Copy `.env.example` to `.env`, then replace `your_api_key_here` with your OpenAI API key. Never commit `.env`.

4. Start the app:

   ```powershell
   uvicorn app.main:app --reload
   ```

5. Open <http://127.0.0.1:8000>.

## Tests

```powershell
pytest
```

The model is controlled by `OPENAI_MODEL` in `.env`, so it can be changed without editing the application.
