import { useMemo } from "react";
import {
  Select, SelectTrigger, SelectValue, SelectContent, SelectGroup, SelectLabel, SelectItem,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Bot } from "lucide-react";
import { CHAT } from "@/constants/testIds";

const PROVIDER_LABEL = {
  openai: "OpenAI",
  anthropic: "Anthropic",
  gemini: "Google Gemini",
};

export default function ChatHeader({ session, defaultModel, models, onModelChange }) {
  const current = session
    ? { provider: session.provider, model: session.model }
    : defaultModel;

  const selectValue = `${current.provider}::${current.model}`;

  const options = useMemo(() => {
    const out = [];
    Object.entries(models || {}).forEach(([provider, list]) => {
      out.push({ provider, list: list || [] });
    });
    return out;
  }, [models]);

  const handleChange = (val) => {
    const [provider, model] = val.split("::");
    onModelChange(provider, model);
  };

  return (
    <header className="sticky top-0 z-20 flex items-center gap-3 px-4 sm:px-6 lg:px-8 py-3 border-b border-border bg-[hsl(var(--background))]/80 backdrop-blur supports-[backdrop-filter]:bg-[hsl(var(--background))]/60">
      <div className="hidden md:flex items-center gap-2">
        <div className="h-2 w-2 rounded-full bg-[hsl(var(--ring))]" aria-hidden />
        <h1 className="font-display font-semibold text-base">
          {session?.title || "New conversation"}
        </h1>
      </div>
      <div className="flex-1" />
      <div className="flex items-center gap-2">
        <Badge variant="secondary" className="hidden sm:inline-flex gap-1.5 font-normal">
          <Bot className="h-3 w-3" />
          <span>{PROVIDER_LABEL[current.provider] || current.provider}</span>
        </Badge>
        <Select value={selectValue} onValueChange={handleChange}>
          <SelectTrigger
            className="w-[220px] h-9 text-sm"
            data-testid={CHAT.modelSelect}
          >
            <SelectValue placeholder="Choose a model" />
          </SelectTrigger>
          <SelectContent className="max-h-[360px]">
            {options.map(({ provider, list }) => (
              <SelectGroup key={provider}>
                <SelectLabel className="text-[11px] uppercase tracking-wider">
                  {PROVIDER_LABEL[provider] || provider}
                </SelectLabel>
                {list.map((m) => (
                  <SelectItem key={`${provider}::${m}`} value={`${provider}::${m}`}>
                    {m}
                  </SelectItem>
                ))}
              </SelectGroup>
            ))}
          </SelectContent>
        </Select>
      </div>
    </header>
  );
}
