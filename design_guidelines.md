{
  "design_system_name": "Tidepaper Chat (Premium SaaS Chat UI)",
  "brand_attributes": [
    "calmly premium (not flashy)",
    "developer-friendly (markdown + code first)",
    "trustworthy + precise",
    "fast + tactile micro-interactions",
    "quietly distinctive (paper + ocean accents)"
  ],
  "visual_personality": {
    "style_fusion": [
      "Claude/Perplexity-like minimal chrome + generous whitespace",
      "Swiss grid discipline (clear hierarchy, left-aligned reading flow)",
      "Soft paper surfaces + ocean/mint accents (no purple)",
      "Bento-like grouping for sidebar sections + empty states"
    ],
    "do_not": [
      "Do not center-align the whole app container.",
      "Do not use purple gradients or saturated neon gradients.",
      "Do not use heavy shadows everywhere; reserve depth for active surfaces.",
      "Do not use gradients on small UI elements (<100px)."
    ]
  },
  "inspiration_refs": {
    "layout_patterns": [
      {
        "name": "Shadcn UI Kit — AI Chat V2 (ChatGPT-style with conversation history)",
        "url": "https://adminlte.io/blog/shadcn-ui-ai-chat-templates/",
        "notes": "Use: conversation history sidebar with date groupings; header model picker; voice button pattern; upgrade banner pattern (optional)."
      },
      {
        "name": "Dribbble search — chat sidebar",
        "url": "https://dribbble.com/search/chat-sidebar",
        "notes": "Use: compact list rows, hover actions (rename/delete), subtle separators, search-in-sidebar."
      },
      {
        "name": "Muzli — chat UI inspiration",
        "url": "https://muz.li/inspiration/chat-ui/",
        "notes": "Use: composer growth, typing indicators, scroll-to-bottom affordance."
      }
    ]
  },
  "typography": {
    "google_fonts": {
      "display": {
        "family": "Space Grotesk",
        "weights": [500, 600, 700],
        "usage": "App name, page titles, section headers"
      },
      "body": {
        "family": "Figtree",
        "weights": [400, 500, 600],
        "usage": "All UI text, chat messages"
      },
      "mono": {
        "family": "IBM Plex Mono",
        "weights": [400, 500, 600],
        "usage": "Code blocks, inline code, model IDs"
      }
    },
    "tailwind_font_setup": {
      "instructions": [
        "Add Google Fonts <link> tags in public/index.html (Space Grotesk, Figtree, IBM Plex Mono).",
        "In index.css set body font-family to var(--font-body) and headings to var(--font-display).",
        "Use Tailwind utilities: font-[family-name] only if configured; otherwise rely on CSS variables."
      ]
    },
    "text_size_hierarchy": {
      "h1": "text-4xl sm:text-5xl lg:text-6xl",
      "h2": "text-base md:text-lg lg:text-lg",
      "body": "text-sm md:text-base",
      "small": "text-xs"
    },
    "type_rules": [
      "Chat message body: leading-relaxed, max-w-prose-ish (but allow code blocks full width).",
      "Sidebar titles: text-sm font-medium; timestamps: text-xs text-muted-foreground.",
      "Avoid all-caps except tiny badges (tracking-wide)."
    ]
  },
  "color_system": {
    "gradient_restriction_rule": {
      "prohibited": [
        "blue-500 to purple-600",
        "purple-500 to pink-500",
        "green-500 to blue-500",
        "red to pink"
      ],
      "rules": [
        "NEVER let gradients cover more than 20% of the viewport.",
        "NEVER apply gradients to text-heavy content or reading areas.",
        "NEVER use gradients on small UI elements (<100px width).",
        "NEVER stack multiple gradient layers in the same viewport.",
        "IF gradient area exceeds 20% OR impacts readability THEN fallback to solid colors."
      ],
      "allowed_usage": [
        "Hero/empty-state background wash (very subtle)",
        "Decorative top border / glow behind header only",
        "Large background panels only"
      ]
    },
    "palette_intent": "Paper-like neutrals + ocean blue primary + mint focus ring + sand warning. Premium, calm, readable.",
    "tokens_css_variables": {
      "notes": "These map onto shadcn HSL tokens in index.css. Keep neutrals warm (paper) and accents ocean/mint.",
      "css": ":root {\n  /* Brand fonts */\n  --font-display: 'Space Grotesk', ui-sans-serif, system-ui;\n  --font-body: 'Figtree', ui-sans-serif, system-ui;\n  --font-mono: 'IBM Plex Mono', ui-monospace, SFMono-Regular;\n\n  /* Paper neutrals (HSL) */\n  --background: 42 33% 97%;      /* paper */\n  --foreground: 215 28% 12%;     /* ink */\n  --card: 0 0% 100%;\n  --card-foreground: 215 28% 12%;\n  --popover: 0 0% 100%;\n  --popover-foreground: 215 28% 12%;\n\n  /* Ocean primary */\n  --primary: 198 55% 36%;\n  --primary-foreground: 210 40% 98%;\n\n  /* Secondary surfaces */\n  --secondary: 210 25% 96%;\n  --secondary-foreground: 215 28% 12%;\n  --muted: 210 25% 95%;\n  --muted-foreground: 215 16% 42%;\n\n  /* Accent (mint) */\n  --accent: 162 45% 92%;\n  --accent-foreground: 198 55% 26%;\n\n  /* Borders + ring */\n  --border: 214 20% 88%;\n  --input: 214 20% 88%;\n  --ring: 162 55% 45%;\n\n  /* States */\n  --destructive: 0 72% 52%;\n  --destructive-foreground: 210 40% 98%;\n\n  /* Radius */\n  --radius: 0.75rem;\n\n  /* Extra tokens (custom) */\n  --surface-2: 210 25% 98%;\n  --shadow-color: 215 28% 12%;\n  --shadow-sm: 0 1px 2px hsl(var(--shadow-color) / 0.06);\n  --shadow-md: 0 10px 30px hsl(var(--shadow-color) / 0.10);\n  --shadow-lg: 0 18px 60px hsl(var(--shadow-color) / 0.14);\n  --sidebar-bg: 210 25% 97%;\n  --sidebar-active: 162 45% 92%;\n  --code-bg: 215 28% 12%;\n  --code-fg: 210 40% 98%;\n}\n\n.dark {\n  --background: 215 28% 8%;\n  --foreground: 210 40% 98%;\n  --card: 215 28% 10%;\n  --card-foreground: 210 40% 98%;\n  --popover: 215 28% 10%;\n  --popover-foreground: 210 40% 98%;\n\n  --primary: 198 60% 55%;\n  --primary-foreground: 215 28% 10%;\n\n  --secondary: 215 22% 14%;\n  --secondary-foreground: 210 40% 98%;\n  --muted: 215 22% 14%;\n  --muted-foreground: 215 14% 70%;\n\n  --accent: 162 30% 18%;\n  --accent-foreground: 162 55% 80%;\n\n  --border: 215 18% 18%;\n  --input: 215 18% 18%;\n  --ring: 162 55% 45%;\n\n  --sidebar-bg: 215 22% 12%;\n  --sidebar-active: 162 30% 18%;\n  --code-bg: 215 28% 6%;\n  --code-fg: 210 40% 98%;\n }"
    },
    "tailwind_usage_examples": {
      "app_shell": "bg-[hsl(var(--background))] text-[hsl(var(--foreground))]",
      "sidebar": "bg-[hsl(var(--sidebar-bg))] border-r border-border",
      "active_row": "bg-[hsl(var(--sidebar-active))]",
      "focus": "focus-visible:ring-2 focus-visible:ring-[hsl(var(--ring))] focus-visible:ring-offset-2 focus-visible:ring-offset-[hsl(var(--background))]"
    }
  },
  "layout_and_grid": {
    "app_shell": {
      "desktop": "3-column: (A) icon rail optional 56px, (B) sessions sidebar 320px, (C) chat panel flex-1",
      "tablet": "2-column: sessions sidebar collapsible via Sheet; chat panel full",
      "mobile": "single column; sessions in Sheet/Drawer; header sticky; composer sticky"
    },
    "spacing": {
      "principle": "Use 2–3x more spacing than feels comfortable.",
      "chat_gutters": "px-4 sm:px-6 lg:px-8",
      "message_vertical": "py-4 sm:py-5",
      "sidebar_padding": "p-3",
      "section_gaps": "gap-2 for lists, gap-4 for panels"
    },
    "max_width": {
      "chat_content": "max-w-3xl (messages) but allow code blocks to overflow-x within bubble",
      "composer": "max-w-3xl aligned with messages"
    }
  },
  "components": {
    "component_path": {
      "shadcn_primary": "/app/frontend/src/components/ui/",
      "use_these": [
        "button.jsx",
        "card.jsx",
        "input.jsx",
        "textarea.jsx",
        "select.jsx",
        "dropdown-menu.jsx",
        "dialog.jsx",
        "alert-dialog.jsx",
        "sheet.jsx",
        "scroll-area.jsx",
        "separator.jsx",
        "tabs.jsx",
        "tooltip.jsx",
        "badge.jsx",
        "skeleton.jsx",
        "sonner.jsx"
      ]
    },
    "app_header": {
      "structure": [
        "Left: wordmark + subtle status dot",
        "Center (optional): breadcrumb / conversation title",
        "Right: model selector (Select) + settings (DropdownMenu)"
      ],
      "classes": "sticky top-0 z-30 backdrop-blur supports-[backdrop-filter]:bg-background/70 border-b border-border",
      "data_testids": {
        "model_select": "model-selector",
        "settings_menu": "settings-menu",
        "new_chat": "new-chat-button"
      }
    },
    "sidebar_sessions": {
      "elements": [
        "Search input (optional)",
        "New chat button",
        "Conversation list grouped by date (Today/Yesterday/Last 7 days)",
        "Row actions: rename, delete (DropdownMenu on hover)"
      ],
      "row_design": {
        "default": "rounded-lg px-3 py-2 hover:bg-muted transition-colors",
        "active": "bg-[hsl(var(--sidebar-active))] text-foreground",
        "title": "text-sm font-medium truncate",
        "meta": "text-xs text-muted-foreground truncate"
      },
      "data_testids": {
        "sidebar": "chat-sessions-sidebar",
        "session_row": "chat-session-row",
        "session_rename": "chat-session-rename",
        "session_delete": "chat-session-delete"
      }
    },
    "chat_thread": {
      "message_bubbles": {
        "assistant": "bg-card border border-border rounded-2xl shadow-[var(--shadow-sm)]",
        "user": "bg-[hsl(var(--secondary))] border border-border rounded-2xl",
        "avatar": "Use Avatar component; assistant avatar uses ocean dot; user uses initials",
        "content": "prose prose-slate dark:prose-invert max-w-none"
      },
      "code_blocks": {
        "container": "rounded-xl overflow-hidden border border-border",
        "header": "flex items-center justify-between px-3 py-2 bg-muted",
        "body": "bg-[hsl(var(--code-bg))] text-[hsl(var(--code-fg))] overflow-x-auto p-4 font-mono text-sm",
        "copy_button": "Button variant=ghost size=sm with Tooltip"
      },
      "data_testids": {
        "message": "chat-message",
        "assistant_message": "assistant-message",
        "user_message": "user-message",
        "code_copy": "code-block-copy-button"
      }
    },
    "composer": {
      "structure": [
        "Multiline Textarea (auto-grow up to ~160px)",
        "Left actions: attach (optional), prompt suggestions (chips)",
        "Right actions: Send button + Stop button while streaming"
      ],
      "surface": "bg-card border border-border rounded-2xl shadow-[var(--shadow-md)]",
      "classes": "sticky bottom-0 pb-4",
      "textarea_classes": "min-h-[44px] max-h-[160px] resize-none bg-transparent border-0 focus-visible:ring-0",
      "data_testids": {
        "composer": "chat-composer",
        "composer_textarea": "chat-composer-textarea",
        "composer_send": "chat-composer-send-button",
        "composer_stop": "chat-composer-stop-button"
      }
    },
    "dialogs": {
      "delete_confirm": "Use AlertDialog for delete conversation confirmation.",
      "rename_inline": "Inline rename in sidebar row using Input; confirm on Enter; cancel on Escape."
    },
    "empty_states": {
      "no_sessions": {
        "headline": "Start a new conversation",
        "body": "Choose a model and ask anything. Markdown + code supported.",
        "cta": "New chat",
        "background": "Subtle top wash gradient only (<=20% viewport) + paper texture overlay"
      },
      "no_active_session": {
        "headline": "Select a conversation",
        "body": "Or create a new one to begin.",
        "cta": "New chat"
      },
      "data_testids": {
        "empty_state": "chat-empty-state"
      }
    }
  },
  "buttons": {
    "style": "Professional / Corporate with soft geometry",
    "tokens": {
      "--btn-radius": "12px",
      "--btn-shadow": "0 1px 2px rgba(18,24,32,0.06)",
      "--btn-press-scale": "0.98"
    },
    "variants": {
      "primary": {
        "use": "Send, New chat, Confirm",
        "classes": "bg-primary text-primary-foreground hover:bg-primary/90 transition-colors",
        "focus": "focus-visible:ring-2 focus-visible:ring-[hsl(var(--ring))]"
      },
      "secondary": {
        "use": "Model selector trigger, secondary actions",
        "classes": "bg-secondary text-secondary-foreground hover:bg-secondary/80 transition-colors"
      },
      "ghost": {
        "use": "Row actions, icon buttons",
        "classes": "hover:bg-muted transition-colors"
      },
      "destructive": {
        "use": "Delete conversation",
        "classes": "bg-destructive text-destructive-foreground hover:bg-destructive/90 transition-colors"
      }
    },
    "micro_interaction": {
      "press": "active:scale-[0.98]",
      "hover": "hover:shadow-[var(--shadow-sm)] (only on primary CTAs)",
      "rule": "Never use transition-all; use transition-colors and/or transition-shadow only."
    }
  },
  "motion_and_microinteractions": {
    "library": {
      "recommended": "framer-motion",
      "install": "npm i framer-motion",
      "use_cases": [
        "Sidebar open/close (mobile Sheet)",
        "Message entrance (fade + slight y)",
        "Typing indicator dots",
        "Toast entrance handled by sonner"
      ]
    },
    "principles": [
      "Fast UI: 120–180ms for hover, 180–240ms for panel transitions.",
      "Use subtle transforms only on press; avoid constant floating animations.",
      "Respect prefers-reduced-motion: disable message entrance animations."
    ],
    "snippets_js": {
      "message_enter": "// Example (React .js)\nimport { motion } from 'framer-motion';\n\nexport function ChatMessage({ children }) {\n  return (\n    <motion.div\n      initial={{ opacity: 0, y: 6 }}\n      animate={{ opacity: 1, y: 0 }}\n      transition={{ duration: 0.18 }}\n    >\n      {children}\n    </motion.div>\n  );\n}\n"
    }
  },
  "markdown_and_code": {
    "recommended_libs": [
      {
        "name": "react-markdown",
        "install": "npm i react-markdown",
        "usage": "Render assistant messages with markdown."
      },
      {
        "name": "rehype-highlight",
        "install": "npm i rehype-highlight highlight.js",
        "usage": "Syntax highlighting for code blocks."
      }
    ],
    "code_theme": {
      "note": "Prefer a neutral dark code surface even in light mode (like many premium dev tools).",
      "classes": "bg-[hsl(var(--code-bg))] text-[hsl(var(--code-fg))]"
    }
  },
  "accessibility": {
    "requirements": [
      "All controls keyboard reachable; visible focus ring using --ring.",
      "Ensure contrast: body text on paper background >= WCAG AA.",
      "Use aria-label for icon-only buttons.",
      "Use reduced motion preference to disable entrance animations.",
      "Provide screen-reader text for model selector and session actions."
    ]
  },
  "testing_attributes": {
    "rule": "All interactive and key informational elements MUST include data-testid (kebab-case, role-based).",
    "minimum_set": [
      "model-selector",
      "new-chat-button",
      "chat-sessions-sidebar",
      "chat-session-row",
      "chat-session-delete",
      "chat-session-rename",
      "chat-thread",
      "chat-message",
      "chat-composer",
      "chat-composer-textarea",
      "chat-composer-send-button",
      "chat-composer-stop-button",
      "chat-empty-state",
      "delete-session-confirm-button",
      "delete-session-cancel-button"
    ]
  },
  "image_urls": {
    "background_texture": [
      {
        "category": "paper-grain",
        "description": "Use as subtle fixed/no-repeat overlay at 6–10% opacity on the app background (not on cards).",
        "url": "https://images.pexels.com/photos/7599590/pexels-photo-7599590.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
      }
    ],
    "optional_illustrations": [
      {
        "category": "empty-state",
        "description": "If you want an illustration, keep it monochrome line art or very low-saturation; avoid loud mascots.",
        "url": "(optional)"
      }
    ]
  },
  "implementation_notes": {
    "instructions_to_main_agent": [
      "Replace CRA default App.css styles; remove .App-header centering patterns.",
      "Update /app/frontend/src/index.css :root HSL tokens to the Tidepaper palette above; keep shadcn variable structure.",
      "Use shadcn ScrollArea for sidebar list and chat thread scroll container.",
      "Use Sheet for mobile sidebar; keep desktop sidebar always visible.",
      "Composer: sticky bottom; align width with message column; auto-grow textarea; include Send + Stop states.",
      "Conversation row actions must appear on hover/focus (keyboard accessible) via DropdownMenu.",
      "Use Sonner for toasts (rename success, delete success, error states).",
      "Ensure every interactive element has data-testid per rules.",
      "No universal transition-all anywhere; only transition-colors/shadow/opacity."
    ],
    "extra_css_utilities": {
      "noise_overlay": "/* Add to index.css */\n.noise-overlay {\n  pointer-events: none;\n  position: fixed;\n  inset: 0;\n  opacity: 0.08;\n  mix-blend-mode: multiply;\n  background-image: url('https://images.pexels.com/photos/7599590/pexels-photo-7599590.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940');\n  background-size: 900px 900px;\n  background-repeat: repeat;\n}\n",
      "subtle_top_wash": "/* Use on empty state wrapper only */\n.bg-top-wash {\n  background: radial-gradient(1200px 400px at 20% 0%, rgba(58,147,189,0.14), transparent 60%),\n              radial-gradient(900px 360px at 80% 0%, rgba(63,185,138,0.10), transparent 55%);\n}\n"
    }
  },
  "general_ui_ux_design_guidelines_appendix": "<General UI UX Design Guidelines>\n    - You must **not** apply universal transition. Eg: `transition: all`. This results in breaking transforms. Always add transitions for specific interactive elements like button, input excluding transforms\n    - You must **not** center align the app container, ie do not add `.App { text-align: center; }` in the css file. This disrupts the human natural reading flow of text\n   - NEVER: use AI assistant Emoji characters like`🤖🧠💭💡🔮🎯📚🎭🎬🎪🎉🎊🎁🎀🎂🍰🎈🎨🎰💰💵💳🏦💎🪙💸🤑📊📈📉💹🔢🏆🥇 etc for icons. Always use **FontAwesome cdn** or **lucid-react** library already installed in the package.json\n\n **GRADIENT RESTRICTION RULE**\nNEVER use dark/saturated gradient combos (e.g., purple/pink) on any UI element.  Prohibited gradients: blue-500 to purple 600, purple 500 to pink-500, green-500 to blue-500, red to pink etc\nNEVER use dark gradients for logo, testimonial, footer etc\nNEVER let gradients cover more than 20% of the viewport.\nNEVER apply gradients to text-heavy content or reading areas.\nNEVER use gradients on small UI elements (<100px width).\nNEVER stack multiple gradient layers in the same viewport.\n\n**ENFORCEMENT RULE:**\n    • Id gradient area exceeds 20% of viewport OR affects readability, **THEN** use solid colors\n\n**How and where to use:**\n   • Section backgrounds (not content backgrounds)\n   • Hero section header content. Eg: dark to light to dark color\n   • Decorative overlays and accent elements only\n   • Hero section with 2-3 mild color\n   • Gradients creation can be done for any angle say horizontal, vertical or diagonal\n\n- For AI chat, voice application, **do not use purple color. Use color like light green, ocean blue, peach orange etc**\n\n</Font Guidelines>\n\n- Every interaction needs micro-animations - hover states, transitions, parallax effects, and entrance animations. Static = dead. \n   \n- Use 2-3x more spacing than feels comfortable. Cramped designs look cheap.\n\n- Subtle grain textures, noise overlays, custom cursors, selection states, and loading animations: separates good from extraordinary.\n   \n- Before generating UI, infer the visual style from the problem statement (palette, contrast, mood, motion) and immediately instantiate it by setting global design tokens (primary, secondary/accent, background, foreground, ring, state colors), rather than relying on any library defaults. Don't make the background dark as a default step, always understand problem first and define colors accordingly\n    Eg: - if it implies playful/energetic, choose a colorful scheme\n           - if it implies monochrome/minimal, choose a black–white/neutral scheme\n\n**Component Reuse:**\n\t- Prioritize using pre-existing components from src/components/ui when applicable\n\t- Create new components that match the style and conventions of existing components when needed\n\t- Examine existing components to understand the project's component patterns before creating new ones\n\n**IMPORTANT**: Do not use HTML based component like dropdown, calendar, toast etc. You **MUST** always use `/app/frontend/src/components/ui/ ` only as a primary components as these are modern and stylish component\n\n**Best Practices:**\n\t- Use Shadcn/UI as the primary component library for consistency and accessibility\n\t- Import path: ./components/[component-name]\n\n**Export Conventions:**\n\t- Components MUST use named exports (export const ComponentName = ...)\n\t- Pages MUST use default exports (export default function PageName() {...})\n\n**Toasts:**\n  - Use `sonner` for toasts\"\n  - Sonner component are located in `/app/src/components/ui/sonner.tsx`\n\nUse 2–4 color gradients, subtle textures/noise overlays, or CSS-based noise to avoid flat visuals.\n</General UI UX Design Guidelines>"
}
