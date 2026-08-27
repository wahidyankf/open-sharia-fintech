# Worktree Specification (Mandatory — Applies to ALL Plans)

Provision the worktree **before** defining the plan and author every plan document inside it — the worktree precedes the plan, never follows it. Every plan MUST then declare that worktree path before the delivery checklist begins. This is enforced by `plan-checker` (HIGH finding when missing) and the [plan-execution workflow Step 0 hard gate](../../../../repo-governance/workflows/plan/plan-execution.md) — execution refuses to start if the section is absent. When the section is present, the executor enters the declared worktree by default: it auto-provisions from the latest `origin/main` when missing, syncs with `origin/main` before implementing, and — per the [Worktree Cap HARD RULE](../../../../repo-governance/conventions/structure/plans/worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule) — is capped at **one worktree per repository per plan**, reused across every delivery unit landed there. Cleanup is immediate, not deferred: the worktree is removed the moment this plan is done using that repo, not batched with unrelated later steps.

**Where to declare**:

- **Multi-file plans**: top-level `## Worktree` section in `delivery.md`, placed before any phase heading.
- **Single-file plans**: top-level `## Worktree` section in `README.md`, placed before `## Delivery Checklist`.

**Path format**: `worktrees/<plan-identifier>/` where `<plan-identifier>` matches the plan-folder identifier (strip the `YYYY-MM-DD__` date prefix). Examples:

- Folder `2026-05-15__auth-rewrite/` → worktree path `worktrees/auth-rewrite/`
- Folder `2026-03-01__add-user-search/` → worktree path `worktrees/add-user-search/`

**Required template** (insert verbatim, replacing `<plan-identifier>`):

````markdown
## Worktree

Worktree path: `worktrees/<plan-identifier>/`

Provisioned before this plan was written (run from repo root):

```bash
claude --worktree <plan-identifier>
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest `origin/main` when missing, syncs with `origin/main` before implementing, and — capped at one per repository per plan and reused across every delivery unit landed there — is removed immediately once the plan is done using this repo, not deferred to archival.

### Provisioned Worktree Identity

- Exact path: `/absolute/repo/worktrees/<plan-identifier>`
- Initial branch: `<plan-identifier>-base`
- Created by: `<executor identity or session>`
- Created at: `<ISO-8601 UTC timestamp>`

### Delivery Branch Inventory

| Branch                   | Mode          | Lifecycle state | Proof                                            |
| ------------------------ | ------------- | --------------- | ------------------------------------------------ |
| `<plan-identifier>-base` | `provisioned` | `active`        | `git worktree add` at `<ISO-8601 UTC timestamp>` |

Append every plan-created delivery branch before use. A `*-to-pr` entry records its merged PR and
40-character reviewed-head SHA; direct push records its verified `origin/main` commit. Before
removal, classify every entry as delivered, unused, or retained/escalated; active or unrecorded
branches block cleanup.

For a declared multi-repository parity objective, add `### Cross-Repository Parity Identity` with
the objective slug, one common worktree basename, and a per-repository corresponding short-lived
branch mapping. Use the same basename and branch name across applicable repositories; use `not
applicable` only when a repository's mode has no such identity. See
[Cross-Repository Parity Identity](../../../../repo-governance/development/workflow/cross-repository-parity-identity.md).

See [Worktree Path Convention](../../../../repo-governance/conventions/structure/worktree-path.md) and [Plans Organization Convention §Worktree Specification](../../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).
````

**This applies to ALL plans regardless of size** — pure-docs, single-file, and trivial plans included. No exceptions.
