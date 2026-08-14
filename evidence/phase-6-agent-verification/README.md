# Phase 6 Behavioural Verification

Five migrated `.claude/agents/` (grouped into role subfolders in this Phase) invoked live, each
with a question answerable only by applying a rule that lives in a Skill reference module or a
governance doc — not in the agent's own trimmed ≤500-word charter. Confirms the migration didn't
lose behaviour when content moved out of the charter file.

| Agent                        | Group      | Rule under test                                                                                       | Rule's actual home                                                                                       | Result    |
| ---------------------------- | ---------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | --------- |
| `specs-maker`                | `specs/`   | Lib spec targets get no five-folder C4 tree (app-only concept)                                        | `repo-governance/conventions/structure/specs-directory-structure/04-*.md` (skill reference)              | Confirmed |
| `social-linkedin-post-maker` | `general/` | 3,000-char body limit measured from `OPEN SHARIA ENTERPRISE` line down, exact `awk`+`python3` command | `.claude/skills/social-linkedin-posting/reference/01-hard-constraints-and-measurement.md`                | Confirmed |
| `web-researcher`             | `web/`     | Four confidence tags + source-prioritization tiers                                                    | `.claude/skills/docs-validating-factual-accuracy/SKILL.md` (dedup target, not web-researcher's own file) | Confirmed |
| `repo-rules-fixer`           | `repo/`    | `sed -i` exits 0 on no-match; every fix must be grep-verified                                         | `.claude/skills/repo-rules-fixing/reference/01-verification-and-edit-discipline.md`                      | Confirmed |
| `repo-setup-manager`         | `repo/`    | Vercel MCP Probe full procedure, outcome table, degraded mode                                         | `repo-governance/development/infra/vercel-mcp.md` (dedup target, removed from agent charter)             | Confirmed |

Each agent cited the correct source document/skill by name and path without being told where to
look — proving the reference stayed wired after the Phase-6 charter trim and subfolder move.
Full per-agent transcripts follow.

## specs-maker

**Probe**: asked to scaffold `specs/libs/demo-verification-probe/` with `surface-profile: cli-only` —
a deliberately mismatched combination (surface-profile is an apps-only concept; the target is a
lib path) to test the agent correctly reads the convention rather than pattern-matching the words
in the prompt.

**Response**: correctly declined to apply the app-only `cli-only` five-folder tree to a lib
target, cited
`repo-governance/conventions/structure/specs-directory-structure/04-gherkin-feature-file-placement-and-lib-spec-structure.md`
"Lib Spec Structure" section verbatim, and produced the correct simpler `README.md` +
`gherkin/<package>/` lib tree instead. No files created (probe respected the dry-run instruction).

## social-linkedin-post-maker

**Probe**: asked for the exact character-limit rule, anchor line, and measurement command.

**Response**: reproduced the `awk '/^OPEN SHARIA ENTERPRISE/{p=1} p' <file> | python3 -c
'import sys;print(len(sys.stdin.read()))'` command verbatim, the ~2,900-char safety margin, and
correctly distinguished this rule (agent's own Hard Constraints) from the separately-cited
`docs-applying-content-quality` skill (general prose quality only). This exact command exists
only in `.claude/skills/social-linkedin-posting/reference/01-hard-constraints-and-measurement.md`
— not in the trimmed charter body.

## web-researcher

**Probe**: live research question (latest Node.js LTS) requiring the agent to tag its finding
with the project's confidence classification system.

**Response**: tagged `[Verified]`, cited two independent Tier-1/Tier-4 sources per the
source-prioritization system, and explicitly named
`.claude/skills/docs-validating-factual-accuracy/SKILL.md` as the source of both the four-tag
system and the tier definitions — confirming the dedup-against-existing-skill pattern still
resolves correctly after web-researcher's own copy of this content was removed.

## repo-rules-fixer

**Probe**: asked why a `sed -i` exit code alone isn't proof a fix applied.

**Response**: explained `sed -i` exits 0 even on a no-op match, gave the mandatory
`grep -q "new-pattern" file.md || echo "WARNING..."` verification pattern, and cited "Post-Fix
Verification (Mandatory)" — quoting the "caused garbled headings in previous iterations"
rationale that lives in
`.claude/skills/repo-rules-fixing/reference/01-verification-and-edit-discipline.md` (a condensed
one-line version also survives in the charter's Core Principles, as designed).

## repo-setup-manager

**Probe**: asked for Phase 0 Step 5 ("Vercel MCP Probe") and where the full procedure lives.

**Response**: gave the correct conditional-skip summary (only runs when the plan touches a
Vercel-deployed surface, detected mechanically via `vercel.json`/deploy-branch presence) and
pointed at `repo-governance/development/infra/vercel-mcp.md#degraded-mode` — the exact dedup
target this agent's charter was trimmed against in this Phase, confirming the pointer survived
the move into the `repo/` subfolder.
