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

_None yet — execution has not started._

If execution completes and nothing generalizable surfaced, replace the line above with the explicit
escape: `No generalizable learnings — <one-line reason>`. This file is never left silently empty.
