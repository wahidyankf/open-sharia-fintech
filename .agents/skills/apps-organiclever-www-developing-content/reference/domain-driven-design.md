# organiclever-www — Domain-Driven Design

`apps/organiclever-www` follows Domain-Driven Design. The bounded-context map is canonical at:

- **Registry**: [`specs/apps/organiclever/ddd/bounded-contexts.yaml`](../../../../specs/apps/organiclever/ddd/bounded-contexts.yaml)
- **Glossaries**: `specs/apps/organiclever/ddd/ubiquitous-language/<bc>.md`
- **Design intent (full prose)**: [`plans/done/2026-05-03__organiclever-adopt-ddd/tech-docs.md`](../../../../plans/done/2026-05-03__organiclever-adopt-ddd/tech-docs.md)
- **ADR**: [`specs/apps/organiclever/ddd/bounded-context-map.md`](../../../../specs/apps/organiclever/ddd/bounded-context-map.md)
- **Enforcement**: [`apps/rhino-cli/README.md`](../../../../apps/rhino-cli/README.md) — `rhino-cli specs structure validate` (its `bc:` and `ul:` layers)

## Bounded Contexts

See the registry for the canonical list. Currently 9: `journal`, `workout-session`, `routine`, `stats`, `settings`, `app-shell`, `health`, `landing`, `routing`.

## Layer Rules (Concise)

| Layer            | Imports allowed                                                                    | Imports forbidden                                                  |
| ---------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `domain`         | own `domain/`, `shared/utils/**`                                                   | anything in `application/`, `infrastructure/`, `presentation/`     |
| `application`    | own `domain/`, own `infrastructure/` ports, other contexts' `application/index.ts` | other contexts' `domain/`/`infrastructure/`/`presentation/`        |
| `infrastructure` | own `domain/`, own `application/` ports                                            | other contexts' anything; `presentation/`                          |
| `presentation`   | own `domain/`, own `application/`, other contexts' `presentation/index.ts`         | own `infrastructure/`; other contexts' `domain/`/`infrastructure/` |

Full layer rules: see DDD plan `tech-docs.md` § "Layer rules".

## XState Machine Placement

- **Pure** (no `fromPromise`/IO actors) → `domain/`
- **Orchestrating** (invokes IO actors / cross-context calls) → `application/`
- **UI shell** (no aggregate model, just view state) → `presentation/`

Full xstate placement rules: see DDD plan `tech-docs.md` § "xstate machine placement".

## Cross-Context Calls

- Only via target BC's `application/index.ts` (or `presentation/index.ts` for hooks/components).
- NEVER hold a foreign machine's actor handle.
- NEVER import another context's `domain/`, `infrastructure/`, or non-published files.

## Glossary Authoring Rule

When you add a new domain term to code OR a Gherkin feature:

1. Add a row to the right context's `specs/apps/organiclever/ddd/ubiquitous-language/<bc>.md` Terms table.
2. Set `Code identifier(s)` to the actual symbol(s) in code (backtick-comma-list).
3. Set `Used in features` to the `.feature` filename(s) under that BC's Gherkin folder.
4. If the term is also used by another context with a different meaning, add it to **both** glossaries' "Forbidden synonyms" sections cross-linking each other.
5. The glossary update lands **in the same commit** as the code/feature change.

## Pre-commit Checklist

```bash
nx run organiclever-www:test:quick
# This runs (among other things):
#   rhino-cli specs structure validate   (its bc: and ul: layers)
# It must exit zero before the commit can proceed.
```

If either reports a finding:

- **Orphan code/glossary/gherkin** — register it in `bounded-contexts.yaml` or move it under an existing context.
- **Stale code identifier** — update the glossary `Code identifier(s)` column to match the renamed symbol.
- **Term collision** — add cross-linked Forbidden synonyms to both glossaries.
- **Layer subfolder mismatch** — update the registry's `layers` array OR remove the unused subfolder.

NEVER silence a finding by lowering severity in production. Use `OSE_RHINO_DDD_SEVERITY=warn` only for local exploratory work.
