import { useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ArrowUp } from "lucide-react";
import { CHAT } from "@/constants/testIds";

export default function Composer({ onSend, disabled }) {
  const [value, setValue] = useState("");
  const taRef = useRef(null);

  useEffect(() => {
    if (!taRef.current) return;
    taRef.current.style.height = "auto";
    const next = Math.min(taRef.current.scrollHeight, 200);
    taRef.current.style.height = `${next}px`;
  }, [value]);

  const submit = () => {
    if (disabled) return;
    const v = value.trim();
    if (!v) return;
    onSend(v);
    setValue("");
  };

  const onKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  return (
    <div
      className="flex items-end gap-2 rounded-2xl border border-border bg-card px-3 py-2 shadow-[0_10px_30px_hsl(215_28%_12%/0.08)]"
      data-testid={CHAT.composer}
    >
      <Textarea
        ref={taRef}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={onKeyDown}
        placeholder="Message Tidepaper… (Shift+Enter for new line)"
        rows={1}
        className="min-h-[40px] max-h-[200px] resize-none border-0 bg-transparent focus-visible:ring-0 px-2 py-2 leading-relaxed"
        data-testid={CHAT.composerTextarea}
        disabled={disabled}
      />
      <Button
        type="button"
        onClick={submit}
        disabled={disabled || !value.trim()}
        size="icon"
        className="h-9 w-9 rounded-xl shrink-0 active:scale-[0.97]"
        aria-label="Send message"
        data-testid={CHAT.composerSend}
      >
        <ArrowUp className="h-4 w-4" />
      </Button>
    </div>
  );
}
