import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Copy, Check } from "lucide-react";
import { useState } from "react";
import { CHAT } from "@/constants/testIds";
import { cn } from "@/lib/utils";

function CopyButton({ text }) {
  const [copied, setCopied] = useState(false);
  return (
    <Button
      type="button"
      variant="ghost"
      size="sm"
      className="h-7 px-2 text-xs text-[hsl(var(--code-fg))]/80 hover:text-[hsl(var(--code-fg))]"
      data-testid={CHAT.codeCopy}
      onClick={async (e) => {
        e.stopPropagation();
        try {
          await navigator.clipboard.writeText(text);
          setCopied(true);
          setTimeout(() => setCopied(false), 1400);
        } catch {}
      }}
    >
      {copied ? <Check className="h-3 w-3 mr-1" /> : <Copy className="h-3 w-3 mr-1" />}
      {copied ? "Copied" : "Copy"}
    </Button>
  );
}

function CodeBlock({ inline, className, children, ...props }) {
  const text = String(children).replace(/\n$/, "");
  if (inline) {
    return <code className={className} {...props}>{children}</code>;
  }
  const lang = (className || "").replace("language-", "") || "text";
  return (
    <div className="my-2 rounded-xl overflow-hidden border border-border">
      <div className="flex items-center justify-between px-3 py-1.5 bg-[hsl(var(--code-bg))]/85 text-[hsl(var(--code-fg))]/80 text-[11px] font-mono">
        <span className="uppercase tracking-wider">{lang}</span>
        <CopyButton text={text} />
      </div>
      <pre className="!m-0">
        <code className={className} {...props}>{children}</code>
      </pre>
    </div>
  );
}

export default function ChatMessage({ message }) {
  const isUser = message.role === "user";
  return (
    <div
      data-testid={CHAT.message}
      className={cn("flex w-full gap-3", isUser ? "justify-end" : "justify-start")}
    >
      {!isUser && (
        <Avatar className="h-7 w-7 mt-0.5">
          <AvatarFallback className="bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] text-[11px] font-semibold">AI</AvatarFallback>
        </Avatar>
      )}
      <div
        data-testid={isUser ? CHAT.userMessage : CHAT.assistantMessage}
        className={cn(
          "max-w-[88%] rounded-2xl border px-4 py-3",
          isUser
            ? "bg-[hsl(var(--secondary))] border-border"
            : "bg-card border-border shadow-[0_1px_2px_hsl(215_28%_12%/0.06)]"
        )}
      >
        {isUser ? (
          <div className="whitespace-pre-wrap text-sm leading-relaxed">{message.content}</div>
        ) : (
          <div className="markdown-body">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeHighlight]}
              components={{ code: CodeBlock }}
            >
              {message.content || ""}
            </ReactMarkdown>
          </div>
        )}
        <div className="mt-1.5 text-[10px] text-muted-foreground/80 select-none">
          {formatTime(message.created_at)} {message.model ? `· ${message.model}` : ""}
        </div>
      </div>
      {isUser && (
        <Avatar className="h-7 w-7 mt-0.5">
          <AvatarFallback className="bg-[hsl(var(--secondary))] text-[hsl(var(--foreground))] text-[11px] font-semibold">You</AvatarFallback>
        </Avatar>
      )}
    </div>
  );
}

function formatTime(iso) {
  if (!iso) return "";
  try {
    const d = new Date(iso);
    return d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
  } catch { return ""; }
}
