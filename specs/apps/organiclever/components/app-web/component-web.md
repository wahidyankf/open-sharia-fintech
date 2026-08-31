# Component Diagram: Next.js Frontend

Level 3 of the C4 model. Shows the logical components inside the Next.js 16 frontend container.
No authenticated screens today. The frontend is organized into 9 feature contexts
(`src/contexts/<bc>/{domain,application,infrastructure,presentation}`), with PGlite
(Postgres-WASM, IndexedDB-backed) as the local-first system of record.

## Routes

| Route                 | Owning context(s)   | Notes                            |
| --------------------- | ------------------- | -------------------------------- |
| `/`                   | landing             | Marketing page                   |
| `/app`                | (redirect)          | 308 → `/app/home`                |
| `/app/home`           | app-shell, journal  | Dashboard + quick-log FAB        |
| `/app/history`        | app-shell, stats    | Chronological entry log          |
| `/app/progress`       | app-shell, stats    | Charts and streaks               |
| `/app/settings`       | app-shell, settings | Theme, language, data export     |
| `/app/workout`        | workout-session     | Active workout (TabBar hidden)   |
| `/app/workout/finish` | workout-session     | Post-workout summary             |
| `/app/routines/edit`  | routine             | Routine editor                   |
| `/system/status/be`   | health              | Backend probe (`force-dynamic`)  |
| `/login`, `/profile`  | routing             | 404 stubs (auth not yet shipped) |

## Component Architecture

The architecture is presented as three views of one graph, split by hop so each view stays readable.
Together they carry every component and every relationship.

### View 1: Routing — End User → App Router → Feature Contexts

Thin App Router page and layout wrappers dispatch into the nine feature contexts; no business logic
lives in the router itself.

```mermaid
%% Color Palette: Blue #0173B2 | Orange #DE8F05 | Teal #029E73 | Purple #CC78BC | Brown #CA9161 | Gray #808080
graph LR
    EU("End User<br/>Desktop / Mobile"):::actor

    subgraph FE["Next.js 16 Frontend Container"]

        ROUTER["App Router<br/>────────────────<br/>Thin page+layout wrappers<br/>(no business logic)"]:::router

        subgraph SHELL["UI Shell"]
            APPSHELL["app-shell<br/>────────────────<br/>TabBar · SideNav · i18n<br/>appMachine (XState)"]:::context
        end

        subgraph SOR["System of Record"]
            JOURNAL["journal<br/>────────────────<br/>Append-only event log<br/>journalMachine (XState)<br/>4 layers"]:::context_data
        end

        subgraph DERIVED["Read-only Projections"]
            STATS["stats<br/>────────────────<br/>History · Progress<br/>3 layers (no infra)"]:::context_ro
        end

        subgraph SESSION["Active Session"]
            WORKOUT["workout-session<br/>────────────────<br/>workoutSessionMachine (XState)<br/>3 layers (no infra)"]:::context
        end

        subgraph TEMPLATES["Templates &amp; Preferences"]
            ROUTINE["routine<br/>────────────────<br/>Workout templates<br/>4 layers"]:::context_data
            SETTINGS["settings<br/>────────────────<br/>Dark mode · Language<br/>4 layers"]:::context_data
        end

        subgraph SURFACE["Static Surface &amp; Diagnostics"]
            LANDING["landing<br/>────────────────<br/>Marketing page<br/>presentation only"]:::context_ui
            ROUTING["routing<br/>────────────────<br/>404 guards<br/>presentation only"]:::context_ui
            HEALTH["health<br/>────────────────<br/>BE diagnostic<br/>infrastructure only"]:::context_infra
        end
    end

    EU --> ROUTER
    ROUTER --> APPSHELL
    ROUTER --> JOURNAL
    ROUTER --> STATS
    ROUTER --> WORKOUT
    ROUTER --> ROUTINE
    ROUTER --> SETTINGS
    ROUTER --> LANDING
    ROUTER --> ROUTING
    ROUTER --> HEALTH

    classDef actor fill:#DE8F05,stroke:#000000,color:#000000,stroke-width:2px
    classDef router fill:#CA9161,stroke:#000000,color:#000000,stroke-width:2px
    classDef context fill:#0173B2,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef context_data fill:#0173B2,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef context_ro fill:#029E73,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef context_ui fill:#CA9161,stroke:#000000,color:#000000,stroke-width:2px
    classDef context_infra fill:#808080,stroke:#000000,color:#FFFFFF,stroke-width:2px
```

### View 2: Persistence — Contexts → Shared Runtime → PGlite

Only the three contexts with an `infrastructure` layer persist. They all go through the shared
Effect TS runtime, which is the single owner of the PGlite handle.

```mermaid
%% Color Palette: Blue #0173B2 | Orange #DE8F05 | Teal #029E73 | Purple #CC78BC | Brown #CA9161 | Gray #808080
graph LR

    subgraph FE["Next.js 16 Frontend Container"]

        subgraph SOR["System of Record"]
            JOURNAL["journal<br/>────────────────<br/>Append-only event log<br/>journalMachine (XState)<br/>4 layers"]:::context_data
        end

        subgraph TEMPLATES["Templates &amp; Preferences"]
            ROUTINE["routine<br/>────────────────<br/>Workout templates<br/>4 layers"]:::context_data
            SETTINGS["settings<br/>────────────────<br/>Dark mode · Language<br/>4 layers"]:::context_data
        end

        subgraph SHARED["Shared Runtime (src/shared/)"]
            PGLITE[("PGlite<br/>────────────────<br/>Postgres-WASM<br/>IndexedDB-backed")]:::storage
            EFFECT["Effect TS · PgliteService<br/>────────────────<br/>Layer + Tag<br/>Sequences IO"]:::runtime
        end
    end

    JOURNAL --> EFFECT
    ROUTINE --> EFFECT
    SETTINGS --> EFFECT
    EFFECT --> PGLITE

    classDef context_data fill:#0173B2,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef runtime fill:#029E73,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef storage fill:#CC78BC,stroke:#000000,color:#000000,stroke-width:2px
```

### View 3: Cross-context Reads and the Backend Probe

Dotted edges are cross-context reads through the target context's public barrel. The health context
is the only component that talks to the backend.

```mermaid
%% Color Palette: Blue #0173B2 | Orange #DE8F05 | Teal #029E73 | Purple #CC78BC | Brown #CA9161 | Gray #808080
graph LR

    subgraph FE["Next.js 16 Frontend Container"]

        subgraph DERIVED["Read-only Projections"]
            STATS["stats<br/>────────────────<br/>History · Progress<br/>3 layers (no infra)"]:::context_ro
        end

        subgraph SESSION["Active Session"]
            WORKOUT["workout-session<br/>────────────────<br/>workoutSessionMachine (XState)<br/>3 layers (no infra)"]:::context
        end

        subgraph SOR["System of Record"]
            JOURNAL["journal<br/>────────────────<br/>Append-only event log<br/>journalMachine (XState)<br/>4 layers"]:::context_data
        end

        subgraph TEMPLATES["Templates &amp; Preferences"]
            ROUTINE["routine<br/>────────────────<br/>Workout templates<br/>4 layers"]:::context_data
        end

        subgraph SURFACE["Static Surface &amp; Diagnostics"]
            HEALTH["health<br/>────────────────<br/>BE diagnostic<br/>infrastructure only"]:::context_infra
        end
    end

    BE["F#/Giraffe Backend<br/>REST API"]:::external

    STATS -. "reads" .-> JOURNAL
    WORKOUT -. "persists via app barrel" .-> JOURNAL
    WORKOUT -. "reads templates" .-> ROUTINE

    HEALTH -- "server-side fetch" --> BE

    classDef context fill:#0173B2,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef context_data fill:#0173B2,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef context_ro fill:#029E73,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef context_infra fill:#808080,stroke:#000000,color:#FFFFFF,stroke-width:2px
    classDef external fill:#808080,stroke:#000000,color:#FFFFFF,stroke-width:2px,stroke-dasharray:5 5
```

**Layer rules** (enforced by ESLint `boundaries` at error severity):

- `domain` ← no project imports
- `application` ← `domain` only
- `infrastructure` ← `domain` + `application` + `@/shared/runtime`
- `presentation` ← `domain` + `application`
- Cross-context: only via the target context's `application/index.ts` or `presentation/index.ts` barrel

## Gherkin Coverage by Feature Context

Each feature context owns its Gherkin features under
[`specs/apps/organiclever/behavior/organiclever-app-web/gherkin/<bc>/`](../../behavior/organiclever-app-web/gherkin/README.md):

| Feature Context | Features                                       | Count  |
| --------------- | ---------------------------------------------- | ------ |
| app-shell       | `accessibility`, `entry-loggers`, `navigation` | 3      |
| health          | `system-status-be`                             | 1      |
| journal         | `home-screen`, `journal-mechanism`             | 2      |
| landing         | `landing`                                      | 1      |
| routine         | `routine-management`                           | 1      |
| routing         | `app-routes`, `disabled-routes`                | 2      |
| settings        | `dark-mode`, `language`, `settings-screen`     | 3      |
| stats           | `history-screen`, `progress-screen`            | 2      |
| workout-session | `workout-session`                              | 1      |
| **Total**       |                                                | **16** |

## Testing

| Level              | What                                                     | Coverage |
| ------------------ | -------------------------------------------------------- | -------- |
| `test:unit`        | Per-context steps via `vitest-cucumber`                  | >= 70%   |
| `test:integration` | Real filesystem via tmpdir fixtures                      | N/A      |
| `test:e2e`         | Full browser via Playwright (`organiclever-app-web-e2e`) | N/A      |

## Related

- **Container diagram**: [container.md](../../containers/container.md)
- **Backend component diagram**: [component-be.md](../be/component-be.md)
- **Frontend gherkin specs**: [`behavior/organiclever-app-web/gherkin/`](../../behavior/organiclever-app-web/gherkin/README.md)
- **Parent**: [organiclever specs](../../README.md)
