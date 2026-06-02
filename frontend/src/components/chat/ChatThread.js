import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import ChatMessage from "@/components/chat/ChatMessage";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Skeleton } from "@/components/ui/skeleton";
import { CHAT } from "@/constants/testIds";

export default function ChatThread({ messages, sending, loading }) {
  const bottomRef = useRef(null);
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages.length, sending]);

  return (
    <ScrollArea className="h-full w-full scroll-soft">
      <div
        className="px-4 sm:px-6 lg:px-8 py-6 max-w-3xl mx-auto flex flex-col gap-5"
        data-testid={CHAT.thread}
      >
        {loading && (
          <div className="flex flex-col gap-4 pt-4">
            <Skeleton className="h-4 w-40" />
            <Skeleton className="h-20 w-full rounded-2xl" />
            <Skeleton className="h-4 w-24 self-end" />
            <Skeleton className="h-16 w-2/3 self-end rounded-2xl" />
          </div>
        )}

        {!loading && messages.length === 0 && (
          <div className="py-10 text-center text-sm text-muted-foreground">
            Send a message to begin this conversation.
          </div>
        )}

        <AnimatePresence initial={false}>
          {messages.map((m) => (
            <motion.div
              key={m.id}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.18 }}
            >
              <ChatMessage message={m} />
            </motion.div>
          ))}
        </AnimatePresence>

        {sending && (
          <div className="flex items-center gap-3" aria-live="polite">
            <div className="h-7 w-7 rounded-full bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] flex items-center justify-center text-xs font-semibold">AI</div>
            <div className="rounded-2xl border border-border bg-card px-3 py-2">
              <span className="typing-dot" /><span className="typing-dot" /><span className="typing-dot" />
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>
    </ScrollArea>
  );
}
