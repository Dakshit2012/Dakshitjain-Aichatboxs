import { useEffect, useMemo, useState, useCallback } from "react";
import { ChatAPI } from "@/lib/api";
import { toast } from "sonner";
import SessionsSidebar from "@/components/chat/SessionsSidebar";
import ChatHeader from "@/components/chat/ChatHeader";
import ChatThread from "@/components/chat/ChatThread";
import Composer from "@/components/chat/Composer";
import EmptyState from "@/components/chat/EmptyState";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { Menu } from "lucide-react";
import { CHAT } from "@/constants/testIds";

export default function ChatPage() {
  const [sessions, setSessions] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [models, setModels] = useState({ openai: [], anthropic: [], gemini: [] });
  const [defaultModel, setDefaultModel] = useState({ provider: "openai", model: "gpt-5" });
  const [loadingSession, setLoadingSession] = useState(false);
  const [sending, setSending] = useState(false);
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  const activeSession = useMemo(
    () => sessions.find((s) => s.id === activeId) || null,
    [sessions, activeId]
  );

  // Initial load
  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const m = await ChatAPI.getModels();
        if (cancelled) return;
        setModels(m.models || { openai: [], anthropic: [], gemini: [] });
        if (m.default) setDefaultModel(m.default);
        const list = await ChatAPI.listSessions();
        if (cancelled) return;
        setSessions(list);
        if (list.length > 0) {
          setActiveId(list[0].id);
        }
      } catch (e) {
        toast.error("Failed to load workspace");
      }
    })();
    return () => { cancelled = true; };
  }, []);

  // Load messages when active session changes
  useEffect(() => {
    let cancelled = false;
    if (!activeId) {
      setMessages([]);
      return;
    }
    (async () => {
      setLoadingSession(true);
      try {
        const msgs = await ChatAPI.listMessages(activeId);
        if (cancelled) return;
        setMessages(msgs);
      } catch (e) {
        toast.error("Failed to load conversation");
      } finally {
        if (!cancelled) setLoadingSession(false);
      }
    })();
    return () => { cancelled = true; };
  }, [activeId]);

  const handleNewChat = useCallback(async () => {
    try {
      const s = await ChatAPI.createSession({
        title: "New conversation",
        provider: defaultModel.provider,
        model: defaultModel.model,
      });
      setSessions((prev) => [s, ...prev]);
      setActiveId(s.id);
      setMessages([]);
      setMobileSidebarOpen(false);
    } catch (e) {
      toast.error("Could not create new chat");
    }
  }, [defaultModel]);

  const handleSelectSession = (id) => {
    setActiveId(id);
    setMobileSidebarOpen(false);
  };

  const handleRename = async (id, title) => {
    try {
      const updated = await ChatAPI.updateSession(id, { title });
      setSessions((prev) => prev.map((s) => (s.id === id ? updated : s)));
      toast.success("Renamed");
    } catch {
      toast.error("Rename failed");
    }
  };

  const handleDelete = async (id) => {
    try {
      await ChatAPI.deleteSession(id);
      setSessions((prev) => prev.filter((s) => s.id !== id));
      if (activeId === id) {
        setActiveId(null);
        setMessages([]);
      }
      toast.success("Conversation deleted");
    } catch {
      toast.error("Delete failed");
    }
  };

  const handleModelChange = async (provider, model) => {
    if (!activeSession) {
      setDefaultModel({ provider, model });
      return;
    }
    try {
      const updated = await ChatAPI.updateSession(activeSession.id, { provider, model });
      setSessions((prev) => prev.map((s) => (s.id === activeSession.id ? updated : s)));
      toast.success(`Switched to ${provider} — ${model}`);
    } catch {
      toast.error("Failed to change model");
    }
  };

  const handleSend = async (text) => {
    if (!text.trim()) return;
    let sessionToUse = activeSession;
    if (!sessionToUse) {
      try {
        sessionToUse = await ChatAPI.createSession({
          title: "New conversation",
          provider: defaultModel.provider,
          model: defaultModel.model,
        });
        setSessions((prev) => [sessionToUse, ...prev]);
        setActiveId(sessionToUse.id);
      } catch {
        toast.error("Could not create session");
        return;
      }
    }
    // Optimistic user message
    const tempUser = {
      id: `temp-${Date.now()}`,
      session_id: sessionToUse.id,
      role: "user",
      content: text,
      created_at: new Date().toISOString(),
      _pending: false,
    };
    setMessages((m) => [...m, tempUser]);
    setSending(true);
    try {
      const res = await ChatAPI.sendMessage(sessionToUse.id, { text });
      // Replace temp user + append assistant
      setMessages((m) => {
        const filtered = m.filter((x) => x.id !== tempUser.id);
        return [...filtered, res.user_message, res.assistant_message];
      });
      // refresh sessions order/title
      const list = await ChatAPI.listSessions();
      setSessions(list);
    } catch (err) {
      // server returns 502 with assistant_message even on error
      if (err?.response?.data?.assistant_message) {
        const data = err.response.data;
        setMessages((m) => {
          const filtered = m.filter((x) => x.id !== tempUser.id);
          return [...filtered, data.user_message, data.assistant_message];
        });
        toast.error("AI provider returned an error");
      } else {
        setMessages((m) => m.filter((x) => x.id !== tempUser.id));
        toast.error("Could not send message");
      }
    } finally {
      setSending(false);
    }
  };

  const sidebarProps = {
    sessions,
    activeId,
    onSelect: handleSelectSession,
    onNew: handleNewChat,
    onRename: handleRename,
    onDelete: handleDelete,
  };

  return (
    <div className="relative flex h-screen w-full overflow-hidden">
      <div className="noise-overlay" aria-hidden />

      {/* Desktop sidebar */}
      <aside className="hidden md:flex md:w-[320px] shrink-0 border-r border-border bg-[hsl(var(--sidebar-bg))] z-10">
        <SessionsSidebar {...sidebarProps} />
      </aside>

      {/* Main column */}
      <main className="flex-1 flex flex-col min-w-0 relative z-10">
        <div className="flex items-center gap-2 md:hidden px-3 py-2 border-b border-border bg-[hsl(var(--background))]/80 backdrop-blur">
          <Sheet open={mobileSidebarOpen} onOpenChange={setMobileSidebarOpen}>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon" aria-label="Open menu" data-testid="open-sidebar-button">
                <Menu className="h-5 w-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="p-0 w-[320px] bg-[hsl(var(--sidebar-bg))]">
              <SessionsSidebar {...sidebarProps} />
            </SheetContent>
          </Sheet>
          <span className="font-display font-semibold text-base">Tidepaper Chat</span>
        </div>

        <ChatHeader
          session={activeSession}
          defaultModel={defaultModel}
          models={models}
          onModelChange={handleModelChange}
        />

        <div className="flex-1 min-h-0 relative">
          {!activeSession && messages.length === 0 ? (
            <EmptyState onNewChat={handleNewChat} />
          ) : (
            <ChatThread
              messages={messages}
              sending={sending}
              loading={loadingSession}
            />
          )}
        </div>

        <div className="px-4 sm:px-6 lg:px-8 pb-4 pt-2 border-t border-border bg-[hsl(var(--background))]/80 backdrop-blur">
          <div className="max-w-3xl mx-auto">
            <Composer onSend={handleSend} disabled={sending} data-testid={CHAT.composer} />
            <p className="text-[11px] text-muted-foreground mt-2 text-center">
              Tidepaper may make mistakes. Verify important information.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
