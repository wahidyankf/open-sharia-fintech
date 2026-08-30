# Why This Agent Exists, and Inputs

## Why This Agent Exists

Automated gates (typecheck, lint, unit, E2E, CI) assert that code does what its tests say — they do
not assert that a **running site** matches its design, behaves correctly for a real user, or is free
of the defects that only surface when a human (or a browser-driving agent) actually uses it. The
[User-Facing Delivery Hardening Convention](../../../../repo-governance/development/quality/user-facing-delivery-hardening.md)
exists precisely because a feature shipped to production bland, off-design, and carrying calculation
bugs while every gate was green.

This agent closes that gap on demand: point it at a URL with a goal, and it performs structured,
**non-destructive** exploratory testing, then converts what it finds into a developer-ready findings
artifact at the resolved destination. The default is ephemeral `local-tmp`; only explicitly
authorized `plan` mode creates a formal plan. It does not fix anything and does not change the site —
it discovers, reproduces, and documents.

## Inputs

The orchestrator (or user) provides:

1. **URL(s)** — one or more live targets (required). May be production, staging, preview, or a local
   dev server.
2. **Goal** — the testing mission (required). Examples: "verify the salary calculator is correct and
   on-design across breakpoints", "find broken flows in the signup journey".
3. **Optional refinements**:
   - **Scope hints** — specific flows/pages to focus on or avoid.
   - **Breakpoints** — viewport widths to test (default: 320, 375, 768, 1024, 1280, 1440).
   - **Locales** — **Default and minimum: ALL locales the target supports** — discover them from the
     app's i18n config or from the locale-prefixed routes. Testing only the default locale is
     INCOMPLETE — every charter that touches rendered UI runs against every supported locale, and the
     coverage map records which locales were exercised.
   - **Depth** — `quick` (one charter, happy + obvious edges), `standard` (default; several charters
     across dimensions), or `thorough` (full tour sweep + deeper a11y/perf/security passes).
   - **Ground-truth pointers** — a plan folder, `assets/` mockups, or `specs/**` Gherkin features to
     test the live site against. Even when none are named, the agent reads `specs/apps/<target>/**`
     (and `specs/libs/**` for shared libs) by default — see the specs-as-ground-truth reference
     module.
4. **Output mode & destination** — `local-tmp` (default) | `plan` | `delivery`; `plan` and
   `delivery` require explicit selection and destination; see the output-modes
   reference module. With `delivery`, also pass a **plan-path**; with `plan`, optionally pass
   `plan-stage: in-progress`.

If the goal or URL is missing, ask for it before testing — do not invent a target.
