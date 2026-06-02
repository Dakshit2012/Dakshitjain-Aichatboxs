import { useState } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem,
} from "@/components/ui/dropdown-menu";
import {
  AlertDialog, AlertDialogTrigger, AlertDialogContent, AlertDialogHeader, AlertDialogTitle,
  AlertDialogDescription, AlertDialogFooter, AlertDialogCancel, AlertDialogAction,
} from "@/components/ui/alert-dialog";
import { Plus, MoreHorizontal, Pencil, Trash2, MessageSquare, Sparkles } from "lucide-react";
import { CHAT } from "@/constants/testIds";
import { formatRelativeGroup } from "@/lib/dates";
import { cn } from "@/lib/utils";

export default function SessionsSidebar({
  sessions, activeId, onSelect, onNew, onRename, onDelete,
}) {
  const [renamingId, setRenamingId] = useState(null);
  const [renameValue, setRenameValue] = useState("");

  const groups = groupByDate(sessions);

  const startRename = (s) => {
    setRenamingId(s.id);
    setRenameValue(s.title);
  };
  const commitRename = (s) => {
    const v = renameValue.trim();
    if (v && v !== s.title) onRename(s.id, v);
    setRenamingId(null);
  };

  return (
    <div
      className="flex flex-col w-full h-full"
      data-testid={CHAT.sidebar}
    >
      {/* Brand */}
      <div className="px-4 py-4 flex items-center gap-2 border-b border-border">
        <div className="h-8 w-8 rounded-lg bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] flex items-center justify-center">
          <Sparkles className="h-4 w-4" />
        </div>
        <div className="flex-1">
          <div className="font-display font-semibold leading-tight">Tidepaper</div>
          <div className="text-[11px] text-muted-foreground -mt-0.5">AI chat workspace</div>
        </div>
      </div>

      {/* New chat */}
      <div className="p-3">
        <Button
          onClick={onNew}
          className="w-full justify-start gap-2 active:scale-[0.99]"
          data-testid={CHAT.newChat}
        >
          <Plus className="h-4 w-4" />
          New chat
        </Button>
      </div>

      <ScrollArea className="flex-1 px-2">
        <div className="px-1 pb-6">
          {sessions.length === 0 && (
            <div className="text-center text-xs text-muted-foreground py-10 px-3">
              No conversations yet. Start a new chat to begin.
            </div>
          )}
          {groups.map((group) => (
            <div key={group.label} className="mb-3">
              <div className="px-3 pt-3 pb-1 text-[10px] uppercase tracking-wider text-muted-foreground">
                {group.label}
              </div>
              <ul className="flex flex-col gap-0.5">
                {group.items.map((s) => {
                  const isActive = s.id === activeId;
                  const isRenaming = renamingId === s.id;
                  return (
                    <li key={s.id}>
                      <div
                        data-testid={CHAT.sessionRow}
                        className={cn(
                          "group flex items-center gap-2 rounded-lg px-3 py-2 cursor-pointer transition-colors",
                          isActive ? "bg-[hsl(var(--sidebar-active))]" : "hover:bg-muted"
                        )}
                        onClick={() => !isRenaming && onSelect(s.id)}
                      >
                        <MessageSquare className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
                        {isRenaming ? (
                          <Input
                            autoFocus
                            value={renameValue}
                            onChange={(e) => setRenameValue(e.target.value)}
                            onBlur={() => commitRename(s)}
                            onKeyDown={(e) => {
                              if (e.key === "Enter") commitRename(s);
                              if (e.key === "Escape") setRenamingId(null);
                            }}
                            className="h-7 text-sm py-1"
                            data-testid={CHAT.sessionRename + "-input"}
                          />
                        ) : (
                          <div className="flex-1 min-w-0">
                            <div className="text-sm font-medium truncate">{s.title || "Untitled"}</div>
                            <div className="text-[11px] text-muted-foreground truncate">
                              {s.provider} · {s.model}
                            </div>
                          </div>
                        )}
                        {!isRenaming && (
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button
                                variant="ghost"
                                size="icon"
                                className="h-7 w-7 opacity-0 group-hover:opacity-100 focus:opacity-100"
                                aria-label="Row actions"
                                onClick={(e) => e.stopPropagation()}
                              >
                                <MoreHorizontal className="h-4 w-4" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end" className="w-40">
                              <DropdownMenuItem
                                data-testid={CHAT.sessionRename}
                                onClick={(e) => { e.stopPropagation(); startRename(s); }}
                              >
                                <Pencil className="h-3.5 w-3.5 mr-2" /> Rename
                              </DropdownMenuItem>
                              <AlertDialog>
                                <AlertDialogTrigger asChild>
                                  <DropdownMenuItem
                                    data-testid={CHAT.sessionDelete}
                                    className="text-destructive focus:text-destructive"
                                    onClick={(e) => e.stopPropagation()}
                                    onSelect={(e) => e.preventDefault()}
                                  >
                                    <Trash2 className="h-3.5 w-3.5 mr-2" /> Delete
                                  </DropdownMenuItem>
                                </AlertDialogTrigger>
                                <AlertDialogContent>
                                  <AlertDialogHeader>
                                    <AlertDialogTitle>Delete conversation?</AlertDialogTitle>
                                    <AlertDialogDescription>
                                      “{s.title}” and all its messages will be permanently deleted.
                                    </AlertDialogDescription>
                                  </AlertDialogHeader>
                                  <AlertDialogFooter>
                                    <AlertDialogCancel data-testid={CHAT.deleteCancel}>Cancel</AlertDialogCancel>
                                    <AlertDialogAction
                                      onClick={() => onDelete(s.id)}
                                      className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                                      data-testid={CHAT.deleteConfirm}
                                    >
                                      Delete
                                    </AlertDialogAction>
                                  </AlertDialogFooter>
                                </AlertDialogContent>
                              </AlertDialog>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        )}
                      </div>
                    </li>
                  );
                })}
              </ul>
            </div>
          ))}
        </div>
      </ScrollArea>

      <div className="px-4 py-3 border-t border-border text-[11px] text-muted-foreground">
        Powered by Emergent LLM · v1
      </div>
    </div>
  );
}

function groupByDate(sessions) {
  const today = [], yesterday = [], week = [], earlier = [];
  const now = new Date();
  for (const s of sessions) {
    const d = new Date(s.updated_at || s.created_at);
    const diff = (now - d) / (1000 * 60 * 60 * 24);
    if (sameDay(now, d)) today.push(s);
    else if (diff < 2 && d.getDate() === now.getDate() - 1) yesterday.push(s);
    else if (diff < 7) week.push(s);
    else earlier.push(s);
  }
  const groups = [];
  if (today.length) groups.push({ label: "Today", items: today });
  if (yesterday.length) groups.push({ label: "Yesterday", items: yesterday });
  if (week.length) groups.push({ label: "Last 7 days", items: week });
  if (earlier.length) groups.push({ label: "Earlier", items: earlier });
  return groups;
}
function sameDay(a, b) {
  return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
}
// keep imports used
export { formatRelativeGroup };
