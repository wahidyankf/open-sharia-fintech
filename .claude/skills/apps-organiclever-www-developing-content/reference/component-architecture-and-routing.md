# organiclever-www — Component Architecture and Next.js App Router Conventions

## Component Architecture

Components live inside the bounded context that owns them, not in a global `src/components/` folder.

### Where Components Live

- **Context-owned**: `src/contexts/<bc>/presentation/components/` — components that belong to a specific bounded context
- **Shared primitives**: `@open-sharia-enterprise/web-ui` — the shared design system library. Import from here, not from `src/`
- **App routing chrome**: `src/app/` — Next.js `page.tsx` and `layout.tsx` thin wrappers only; no business logic

```typescript
// Correct — import from bounded context barrel
import { JournalList } from "@/contexts/journal/presentation";
import { HistoryScreen } from "@/contexts/stats/presentation";

// Correct — import from web-ui design system
import { Button, StatCard, TabBar } from "@open-sharia-enterprise/web-ui";

// Wrong — no global src/components/ exists
import { SomeComponent } from "@/components/SomeComponent"; // ❌
```

### Server vs Client Components

**Default**: Server Components (no `"use client"` directive needed)

**Use Client Components when**:

- Interactive state (`useState`, `useReducer`, XState `useActor`)
- Browser APIs (IndexedDB, window, localStorage)
- Event handlers (`onClick`, `onChange`)
- React context consumers

The app layout mounts the PGlite runtime and XState `appMachine` in a client component (`app-runtime-context.tsx`). Per-tab `page.tsx` files are server components that render client presentation components.

## Next.js App Router Conventions

### Route Structure

```
src/app/
├── layout.tsx                  # Root layout — loads fonts, globals.css
├── page.tsx                    # Landing page (/) — server component
├── app/
│   ├── layout.tsx              # App shell layout — mounts PGlite runtime + appMachine
│   ├── home/page.tsx           # Home screen (/app/home)
│   ├── history/page.tsx        # History screen (/app/history)
│   ├── progress/page.tsx       # Progress screen (/app/progress)
│   ├── settings/page.tsx       # Settings screen (/app/settings)
│   ├── workout/page.tsx        # Active workout (/app/workout)
│   ├── workout/finish/page.tsx # Post-workout summary (/app/workout/finish)
│   └── routines/edit/page.tsx  # Routine editor (/app/routines/edit)
└── system/status/be/page.tsx   # Diagnostic page (force-dynamic, no cache)
```

Every `page.tsx` is a thin wrapper — it imports from the relevant bounded context's `presentation/` barrel and renders the screen component. No business logic in `page.tsx`.
