---
description: What each of the three withdrawn filename rules checked, and whether dropping the governance workflow scope prefix requirement was a deliberate decision.
when_to_use: Read this when you need the full withdrawal history behind File Naming's Withdrawn Rules summary, or when deciding whether to re-document the workflow scope-prefix requirement.
---

# File Naming — Withdrawn Rules Detail

Three filename rules once bound under [File Naming](../file-naming.md#withdrawn-rules) and no longer
do.

## The Three Rules

- **Agent role suffix** — checked an agent definition file's last basename token against a closed
  role vocabulary.
- **Governance workflow type suffix** — checked a workflow filename's last segment against a closed
  type vocabulary.
- **Governance workflow scope prefix** — required a workflow filename's _first_ segment to come from
  a closed scope vocabulary matching its parent directory
  (`<scope>(-<qualifier>)*-<type>`), formerly the deleted `workflow-naming.md`'s Scope Vocabulary
  shard; see `git show
3b5349a97:repo-governance/conventions/structure/workflow-naming/02-scope-vocabulary.md` for the
  withdrawn text.

Each checked one basename token against a closed vocabulary, so none prevented a real defect while
each forced a rename whenever a new agent, workflow type, or scope appeared. No existing filename
changed for any of the three.

## Was Dropping the Scope Prefix Deliberate?

**No.** It was a side effect of deleting `workflow-naming.md` whole rather than editing it. The
withdrawal-criterion audit in `learnings.md` weighed the type-suffix and agent role-suffix rules but
never considered the scope-prefix rule on its own merits — it was not judged and rejected, it went
unnoticed until a PR review surfaced it.

In practice, workflow files still live under a `repo-governance/workflows/<scope>/` directory whose
name is the scope, and filenames in this tree still begin with that same scope token by convention —
the observable naming pattern is unchanged. What is gone is the _written_, independently-validated
requirement: nothing today would catch a new workflow filename that omits or misspells its scope
segment. Whether to re-document and re-enforce this rule is left open, decided the next time a
workflow-naming defect surfaces or a governance review specifically revisits it — not silently
reinstated here.

## Related

- [File Naming](../file-naming.md) — the parent convention.
