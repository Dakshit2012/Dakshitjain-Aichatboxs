# plan.md

## 1. Objectives
- Deliver a **production-quality v1 chatbot** (FastAPI + React + MongoDB) using **Emergent Universal LLM Key** with a **model picker** (GPT/Claude/Gemini).
- Prove the **core workflow** works end-to-end: **create session → send message → stream AI reply → persist messages → resume session**.
- Provide a polished UX: **modern dark theme**, smooth interactions, **Markdown + code highlighting**, and reliable error handling.

---

## 2. Implementation Steps

### Phase 1 — Core LLM Integration POC (Isolation)
**Goal:** Validate LLM calls + streaming + session continuity before building the app.

**User stories (Phase 1)**
1. As a user, I can send a prompt and receive a valid model response.
2. As a user, I see the response **stream token-by-token**.
3. As a user, the assistant remembers prior messages when I send a follow-up.
4. As a user, I can switch models (GPT/Claude/Gemini) and still get a response.
5. As a user, I get a clear error message when the provider/model is unavailable.

**Steps**
- Websearch / quick review: best practices for **SSE streaming** from FastAPI + React and emergentintegrations usage patterns.
- Create `poc_llm.py`:
  - Call emergentintegrations chat completion (non-streaming) and validate output shape.
  - Call streaming variant and print incremental chunks.
  - Include a minimal in-memory message list to verify continuity.
  - Add model parameter (e.g., `gpt-*`, `claude-*`, `gemini-*`).
- Add `poc_mongo.py` (optional but recommended):
  - Write/read a session + messages in MongoDB; verify ordering + timestamps.
- **Fix until stable**:
  - Robust parsing of streamed events.
  - Timeouts/retries and graceful fallbacks.
  - Confirm session continuation produces context-aware answers.

**Exit criteria (Phase 1)**
- Streaming works reliably; follow-ups demonstrate memory; at least 2 providers/models verified.

---

### Phase 2 — V1 App Development (Build around proven core)
**Goal:** Implement the full MVP with session CRUD, message persistence, streaming chat endpoint, and polished UI.

**User stories (Phase 2)**
1. As a user, I can start a new chat and it appears in the sidebar.
2. As a user, AI responses stream in real-time with a typing indicator.
3. As a user, my messages and AI replies are auto-saved and restored on refresh.
4. As a user, I can rename or delete a conversation.
5. As a user, I can switch LLM models per conversation (or per message).
6. As a user, Markdown renders correctly and code blocks are syntax-highlighted.

**Backend (FastAPI + MongoDB)**
- Data model (Mongo):
  - `sessions`: `{_id, title, model, created_at, updated_at}`
  - `messages`: `{_id, session_id, role, content, created_at, tokens?, provider?}`
- REST endpoints:
  - `POST /api/sessions` (create, default title)
  - `GET /api/sessions` (list recent)
  - `PATCH /api/sessions/{id}` (rename, set model)
  - `DELETE /api/sessions/{id}` (delete + cascade messages)
  - `GET /api/sessions/{id}/messages` (history)
  - `POST /api/sessions/{id}/messages` (non-streaming send)
  - `POST /api/sessions/{id}/stream` (SSE streaming send)
- LLM service layer:
  - Provider/model abstraction using Emergent key.
  - Build prompt from persisted messages (role-based).
  - Streaming via SSE; also store assistant message at end.
- Reliability:
  - Input validation, max message length, basic rate limiting knobs.
  - Structured error responses; log correlation IDs.

**Frontend (React + Tailwind + shadcn/ui)**
- Layout:
  - Left sidebar: sessions list + new chat + rename/delete.
  - Main panel: message list + composer + model selector.
- Chat UX:
  - Streaming renderer (append tokens), stop button (optional v1).
  - Markdown rendering + code highlighting.
  - Auto-scroll with “jump to latest” when user scrolls up.
  - Empty states, loading skeletons, toasts on errors.
- Styling:
  - Dark theme, gradient accents, subtle motion (Framer Motion optional).

**End-of-phase testing (Phase 2)**
- Run one end-to-end pass: create session → send → stream → refresh → history intact → rename/delete.
- Verify markdown/code highlighting and model switching.

---

### Phase 3 — Hardening + Secondary Features
**Goal:** Improve robustness and UX polish based on real behavior.

**User stories (Phase 3)**
1. As a user, I can regenerate the last response if it was unsatisfactory.
2. As a user, I can edit my last message and resend.
3. As a user, I can search my conversations.
4. As a user, I can export a conversation (Markdown/JSON).
5. As a user, the app remains responsive under slow networks and large histories.

**Steps**
- Conversation utilities: regenerate, edit/resend (message versioning or replace-last).
- Performance: pagination/virtualized message list; truncate context window with summary stub (optional).
- Observability: structured logs; basic metrics; better error boundaries.
- Security basics: sanitize markdown rendering, CORS tightening.
- Testing: expand E2E coverage; add API tests for session/message endpoints.

---

### Phase 4 — Optional: Authentication + Multi-user
**Goal:** Add accounts only after core UX is validated (auth complicates testing).

**User stories (Phase 4)**
1. As a user, I can sign up and log in securely.
2. As a user, I only see my own conversations.
3. As a user, I can manage my profile and API usage settings.
4. As a user, my sessions sync across devices.
5. As a user, I can delete my account and data.

**Steps**
- JWT auth (email/password) or OAuth (if requested) + per-user data partitioning.
- Rate limits/quotas per user.
- Re-test all flows under authenticated context.

---

## 3. Next Actions
- Confirm model names to expose in the picker (default: GPT + Claude + Gemini latest).
- Execute Phase 1 POC scripts (LLM streaming + continuity; Mongo persistence).
- Once Phase 1 exit criteria pass, scaffold backend + frontend and implement Phase 2 in one integrated build.

---

## 4. Success Criteria
- Core loop works reliably: **session created, messages persist, streaming response renders, session resumes**.
- UI is polished: responsive layout, clear states, markdown + highlighted code blocks.
- Model switching works and errors are handled gracefully.
- No data loss on refresh; delete/rename operations consistent.
- End-to-end tests (manual + basic automated) pass without regressions.
