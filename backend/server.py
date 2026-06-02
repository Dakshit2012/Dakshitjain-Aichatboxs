"""
Chatbot Backend
- FastAPI + MongoDB (motor) + Emergent LLM (emergentintegrations)
- Endpoints:
    POST   /api/sessions                  -> create new session
    GET    /api/sessions                  -> list sessions
    GET    /api/sessions/{id}             -> get one session
    PATCH  /api/sessions/{id}             -> rename / change model
    DELETE /api/sessions/{id}             -> delete session + messages
    GET    /api/sessions/{id}/messages    -> messages history
    POST   /api/sessions/{id}/messages    -> send a user message, get AI reply
    GET    /api/models                    -> available models grouped by provider
"""
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field, ConfigDict
from emergentintegrations.llm.chat import LlmChat, UserMessage

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ.get("DB_NAME", "test_database")
EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY", "")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

app = FastAPI(title="Tidepaper Chat API")
api_router = APIRouter(prefix="/api")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("chat-api")

# ---------- Models ----------
class SessionCreate(BaseModel):
    title: Optional[str] = None
    provider: str = "openai"
    model: str = "gpt-5"
    system_message: Optional[str] = None

class SessionUpdate(BaseModel):
    title: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    system_message: Optional[str] = None

class ChatSession(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    title: str
    provider: str
    model: str
    system_message: str
    created_at: datetime
    updated_at: datetime

class Message(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    session_id: str
    role: str  # 'user' | 'assistant' | 'system'
    content: str
    provider: Optional[str] = None
    model: Optional[str] = None
    created_at: datetime

class SendMessage(BaseModel):
    text: str
    # Optional per-message override
    provider: Optional[str] = None
    model: Optional[str] = None

# ---------- Helpers ----------
DEFAULT_SYSTEM_MESSAGE = (
    "You are Tidepaper, a helpful, precise, and friendly AI assistant. "
    "Format responses in Markdown. Use fenced code blocks with language hints for code. "
    "Keep answers clear and well-structured."
)

AVAILABLE_MODELS: Dict[str, List[str]] = {
    "openai": ["gpt-5", "gpt-5-mini", "gpt-4o", "gpt-4o-mini", "gpt-4.1"],
    "anthropic": [
        "claude-sonnet-4-6",
        "claude-opus-4-6",
        "claude-sonnet-4-5-20250929",
        "claude-haiku-4-5-20251001",
    ],
    "gemini": [
        "gemini-3-flash-preview",
        "gemini-2.5-pro",
        "gemini-2.5-flash",
    ],
}

def _now() -> datetime:
    return datetime.now(timezone.utc)

def _serialize(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert Mongo doc datetimes to isoformat for JSON."""
    if not doc:
        return doc
    out = {}
    for k, v in doc.items():
        if k == "_id":
            continue
        if isinstance(v, datetime):
            out[k] = v.isoformat()
        else:
            out[k] = v
    return out

async def _get_session_or_404(session_id: str) -> Dict[str, Any]:
    s = await db.chat_sessions.find_one({"id": session_id})
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    return s

def _build_initial_messages(system_message: str, history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Reconstruct LlmChat-compatible message history from DB messages.
    Each user message stored as text becomes content [{type:text,text:...}].
    Assistant messages stored as plain string content.
    """
    msgs: List[Dict[str, Any]] = [{"role": "system", "content": system_message}]
    for m in history:
        if m["role"] == "user":
            msgs.append({"role": "user", "content": [{"type": "text", "text": m["content"]}]})
        elif m["role"] == "assistant":
            msgs.append({"role": "assistant", "content": m["content"]})
    return msgs

# ---------- Routes ----------
@api_router.get("/")
async def root():
    return {"ok": True, "service": "tidepaper-chat"}

@api_router.get("/models")
async def get_models():
    return {
        "models": AVAILABLE_MODELS,
        "default": {"provider": "openai", "model": "gpt-5"},
    }

@api_router.post("/sessions")
async def create_session(payload: SessionCreate):
    if payload.provider not in AVAILABLE_MODELS:
        raise HTTPException(status_code=400, detail=f"Unknown provider {payload.provider}")
    if payload.model not in AVAILABLE_MODELS[payload.provider]:
        raise HTTPException(status_code=400, detail=f"Unknown model {payload.model} for provider {payload.provider}")
    sid = str(uuid.uuid4())
    now = _now()
    doc = {
        "id": sid,
        "title": payload.title or "New conversation",
        "provider": payload.provider,
        "model": payload.model,
        "system_message": payload.system_message or DEFAULT_SYSTEM_MESSAGE,
        "created_at": now,
        "updated_at": now,
    }
    await db.chat_sessions.insert_one(doc)
    return _serialize(doc)

@api_router.get("/sessions")
async def list_sessions():
    cursor = db.chat_sessions.find({}).sort("updated_at", -1)
    sessions = await cursor.to_list(500)
    return [_serialize(s) for s in sessions]

@api_router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    s = await _get_session_or_404(session_id)
    return _serialize(s)

@api_router.patch("/sessions/{session_id}")
async def update_session(session_id: str, payload: SessionUpdate):
    s = await _get_session_or_404(session_id)
    updates: Dict[str, Any] = {}
    if payload.title is not None:
        title = payload.title.strip()
        if not title:
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        updates["title"] = title
    if payload.provider is not None:
        if payload.provider not in AVAILABLE_MODELS:
            raise HTTPException(status_code=400, detail="Unknown provider")
        updates["provider"] = payload.provider
    if payload.model is not None:
        prov = updates.get("provider", s["provider"])
        if payload.model not in AVAILABLE_MODELS.get(prov, []):
            raise HTTPException(status_code=400, detail="Unknown model for provider")
        updates["model"] = payload.model
    if payload.system_message is not None:
        updates["system_message"] = payload.system_message
    if not updates:
        return _serialize(s)
    updates["updated_at"] = _now()
    await db.chat_sessions.update_one({"id": session_id}, {"$set": updates})
    new_doc = await db.chat_sessions.find_one({"id": session_id})
    return _serialize(new_doc)

@api_router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    await _get_session_or_404(session_id)
    await db.chat_messages.delete_many({"session_id": session_id})
    await db.chat_sessions.delete_one({"id": session_id})
    return {"ok": True, "deleted": session_id}

@api_router.get("/sessions/{session_id}/messages")
async def list_messages(session_id: str):
    await _get_session_or_404(session_id)
    cursor = db.chat_messages.find({"session_id": session_id}).sort("created_at", 1)
    msgs = await cursor.to_list(2000)
    return [_serialize(m) for m in msgs]

@api_router.post("/sessions/{session_id}/messages")
async def send_message(session_id: str, payload: SendMessage):
    if not payload.text or not payload.text.strip():
        raise HTTPException(status_code=400, detail="Message text cannot be empty")
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="EMERGENT_LLM_KEY not configured")
    session = await _get_session_or_404(session_id)

    provider = payload.provider or session["provider"]
    model = payload.model or session["model"]
    if provider not in AVAILABLE_MODELS or model not in AVAILABLE_MODELS[provider]:
        raise HTTPException(status_code=400, detail="Invalid provider/model")

    # Load history
    history_cursor = db.chat_messages.find({"session_id": session_id}).sort("created_at", 1)
    history = await history_cursor.to_list(2000)

    # Persist user message
    user_doc = {
        "id": str(uuid.uuid4()),
        "session_id": session_id,
        "role": "user",
        "content": payload.text.strip(),
        "provider": provider,
        "model": model,
        "created_at": _now(),
    }
    await db.chat_messages.insert_one(user_doc)

    initial_messages = _build_initial_messages(session["system_message"], history)

    try:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=session["system_message"],
            initial_messages=initial_messages,
        ).with_model(provider, model)
        ai_response = await chat.send_message(UserMessage(text=payload.text.strip()))
    except Exception as exc:
        logger.exception("LLM call failed")
        # Persist an error assistant message so UI shows feedback
        err_doc = {
            "id": str(uuid.uuid4()),
            "session_id": session_id,
            "role": "assistant",
            "content": f"⚠️ Error from {provider}/{model}: {str(exc)[:300]}",
            "provider": provider,
            "model": model,
            "created_at": _now(),
            "error": True,
        }
        await db.chat_messages.insert_one(err_doc)
        await db.chat_sessions.update_one({"id": session_id}, {"$set": {"updated_at": _now()}})
        return JSONResponse(
            status_code=502,
            content={
                "detail": "LLM provider error",
                "user_message": _serialize(user_doc),
                "assistant_message": _serialize(err_doc),
            },
        )

    assistant_doc = {
        "id": str(uuid.uuid4()),
        "session_id": session_id,
        "role": "assistant",
        "content": ai_response,
        "provider": provider,
        "model": model,
        "created_at": _now(),
    }
    await db.chat_messages.insert_one(assistant_doc)

    # Update session updated_at and provider/model if changed; auto-title on first turn
    set_doc: Dict[str, Any] = {"updated_at": _now()}
    if session["title"] in ("New conversation", "") and len(history) == 0:
        # use first user message as a title (truncated)
        title = payload.text.strip().split("\n")[0][:60]
        set_doc["title"] = title
    set_doc["provider"] = provider
    set_doc["model"] = model
    await db.chat_sessions.update_one({"id": session_id}, {"$set": set_doc})

    return {
        "user_message": _serialize(user_doc),
        "assistant_message": _serialize(assistant_doc),
    }

# ---------- App wiring ----------
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
