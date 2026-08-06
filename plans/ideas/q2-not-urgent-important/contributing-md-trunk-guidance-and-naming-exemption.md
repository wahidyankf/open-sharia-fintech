# CONTRIBUTING.md trunk guidance correction + naming exemption

One-line summary: fix `CONTRIBUTING.md`'s stale "work directly on `main`" instruction and unblock the
file so the correction can actually be committed.

> De-promoted 2026-07-21 from a full backlog plan (full detail preserved in git history).

## Problem / context

`CONTRIBUTING.md` line 132 still tells contributors "**Default**: Work directly on the `main` branch",
which directly contradicts every other governance surface — `AGENTS.md §Delivery Mode` makes
`worktree-to-pr` the default and direct-to-`main` an explicit per-plan selection. Worse, the
correction is unlandable today: `lint-staged` hands every staged `.md` to `rhino-cli md naming
validate`, which enforces `^[a-z0-9-]+\.md$` on the basename and rejects the uppercase
`CONTRIBUTING.md`, so any commit touching the file is blocked at pre-commit. The validator's
always-exempt set (`README.md`, `SKILL.md`, `AGENTS.md`, `CLAUDE.md`, `_index.md`) is hardcoded in
`apps/rhino-cli/src/application/docs/naming.rs`, which sits inside the rhino-cli byte-identity
boundary (zero carve-outs across all three repos). Surfaced during the
`parallel-orchestration-shared-machine-governance` Knowledge Capture phase.

## Why now

The file is effectively frozen — the naming gate blocks any edit — so the stale trunk guidance cannot
be corrected without first resolving the exemption. A new contributor reading `CONTRIBUTING.md` today
gets the opposite instruction from the rest of the repo, and every day it stays that way is another
contributor onboarded against the wrong workflow.

## Prior art / precedents

- **GitHub CONTRIBUTING.md convention** — the ecosystem-standard uppercase root file GitHub resolves by
  name, which is why renaming is out of scope and an exemption is needed instead. [GitHub docs](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors)
- **Trunk Based Development** — the workflow the stale "work directly on `main`" line contradicts and the
  correction restores. [trunkbaseddevelopment.com](https://trunkbaseddevelopment.com/)
- **File Naming convention (exempt set)** — the existing precedent for exempting conventional uppercase
  root files (`README.md`, `AGENTS.md`) that Route B extends. [file-naming](../../../repo-governance/conventions/structure/file-naming.md)
- **AGENTS.md §Delivery Mode** — the governance surface the corrected trunk guidance must agree with.
  [AGENTS.md](../../../AGENTS.md)

## Proposed direction (sketch)

- Pick one of two exemption routes: **Route A** adds `--exempt "CONTRIBUTING.md"` to the one
  `package.json` lint-staged line (cheap, single-repo, no boundary crossing; already verified to
  unblock the file), or **Route B** adds `CONTRIBUTING.md` to the hardcoded always-exempt set
  (principled — it is an ecosystem-standard root file like the others already exempt — but requires a
  coordinated 3-repo byte-identical change plus companion Gherkin).
- Correct the git-workflow section to state `worktree-to-pr` as the default, direct-to-`main` as an
  explicit selection.
- Sweep the rest of the file for other guidance that drifted while it was frozen.

## Rough scope & non-goals

In scope: the exemption route, the trunk-guidance correction, and a drift sweep of the whole file.

Out of scope (for now): renaming `CONTRIBUTING.md` to kebab-case (GitHub resolves the file by its
conventional uppercase name; renaming breaks platform integration).

## Risks & open questions

- Route A vs. Route B is the one unresolved design decision — cheap single-repo unblock vs. the more
  consistent rule that pays the byte-identity-boundary coordination cost. (open)
- If Route B is chosen, the change is bound by the rhino-cli byte-identity boundary: identical source
  in all three repos plus companion Gherkin under `specs/apps/rhino/behavior/rhino-cli/gherkin/**`.
- The exemption must not silently disable the rule for other files — a falsifiability control (a
  non-exempt `Some-Doc.md` must still fail) has to stay green.

## What success looks like + promotion signal

Success: `CONTRIBUTING.md` states `worktree-to-pr` as the default, agrees with `AGENTS.md`, and can be
committed (naming validate exits 0) while the rule still rejects other uppercase filenames. Ready to
re-promote to a `backlog/` plan once the Route A vs. Route B decision is made — the edits themselves
are mechanical.
