# Learnings: ayokoding-learning-path-01-url-restructure

Transient running log. The executor appends one entry per generalizable learning **as it surfaces**,
sanitized before it is written. Phase 7 (Knowledge Capture) triages every entry to a durable home or
discards it with a reason; nothing is left in a non-terminal state at archival.

**Before writing any entry**, apply the two safety gates:

- **Secret / sensitivity gate** — replace any secret, credential, token, or private hostname with a
  `<placeholder>` token; discard the entry outright if it cannot be sanitized.
- **Repo-relevance gate** — infra-private content (Terraform, k3s, Proxmox, real hostnames or
  inventories) stays in `ose-infra` only and is never cross-routed into this repo.

**Code-routing rule** — a learning whose home is `apps/`, `libs/`, or tests is **ALWAYS** filed as a
separate `plans/backlog/<slug>/` plan and **NEVER** landed inline in this plan's commits or PR. The
only carve-out is a blocker genuinely required to finish this plan's own scope (Root Cause
Orientation).

Entry shape:

```markdown
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized)
- **Why it might generalize**: the litmus reasoning
- **Routing**: _(filled at Phase 7 — durable home, backlog plan slug, or discard reason)_
```

## Entries

## Learning: `ls` is shell-aliased to `eza` — `ls … | xargs` corrupts output

- **Context**: Phase 0, freezing the 37 re-home slugs via
  `ls -d …/*/ | xargs -n1 basename > evidence/phase-0-rehome-slugs.txt`.
- **Observation**: `ls` resolves to `eza --icons --hyperlink` in this environment. Piping its
  hyperlinked (OSC-8-escaped) output through `xargs` collapsed 37 directory names into 2 garbled
  lines with embedded escape codes. Invoking `/bin/ls` explicitly produced the correct 37 lines.
- **Why it might generalize**: distinct from the plan's already-documented `find`/RTK hazard — this is
  an `ls`-alias hazard. Any later step (or any plan) that pipes `ls` into `xargs`/`while read`/`wc`
  must use `/bin/ls` (or `command ls`). Phases 1–3 of this plan use `ls`-based enumeration.
- **Routing**: _(Phase 7 — candidate durable home: an env/tooling hazards note alongside the RTK
  `find` hazard, since both are "a bare builtin is silently transformed before your command sees it".)_

## Learning: tech-docs ground-truth counts drift; re-measure at Phase 0, don't trust the authored table

- **Context**: Phase 0 baseline inventory vs. tech-docs' "Ground-truth inventory" table.
- **Observation**: `fundamentally-strong` measured 562 `.md` on disk (git-tracked) vs. 563 stated in
  tech-docs — a stale authored count, confirmed via `git ls-files` + `git log --diff-filter=DR` (no
  deletions), i.e. authoring-time miscount, not a session regression. Reconciled in tech-docs (table +
  tree) and the delivery baseline string this session.
- **Why it might generalize**: any plan that hard-codes a repo-measured count in its docs should have
  a Phase-0 step that re-measures and reconciles before a later phase asserts on it — the count the
  author wrote can be stale by the time the plan runs.
- **Routing**: _(Phase 7 — likely discard-as-plan-specific, or fold into the anti-hallucination
  "repo-ground every count" guidance.)_

If execution completes and nothing generalizable surfaced, replace the entries above with the explicit
escape: `No generalizable learnings — <one-line reason>`. This file is never left silently empty.
