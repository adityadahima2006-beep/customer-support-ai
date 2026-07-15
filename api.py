from fastapi import FastAPI
from pydantic import BaseModel

from agent.intent_agent import detect_intent
from ai_agents.router import route_query

app = FastAPI(
    title="Customer Support Multi-Agent API",
    description="REST API for the Customer Support Multi-Agent AI Chatbot",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    user_message: str
    intents: list[str]
    response: str


@app.get("/")
def home():
    return {
        "status": "Running",
        "message": "Customer Support Multi-Agent API is running successfully."
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    intents = detect_intent(request.message)

    response = route_query(intents, request.message)

    return ChatResponse(
        user_message=request.message,
        intents=intents,
        response=response
    )
