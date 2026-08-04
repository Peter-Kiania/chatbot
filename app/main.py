import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="Chatbot")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


class Message(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=10_000)


class ChatRequest(BaseModel):
    messages: list[Message] = Field(min_length=1, max_length=50)


class ChatResponse(BaseModel):
    message: str


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY is not configured")

    client = OpenAI(api_key=api_key)
    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            instructions="You are a friendly, concise, and helpful assistant.",
            input=[message.model_dump() for message in request.messages],
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail="The AI service could not answer") from exc

    if not response.output_text:
        raise HTTPException(status_code=502, detail="The AI service returned an empty answer")
    return ChatResponse(message=response.output_text)

