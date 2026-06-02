import { Button } from "@/components/ui/button";
import { Plus, Sparkles, Code2, BookOpen, MessageSquare } from "lucide-react";
import { CHAT } from "@/constants/testIds";

const PROMPTS = [
  { icon: Code2, title: "Explain a code snippet", body: "Paste code and ask the model to explain or refactor it." },
  { icon: BookOpen, title: "Summarize a document", body: "Paste long-form text and ask for a structured summary." },
  { icon: MessageSquare, title: "Brainstorm ideas", body: "Generate creative ideas, names, or strategies." },
  { icon: Sparkles, title: "Learn anything", body: "Ask any technical or general-knowledge question." },
];

export default function EmptyState({ onNewChat }) {
  return (
    <div
      className="h-full w-full overflow-auto bg-top-wash"
      data-testid={CHAT.empty}
    >
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-16">
        <div className="flex items-center gap-3 mb-3">
          <div className="h-10 w-10 rounded-xl bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] flex items-center justify-center">
            <Sparkles className="h-5 w-5" />
          </div>
          <div>
            <h2 className="font-display font-semibold text-2xl sm:text-3xl leading-tight">Welcome to Tidepaper</h2>
            <p className="text-sm text-muted-foreground">A premium AI chat workspace powered by leading LLMs.</p>
          </div>
        </div>

        <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-3">
          {PROMPTS.map(({ icon: Icon, title, body }) => (
            <div
              key={title}
              className="rounded-2xl border border-border bg-card p-4 hover:shadow-[0_1px_2px_hsl(215_28%_12%/0.06)] transition-shadow"
            >
              <div className="flex items-center gap-2 mb-1">
                <Icon className="h-4 w-4 text-[hsl(var(--primary))]" />
                <div className="text-sm font-medium">{title}</div>
              </div>
              <div className="text-xs text-muted-foreground leading-relaxed">{body}</div>
            </div>
          ))}
        </div>

        <div className="mt-8">
          <Button onClick={onNewChat} className="gap-2" data-testid={CHAT.newChat + "-empty"}>
            <Plus className="h-4 w-4" /> Start a new chat
          </Button>
        </div>

        <div className="mt-12 text-[11px] text-muted-foreground">
          Tip: Use the model selector in the top right to switch between GPT, Claude, and Gemini.
        </div>
      </div>
    </div>
  );
}
