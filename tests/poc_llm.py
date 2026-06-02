"""
POC: Test Emergent LLM integration for chatbot
- Verify single-turn chat works
- Verify multi-turn (memory) works
- Verify provider/model switching works
- Verify Mongo persistence of sessions + messages
"""
import asyncio
import os
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from emergentintegrations.llm.chat import LlmChat, UserMessage

load_dotenv("/app/backend/.env")
EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY")
MONGO_URL = os.environ.get("MONGO_URL")
DB_NAME = os.environ.get("DB_NAME", "test_database")


def make_chat(session_id: str, system_message: str, provider: str = "openai", model: str = "gpt-5.4"):
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=session_id,
        system_message=system_message,
    ).with_model(provider, model)
    return chat


async def test_single_turn():
    print("\n=== TEST 1: Single-turn ===")
    chat = make_chat(str(uuid.uuid4()), "You are a concise assistant.")
    resp = await chat.send_message(UserMessage(text="Say exactly: 'Hello, integration test!'"))
    print(f"Response: {resp}")
    assert resp and isinstance(resp, str), "Expected non-empty string response"
    print("PASS: Single-turn works")
    return True


async def test_multi_turn_memory():
    print("\n=== TEST 2: Multi-turn memory ===")
    chat = make_chat(str(uuid.uuid4()), "You are a helpful assistant.")
    r1 = await chat.send_message(UserMessage(text="My favorite color is teal. Remember this."))
    print(f"R1: {r1}")
    r2 = await chat.send_message(UserMessage(text="What is my favorite color? Reply with just the color word."))
    print(f"R2: {r2}")
    assert "teal" in r2.lower(), f"Memory failed. Got: {r2}"
    print("PASS: Multi-turn memory works")
    return True


async def test_provider_switch():
    print("\n=== TEST 3: Provider switching ===")
    providers = [
        ("openai", "gpt-5.4"),
        ("anthropic", "claude-sonnet-4-6"),
        ("gemini", "gemini-3-flash-preview"),
    ]
    results = {}
    for provider, model in providers:
        try:
            chat = make_chat(str(uuid.uuid4()), "You are a helpful assistant.", provider, model)
            resp = await chat.send_message(UserMessage(text=f"Say 'Hello from {provider}' and nothing else."))
            print(f"  {provider}/{model}: {resp[:80]}")
            results[provider] = bool(resp)
        except Exception as e:
            print(f"  {provider}/{model} FAILED: {e}")
            results[provider] = False
    print(f"Results: {results}")
    assert any(results.values()), "All providers failed"
    print("PASS: At least one provider works")
    return results


async def test_mongo_persistence():
    print("\n=== TEST 4: Mongo persistence ===")
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    session_id = str(uuid.uuid4())
    await db.sessions_test.insert_one({
        "_id": session_id,
        "title": "POC Session",
        "model": "openai/gpt-5.4",
        "created_at": datetime.now(timezone.utc),
    })
    await db.messages_test.insert_many([
        {"_id": str(uuid.uuid4()), "session_id": session_id, "role": "user", "content": "Hi", "created_at": datetime.now(timezone.utc)},
        {"_id": str(uuid.uuid4()), "session_id": session_id, "role": "assistant", "content": "Hello!", "created_at": datetime.now(timezone.utc)},
    ])
    msgs = await db.messages_test.find({"session_id": session_id}).sort("created_at", 1).to_list(100)
    print(f"Fetched {len(msgs)} messages")
    assert len(msgs) == 2
    # Cleanup
    await db.sessions_test.delete_one({"_id": session_id})
    await db.messages_test.delete_many({"session_id": session_id})
    client.close()
    print("PASS: Mongo persistence works")
    return True


async def test_rebuild_session_from_db():
    print("\n=== TEST 5: Rebuild context from DB messages ===")
    # Simulate: store user messages, then create new LlmChat instance using same session_id
    # and confirm we can send messages in sequence (LlmChat tracks history internally per-instance)
    session_id = str(uuid.uuid4())
    chat = make_chat(session_id, "You are a helpful assistant.")
    await chat.send_message(UserMessage(text="My name is Alice."))
    # Simulating server restart -> new instance, but same session_id (lib stores history in instance)
    # For real persistence, we rebuild by replaying history. We test by passing context in the prompt.
    chat2 = make_chat(session_id, "You are a helpful assistant. The user previously said: 'My name is Alice.'")
    r = await chat2.send_message(UserMessage(text="What is my name? Reply with just the name."))
    print(f"Response: {r}")
    assert "alice" in r.lower()
    print("PASS: Context replay strategy works")
    return True


async def main():
    print(f"EMERGENT_LLM_KEY present: {bool(EMERGENT_LLM_KEY)}")
    print(f"MONGO_URL: {MONGO_URL}")
    results = {}
    try:
        results["single_turn"] = await test_single_turn()
    except Exception as e:
        print(f"FAIL single_turn: {e}")
        results["single_turn"] = False
    try:
        results["multi_turn"] = await test_multi_turn_memory()
    except Exception as e:
        print(f"FAIL multi_turn: {e}")
        results["multi_turn"] = False
    try:
        results["providers"] = await test_provider_switch()
    except Exception as e:
        print(f"FAIL providers: {e}")
        results["providers"] = False
    try:
        results["mongo"] = await test_mongo_persistence()
    except Exception as e:
        print(f"FAIL mongo: {e}")
        results["mongo"] = False
    try:
        results["context_replay"] = await test_rebuild_session_from_db()
    except Exception as e:
        print(f"FAIL context_replay: {e}")
        results["context_replay"] = False
    print("\n\n=== FINAL RESULTS ===")
    for k, v in results.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    asyncio.run(main())
