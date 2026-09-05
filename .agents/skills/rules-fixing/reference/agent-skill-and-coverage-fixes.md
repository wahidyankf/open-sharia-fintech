# Agent-Skill Duplication and Coverage-Gap Fixes

## Agent-Skill Duplication Fixes

When `rules-checker` flags an agent file carrying procedural content that duplicates an
existing Skill:

1. Read the existing Skill in full — confirm it genuinely covers the duplicated content (not a
   near-miss).
2. Remove the duplicated section(s) from the agent file, replacing with a pointer sentence to the
   Skill.
3. Add the Skill's name to the agent's `skills:` frontmatter if not already present.
4. Re-run the post-fix verification (grep for the removed heading — must return nothing) and
   confirm the agent file's `## Required Reading` section still lists the Skill.

## Skills Coverage Gap Remediation

When the same procedural pattern appears duplicated **across 3 or more agents** (the validation
threshold — below 3, leave it inline; extracting a Skill for 2 agents is not worth the indirection)
and no existing Skill covers it:

1. Confirm the 3+-agent threshold via a recursive Grep across `.claude/agents/` for the pattern's
   distinctive phrasing (`.claude/agents/` is nested into role subfolders — a non-recursive
   `.claude/agents/*.md` glob only matches `README.md` and silently misses every agent).
2. Design the new Skill: `SKILL.md` plus plain-named `reference/*.md` modules as needed (a reference
   module is not a step, so it carries no `NN-` ordinal — see
   [Ordinal Filename Prefixes](../../../../repo-governance/conventions/structure/ordinal-filename-prefixes.md);
   the module README carries reading order), following the
   established shape (frontmatter `name`/`description`/`when_to_use`, Overview, reference
   pointers, Core Principles, Related Agents).
3. Rewrite each of the 3+ agent files to remove the duplicated content and point at the new Skill
   via `skills:` frontmatter and a `## Required Reading` pointer.
4. Standalone: verify rewritten agents with the configured word-budget gate. Under
   `rules-quality-gate`, do not rerun a delegated word-budget predicate; invalidate its evidence
   for rewritten files and return it as `pending`.
