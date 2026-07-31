---
title: "Plan Anti-Hallucination Convention"
description: Mandatory pre-write verification, repo-grounding, refuse-on-uncertainty, and confidence-labeling rules for plan content authored by AI agents
category: explanation
subcategory: development
tags:
  - plans
  - ai-agents
  - factual-validation
  - anti-hallucination
  - web-research
  - verification
created: 2026-05-03
---

# Plan Anti-Hallucination Convention

This convention establishes mandatory verification rituals for plan content authored, validated, fixed, or executed by AI agents. Plans are executable blueprints — a hallucinated file path, fabricated Nx target, invented package version, or made-up API signature flips immediately into broken work, wasted execution cycles, and (worst case) silent harm. The cost of one upstream verification call is far smaller than the cost of executing on fabricated content.

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: Every non-trivial factual claim in a plan carries an inline confidence label (`[Repo-grounded]`, `[Web-cited]`, `[Judgment call]`, `[Unverified]`). The author's confidence is explicit text, not implicit tone.
- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: When verification fails, the author refuses to write the claim rather than papering over uncertainty. The defect surfaces at authoring time where it is cheapest to fix.
- **[Reproducibility First](../../principles/software-engineering/reproducibility.md)**: Verification commands are repeatable. A reader audits the same claim by running the same `Glob`, `Grep`, `WebFetch`, or `web-researcher` invocation the author ran.
- **[Documentation First](../../principles/content/documentation-first.md)**: External claims cite the source inline (URL + access date + excerpt). Future readers verify the claim from the plan alone, even after the URL rots.

## Purpose

This convention exists to:

- Establish bright-line **pre-write verification rituals** for every category of factual claim that appears in plan content (file paths, Nx targets, package versions, API signatures, command syntax, KPIs).
- Make **repo-grounding** mandatory — every internal reference (file path, symbol, project, target) MUST be verified to exist in the current repo before being written.
- Make **web-researcher delegation** the default for any external claim that requires more than a single-shot fetch.
- Establish **refuse-on-uncertainty** as a positive virtue — the author who writes `[Unverified]` or refuses the claim entirely is preferred over the author who writes a plausible-sounding fabrication.
- Catalog known **hallucination anti-patterns** so plan-checker can flag them mechanically and plan-fixer can rewrite them deterministically.
- Align the four plan agents (`plan-maker`, `plan-checker`, `plan-fixer`, `plan-execution-checker`) and the two plan workflows (`plan-quality-gate`, `plan-execution`) to one verification standard.

## Scope

### What This Convention Covers

- All content authored into `plans/` by `plan-maker` (or a human invoking the planning skill).
- All validation performed by `plan-checker` and `plan-execution-checker`.
- All remediation performed by `plan-fixer`.
- Every step of the `plan-quality-gate` and `plan-execution` workflows.
- The pre-execution gate that refuses to start when claims are unverifiable.
- **Absence and completeness claims made by any validating agent** — the
  [Absence and Completeness Claims](#absence-and-completeness-claims-hard) rules bind every checker
  or fixer that reports "zero occurrences found" or "this list is complete", not only the four plan
  agents.

### What This Convention Does NOT Cover

- **General factual-validation methodology** — see [Factual Validation Convention](../../conventions/writing/factual-validation.md) for the universal `[Verified]` / `[Outdated]` / `[Unverified]` confidence system. This convention extends those labels with plan-specific repo-grounding labels and stricter delegation thresholds.
- **Web-research delegation threshold** — see [Web Research Delegation Convention](../../conventions/writing/web-research-delegation.md) for the universal 2-search / 3-fetch threshold. This convention LOWERS that threshold for plan content (any non-grep'd external claim → delegate).
- **Plan structure and content placement** — see [Plans Organization Convention](../../conventions/structure/plans.md). That convention says WHAT goes in a plan; this convention says HOW to verify what you write.
- **Manual behavioral verification** — Playwright MCP / curl runtime verification is governed by [Manual Behavioral Verification Convention](./manual-behavioral-verification.md). Anti-hallucination is authoring-and-validation; manual behavioral verification is post-execution.

## Hallucination Categories in Plan Context

Plans drift from reality in predictable ways. Each category maps to a verification ritual.

| Category              | Example                                                   | Verification Ritual                                                                                            |
| --------------------- | --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **File path**         | `apps/ose-www/src/server/trpc.ts`                         | `Glob` or `Bash test -f`; if NEW, mark `_New file_`                                                            |
| **Directory path**    | `repo-governance/conventions/writing/`                    | `Bash test -d` or `Glob` for sibling                                                                           |
| **Symbol / function** | `unstable_cache`, `getServerSession`, `RouteConfig`       | `Grep` against the codebase or cite the import path                                                            |
| **Nx target**         | `nx run ose-www:test:quick`                               | Read `apps/ose-www/project.json` or `nx show project`                                                          |
| **Package version**   | `next@16.0.0`, `tRPC v11`                                 | Grep `package.json` (or `go.mod`, `Cargo.toml`, `*.csproj`, etc.)                                              |
| **API signature**     | `unstable_cache(fn, keyParts, { revalidate })`            | `web-researcher` against authoritative docs                                                                    |
| **Command flag**      | `npx nx affected -t typecheck --parallel=cores-1`         | `<cmd> --help` or repo's documented usage in `package.json` scripts                                            |
| **Test name**         | `RateLimit_RejectsExceedingRequests`                      | If pre-existing, `Grep` test files; if NEW, mark `_New test_`                                                  |
| **Agent name**        | `swe-typescript-dev`, `web-researcher`                    | List `.claude/agents/*.md` and confirm                                                                         |
| **Skill name**        | `plan-creating-project-plans`                             | List `.claude/skills/` and confirm                                                                             |
| **External standard** | "AGENTS.md spec at agents.md", "Conventional Commits 1.0" | `web-researcher` with cited excerpt + URL + access date                                                        |
| **Behavior claim**    | "Next.js serves `app/robots.ts` over `public/robots.txt`" | `web-researcher` with cited official-doc excerpt                                                               |
| **Numeric KPI**       | "reduces review time by 35%"                              | If no measured baseline exists: FORBIDDEN as fact, allowed only as `_Judgment call:_` or qualitative reasoning |
| **Cross-link target** | `[Worktree Path Convention](./worktree-path.md)`          | `Bash test -f` on the resolved path                                                                            |

If a claim does not match any row above and is not directly observable from the plan's own narrative, it is a candidate for `[Unverified]` labeling or refusal.

## The Four Confidence Labels

Every non-trivial factual claim written into a plan carries one of four inline labels. Labels are visible in the rendered markdown, not hidden in metadata.

- **`[Repo-grounded]`** — verified against the current commit via `Glob`, `Grep`, `Bash`, or by reading the file. The label may be omitted when the claim appears within a fenced code block whose entire purpose is to quote a repo file (the fence itself is the evidence). Use the label inline whenever a repo path or symbol is named in prose.
- **`[Web-cited]`** — verified against an external source. The claim MUST include the URL and the access date inline. Multi-page research MUST go through `web-researcher` (see Delegation Threshold below).
- **`[Judgment call]`** — explicitly labeled subjective claim. No verification possible because the claim is opinion or expectation. Numeric KPIs that are gut targets (not measurements) MUST use this label.
- **`[Unverified]`** — author flagged the claim as needing verification but proceeded under time pressure. `plan-checker` flags `[Unverified]` claims as MEDIUM findings; `plan-fixer` either verifies and re-labels or escalates to manual review.

Bare unlabeled claims about file paths, versions, APIs, or behavior are treated as `[Unverified]` by default. Authors SHOULD label proactively rather than rely on the default.

## Repo-Grounding Rule (HARD)

Every internal reference in a plan MUST be verified to exist in the current commit before being written. The verification command is encoded by the claim category in the table above.

**Verification recipe** (run BEFORE writing the claim):

```bash
# File path
test -f apps/ose-www/src/server/trpc.ts && echo OK

# Directory path
test -d repo-governance/conventions/writing/ && echo OK

# Symbol exists in codebase
rg -lE "(^|[^A-Za-z0-9_])unstable_cache([^A-Za-z0-9_]|$)" apps/ libs/

# Nx target defined
jq -r '.targets | keys[]' apps/ose-www/project.json | grep -q '^test:quick$' && echo OK

# Package version present in package.json
jq -r '.dependencies.next // .devDependencies.next' package.json

# Agent/skill exists
test -f .claude/agents/swe-typescript-dev.md && echo OK
test -f .claude/skills/plan-creating-project-plans/SKILL.md && echo OK
```

If any verification fails, the author has three valid responses:

1. **Find the correct reference** (different file path, different target name) and re-verify.
2. **Mark the claim as `_New file_` / `_New target_`** if the plan creates it (and ensure the delivery checklist explicitly covers creation).
3. **Refuse the claim** — write `[Unverified]` and flag for follow-up, or omit entirely.

The forbidden response is to write the unverified claim as if it were a fact.

## Absence and Completeness Claims (HARD)

The Repo-Grounding Rule above governs **presence** claims ("this file exists"). The mirror-image
claims — **absence** ("no file does X") and **completeness** ("this doc lists every Y") — fail in a
different and more dangerous way: the verification command returns a clean-looking result while
having verified nothing at all. These rules bind every agent that asserts absence or completeness —
`plan-maker`, `plan-checker`, `plan-execution-checker`, `plan-fixer`, and any checker or fixer agent
reporting "zero occurrences found" or "the list is complete".

### A zero-result search is evidence only if the command could have produced a non-zero result

A search that fails to run reports the same thing as a search that ran and found nothing. Before a
zero result may be cited as evidence of absence, all four of the following MUST hold:

1. **The verbatim command is recorded** — in the plan, the audit report, or the delivery note. A
   zero result without its command is unfalsifiable and carries no evidentiary weight.
2. **stderr is NOT suppressed** — `2>/dev/null` on a search command converts a hard tool failure
   into an indistinguishable clean zero. Never append it to a search whose zero result will be
   cited.
3. **The exit status is inspected** — distinguish "ran, matched nothing" (grep exit 1) from "failed
   to run" (exit 2, or a tool-specific usage error).
4. **A known-positive control probe passes** — run the same command shape against a pattern that
   MUST match, in the same tree, and confirm it returns non-zero. Only then does the real query's
   zero mean absence.

**Measured example from this repository** — one query, one tree, three commands:

| Command                                         | Result   | What it actually means          |
| ----------------------------------------------- | -------- | ------------------------------- |
| `grep -r <pat> --glob '*.md' . 2>/dev/null`     | 0 hits   | Tool rejected the flag and died |
| `command grep -rn --include='*.md' <pat> .`     | 377 hits | Ran correctly                   |
| `/opt/homebrew/bin/rg -l --glob '*.md' <pat> .` | 69 files | Ran correctly (file counts)     |

The cause: in this environment `grep` resolves to **`ugrep`**, which REJECTS ripgrep's `--glob`
flag. Combined with `2>/dev/null`, a hard failure was indistinguishable from a clean sweep. Related
tool traps documented elsewhere in this repo: `grep -L` means _follow symlinks_, not
_files-without-match_, so a `grep -L` acceptance clause reads as passing unconditionally.

**Verification recipe** (run BEFORE citing any zero result):

```bash
# Prefer an absolute path to the tool whose flag syntax you are using
/opt/homebrew/bin/rg -n --glob '*.md' 'Delivery Mode' repo-governance/   # rg syntax
command grep -rn --include='*.md' 'Delivery Mode' repo-governance/       # POSIX syntax
# Never: grep -r --glob '*.md' ... 2>/dev/null

# Known-positive control probe: this MUST return non-zero before a zero result is trusted
command grep -rn --include='*.md' 'Delivery Mode' repo-governance/ | head -1

# Do not parse `ls` — its output can carry hyperlink escapes that corrupt catalogue diffs
find repo-governance -name '*.md' -print0 | xargs -0 -n1 basename | sort
```

### A completeness claim requires a diff against enumerated ground truth, not a text search

Text search finds what you thought to look for. It cannot find what a document **omits**. To assert
that a document enumerates all of something, enumerate the ground truth independently and **diff**
the two sets. Three blind-spot classes in the plan that authored this rule were found only this
way — never by searching text.

**Ground truth is frequently NOT a file on disk.** A completeness contract that assumes on-disk
artifacts reproduces the exact class of gap it means to catch. Enumerate from whatever authority
actually owns the set:

| Set being claimed complete  | Authoritative enumeration command          |
| --------------------------- | ------------------------------------------ |
| Deploy/environment branches | `git branch -r`                            |
| Agents                      | `find .claude/agents -name '*.md' -print0` |
| Nx targets on a project     | `nx show project <name> --json`            |
| Declared dependencies       | `jq` over `package.json` / `Cargo.toml`    |
| Committed files of a kind   | `git ls-files '<pattern>'`                 |

**Recipe**:

```bash
# 1. Enumerate ground truth from its owning authority
git branch -r | sed 's#^ *origin/##' | command grep -E '^(prod|stag)-' | sort > /tmp/truth.txt
# 2. Enumerate what the document claims
command grep -oE '(prod|stag)-[a-z0-9-]+' AGENTS.md | sort -u > /tmp/claimed.txt
# 3. Diff — anything in truth but not claimed is an uncovered case
comm -23 /tmp/truth.txt /tmp/claimed.txt
```

A non-empty left column is a completeness violation, regardless of how many text searches returned
"looks fine".

### A concept sweep validated by its own regex measures phrasing, never coverage

When a plan changes a **rule** (who merges, what the default is, which cap applies), the sweep that
proves the change landed everywhere is a **concept** sweep, not a string search. One regex is a
single sampling instrument with known blind spots — it is never an acceptance criterion. Inverting
one merge default in this repository took **four** corrective rounds; each round the edits were
right and the search was wrong, in a different way:

| Round | Sweep used                        | Blind spot it could not see                                                              |
| ----- | --------------------------------- | ---------------------------------------------------------------------------------------- |
| 1     | `\[HUMAN\][^.]*merge`             | Fixed term order — missed `merged by a human` and every markdown **table cell**          |
| 2     | Only the "generative source" file | The identical boilerplate lived in the convention **and** its maker/checker/fixer copies |
| 3     | `\[HUMAN\][^.]{0,40}merge`        | Assumed a bracketed tag and a plural noun — missed unbracketed singular "human merge"    |
| 4     | Any vocabulary-bound pattern      | **Paraphrases** stating the old rule in words the old rule never used                    |

Round 4 is the decisive one: two survivors read
`- [PR Merge Protocol](...) - Explicit user approval required` — containing neither "human" nor
"merge" as the actor phrase. **No regex over the old rule's vocabulary can ever match a paraphrase
of it.**

**Minimum discipline for a concept sweep** (all six; the last two are the ones that actually work):

1. Search **both term orders** — `A.*B` and `B.*A`.
2. Search each term **alone**, unbracketed and case-insensitively, accepting the noise.
3. Grep the **worked examples and code comments** specifically — a stale `PASS:` example teaches the
   wrong rule more forcefully than stale prose states it.
4. **Read the hits; never count them.** A count is not a signal here: correctly-framed opt-in
   sentences added by the fix legitimately make the count **rise**, so neither a falling nor a rising
   count proves anything.
5. **Enumerate every copy of the rule and treat them as one atomic edit** — the convention plus its
   `*-maker` / `*-checker` / `*-fixer` copies plus any skill that summarizes it. Fixing only the
   "generative source" leaves a checker that flags correct new work as defective and a fixer that
   silently rewrites it. A stale **fixer** copy is strictly worse than a stale convention copy:
   prose misleads a reader, a fixer recipe rewrites the repo unattended at HIGH confidence.
6. **Sweep by inbound link, not by phrasing** — enumerate every file that links to the changed
   document and re-read each referring sentence regardless of its wording. Link targets are stable
   where phrasing is not; this is the only instrument that finds paraphrases.

Rule 6 also covers the related **index-staleness** case: a surface inventory is naturally built from
files that _state_ a rule, while parent index READMEs, catalog tables, and "Related Documentation"
blurbs merely _summarize_ it — and go stale identically. Expand every inventory entry `X` with
"every index or README that links to and characterizes `X`", derived mechanically from inbound
links rather than from the author's recall.

**Hardest case — a competing convention**: an entire document whose _thesis_ is the old default
contributes only a couple of matching lines, so by hit-count it looks like a minor sweep target.
Most of its text never contains the swept literal at all. When a delta **inverts** an existing rule,
require an explicit inventory entry for every convention whose title or `description:` frontmatter
names that rule — those files need **reading**, not grepping.

**Acceptance-criterion rule (HARD)**: an acceptance criterion whose only evidence is the same regex
the delivery step used to make its edits is invalid. Something other than the editing instrument
MUST confirm convergence.

### Check the real invocation before calling a validator result evidence

A validator run in isolation may be missing the flags that make it meaningful. Running
`rhino-cli md mermaid validate` bare returns exit 1 on the validator's own deliberately-invalid
negative fixtures; CI invokes it with `--exclude apps/rhino-cli/tests/fixtures`. Treating the bare
run as a preexisting defect would have manufactured a three-repo parity plan for a non-problem.

Before citing any validator result — pass or fail — read how CI and the git hooks actually invoke
it. **Both failure directions are real**: a missing flag invents failures, and a no-op target
invents passes (this repo has `test:e2e` / `test:integration` targets that are `echo` stubs; read
`options.command` before citing a target as evidence).

### A capped query silently under-counts, and the undercount propagates

A measurement that feeds a plan's arithmetic MUST be taken via a query whose result is a genuine
count — `document.querySelectorAll(selector).length`, `git ls-files <pattern> | wc -l`, `jq
'length'` — never read off a list that was capped for display (`.slice(0, N)`, a paginated UI
listing, a truncated CLI output). A capped list produces a plausible number, not an obviously broken
one, so nothing downstream looks wrong; the undercount then propagates into every dependent
calculation, percentage, and rendered figure that treats it as ground truth.

More broadly, a completeness check should re-derive at least one of the plan's foundational
quantities from the actual source of truth at least once, rather than only checking that every
document agrees with every other document — universal internal agreement is exactly what a
propagated error looks like.

**Verification recipe**:

```bash
# Wrong -- reads a count off a capped/paginated list
browser_evaluate(() => document.querySelectorAll('.model-card').slice(0, 60).length)

# Right -- a genuine, uncapped count
browser_evaluate(() => document.querySelectorAll('.model-card').length)
```

## Refuse-on-Uncertainty Rule

When the author cannot verify a claim — even after running the recipe — the author MUST refuse to write the claim as a fact. Acceptable refusals (in order of preference):

1. **Skip the claim** — do not include it in the plan; the plan is shorter but accurate.
2. **Use `[Unverified]` label** — keep the claim but flag it for verification before execution.
3. **Use `[Judgment call]` label** — convert the claim from "this is true" to "this is my best guess".
4. **Use a placeholder** — write `_Unknown — verify before authoring_` and treat as a delivery item rather than a stated fact.

Forbidden: writing the claim without a label and hoping it is correct. This is the single most damaging hallucination pattern in plan content.

## Web-Research Delegation (Lower Threshold for Plans)

The universal threshold from [Web Research Delegation Convention](../../conventions/writing/web-research-delegation.md) is "2+ `WebSearch` calls OR 3+ `WebFetch` calls per claim → delegate to `web-researcher`". For plan content, the threshold is LOWER:

> **Any external claim that is not already documented in the repo (`docs/`, `repo-governance/`, `apps/*/README.md`, `package.json`, `go.mod`, `Cargo.toml`, etc.) and that requires more than a single `WebFetch` against an already-known authoritative URL MUST be delegated to `web-researcher`.**

Concretely:

| Situation                                                                              | Action                           |
| -------------------------------------------------------------------------------------- | -------------------------------- |
| Claim about a library version is already in `package.json` / lockfile                  | `Grep`, no web call needed       |
| Claim about Nx behavior already in `repo-governance/development/infra/nx-targets.md`   | `Read`, no web call needed       |
| Single `WebFetch` against a known URL (e.g., a specific Next.js docs page) confirms it | In-context `WebFetch` permitted  |
| Two or more searches/fetches needed to find the right source                           | **Delegate to `web-researcher`** |
| Open-ended "current best practice" question                                            | **Delegate to `web-researcher`** |
| Library API surface unfamiliar to the maker                                            | **Delegate to `web-researcher`** |

`plan-fixer` retains Exception 2 from the universal convention (in-context only; same-context re-validation is required for fixer atomicity). All other plan agents follow the lower threshold above.

## Anti-Pattern Catalog

Each pattern below is a known hallucination shape. `plan-checker` flags occurrences as HIGH; `plan-fixer` rewrites mechanically.

### AP-1: Citing a version without grep

> "We will use Next.js 16.0.0 with the new App Router..."

If `package.json` was not grep'd before writing, the version is hearsay. Verify or label `[Unverified]`.

### AP-2: Inventing a file path that "should exist"

> "Edit `apps/ose-www/src/lib/cache.ts`..."

Cache file may or may not exist at that path. `Glob` or `test -f` first. If NEW, write `_New file_` and add a creation step to the delivery checklist.

### AP-3: Citing an Nx target that may not exist

> "Run `nx run ose-www:integration-test`..."

Nx targets vary per project. Read `project.json` or run `nx show project ose-www` to enumerate real targets. The actual target is `test:integration`, not `integration-test`.

### AP-4: Inventing a function or method name

> "Wrap with `unstable_cacheTagged(fn, tags, options)`..."

Fabricated API. Real Next.js 16 surface is `unstable_cache(fn, keyParts, options)` plus `revalidateTag(tag)`. Check official docs (or delegate to `web-researcher`) before writing the API surface.

### AP-5: Fabricating a numeric KPI

> "This change reduces review time by 35%..."

If no baseline measurement exists, the number is fiction. Acceptable rewrites: `_Judgment call:_ we expect review time to drop`, or `Observable check: zero unsolicited PR-creation steps in audited plans after migration`.

### AP-6: Inventing a test name

> "Add test `Cache_RevalidatesOnTagInvalidation` to `cache.test.ts`..."

If the test does not exist yet, the plan must say `_New test_`. If the file does not exist yet, it must say `_New file_`. Otherwise the executor will look for a non-existent test and either fabricate it or stall.

### AP-7: Citing an agent or skill that does not exist

> "Delegate to `swe-rust-dev`..."

The agent must be present at `.claude/agents/<name>.md`. List the directory first or check the AGENTS.md catalog.

### AP-8: Citing a CLI flag without `--help`

> "Run `nx affected -t lint --parallel=cores-1`..."

The `--parallel` flag may or may not accept `cores-1` — check `nx --help` or repo docs. The actual repo standard (per AGENTS.md) is `cores-1` parallelism, but verify before quoting.

### AP-9: Citing a behavior claim without a source

> "Vercel automatically caches static assets for 31 days..."

Behavior claims need either a repo-doc reference, an inline `[Web-cited]` excerpt with URL + date, or `[Judgment call]`.

### AP-10: Cross-link to a file that does not exist

> "See the Foo Convention at relative path `./foo.md` ..." — when the cited target does not resolve on the current commit, this is AP-10.

Resolve the relative path and confirm the file exists before linking.

### AP-11: Citing a zero-result search as proof of absence

> "Grepped the whole repo — no other file references the old target name."

If the command was not recorded, stderr was suppressed, the exit status was not inspected, or no
known-positive control probe was run, the zero proves nothing. See
[Absence and Completeness Claims](#absence-and-completeness-claims-hard). A failed search and a
clean search are textually identical.

### AP-12: Asserting completeness from a text search

> "Checked — the convention lists every environment branch."

Text search cannot find omissions. A completeness claim requires enumerating ground truth from its
owning authority (which is often not a file on disk — `git branch -r`, `nx show project`, `git
ls-files`) and diffing it against what the document claims. See
[Absence and Completeness Claims](#absence-and-completeness-claims-hard).

### AP-13: A concept sweep whose acceptance criterion is its own regex

> "Swept `\[HUMAN\][^.]*merge` — every surviving hit is correct opt-in framing."

The pattern that produced the edits cannot also be the evidence they are complete; it re-confirms
the author's own assumption about what the target text looks like. See
[A concept sweep validated by its own regex](#a-concept-sweep-validated-by-its-own-regex-measures-phrasing-never-coverage).
`plan-checker` rejects any acceptance criterion of this shape.

### AP-14: Citing a validator result without checking its real invocation

> "`md mermaid validate` exits 1 — there is a preexisting defect to fix."

Read how CI and the git hooks actually invoke the validator first. A missing flag invents failures;
a no-op target invents passes.

## Specialized-Agent Delegation (Hallucination Reduction)

Domain-specialized agents hallucinate less than generic orchestration because they carry deeper context about their language, framework, and conventions. `plan-maker` SHOULD annotate each delivery checkbox with a suggested executor agent when a domain-specialized agent fits better than the default plan-execution Agent Selection rules.

**Annotation format** (added under the checkbox prose, before implementation notes):

```markdown
- [ ] Edit `apps/organiclever-be/src/Domain/User.fs`: add `email: string option` field with case-insensitive
      uniqueness constraint. Verify by running `nx run organiclever-be:test:unit` — new test
      `User_RejectsDuplicateEmailIgnoringCase` passes.
  - _Suggested executor: `swe-fsharp-dev`_
```

**When to annotate**:

- The action touches a specific language (`.ts`/`.tsx` → `swe-typescript-dev`, `.go` → `swe-golang-dev`, `.rs` → `swe-rust-dev`, `.fs`/`.fsproj` → `swe-fsharp-dev`, `.cs`/`.csproj` → `swe-csharp-dev`, etc.).
- The action touches a specific app context (`apps/ose-www/...` → `apps-ose-www-content-maker` for content edits).
- The action is a content/documentation change (`docs-maker`, `readme-maker`).
- The action is repo-governance/repo-rules (`repo-rules-maker`).
- The action is a content-platform skill domain (`apps-ayokoding-www-by-example-maker`, `apps-ayokoding-www-in-the-field-maker`).

**When to skip annotation** (default plan-execution Agent Selection suffices):

- Single-line edits to a governance doc (orchestrator can edit directly).
- Mechanical operations (`mv`, `git mv`, `npm install`).
- Shell commands without code edits.

`plan-checker` validates that any annotated executor agent name resolves to a real agent file (`.claude/agents/<name>.md`). Citing a non-existent agent is treated as AP-7 (HIGH finding).

`plan-execution` Step 2 Agent Selection respects the annotation as the highest-priority match — the suggested executor wins over the heuristic match by file extension or content keyword.

## Validation Rituals (per plan agent)

Each plan agent applies this convention at a specific point in its workflow:

- **`plan-maker`** — before writing each non-trivial claim, run the verification recipe for the claim's category. If verification fails, refuse-on-uncertainty.
- **`plan-checker`** — Step 5f scans the entire plan for unverified claims (file paths, Nx targets, package versions, API signatures, agent names, KPIs) and flags violations against the Anti-Pattern catalog.
- **`plan-fixer`** — re-verifies each finding before applying. Repo-grounding failure during re-verification means MEDIUM (manual review), not HIGH (auto-apply). Fabricated content NEVER auto-applied.
- **`plan-execution-checker`** — verifies that all delivery-checkbox claims still hold after execution: file paths exist (or were created), commands ran successfully, claimed test names appear in the test files, claimed Nx targets are present in `project.json`.

## Workflow Integration

- **`plan-quality-gate`** workflow — Step 1 (Initial Validation) explicitly invokes the hallucination scan as part of `plan-checker`'s Step 5f. The gate cannot pass while `[Unverified]` claims remain or any Anti-Pattern violation is open.
- **`plan-execution`** workflow — Step 2 (Initial Execution) per-item verification: before delegating an item, the orchestrator re-grounds its file paths and commands. Verification failure escalates rather than proceeds (refuse-on-uncertainty applied at execution time too).

## Examples

### Good — repo-grounded file path

```markdown
- [ ] Edit `apps/ose-www/src/server/trpc.ts` [Repo-grounded] — wrap public router with
      `unstable_cache(fn, keyParts, { revalidate: 300 })` per Next.js 16 docs (verified
      2026-05-03 at https://nextjs.org/docs/app/api-reference/functions/unstable_cache,
      excerpt: "unstable_cache allows caching results of expensive operations") [Web-cited].
      Verify by running `npx nx run ose-www:test:quick` — all tests pass.
```

### Bad — invented file path + fabricated API

```markdown
- [ ] Edit `apps/ose-www/src/lib/cache-config.ts` to enable Next.js automatic edge caching
      with `enableEdgeCache(true)`. Performance improves by 40%.
```

Problems: file path was not verified (probably does not exist); `enableEdgeCache` is fabricated API; 40% is a fabricated KPI. Three Anti-Pattern violations (AP-2, AP-4, AP-5).

### Good — refuse-on-uncertainty

```markdown
- [ ] Add Sharia-compliant interest-free billing model to `apps/organiclever-www/src/components/Pricing.tsx`.
      _Unknown — verify Vercel + Stripe Sharia-compliance posture before authoring_ — see follow-up
      research item under Open Questions.
```

The author refused to write a fabricated billing flow. A follow-up research item appears under the plan's Open Questions section. Better than fabricating.

## Validation

To validate a plan complies with this convention:

1. **Confidence labels present**: every non-trivial factual claim has `[Repo-grounded]` / `[Web-cited]` / `[Judgment call]` / `[Unverified]` or is contained in a quoted code-fence whose source is unambiguous.
2. **No Anti-Pattern hits**: `plan-checker` Step 5f scan reports zero AP-1 through AP-14 violations.
3. **Repo-grounding verifiable**: every internal reference (file path, Nx target, agent, skill) resolves on the current commit.
4. **External citations complete**: every `[Web-cited]` claim includes URL + access date + excerpt inline.
5. **No bare KPIs**: every numeric percentage / duration / count is either an observable check, a citation, or `[Judgment call]` — never an unlabeled fact.

`plan-checker` enforces all five at validation time.

## Tools and Automation

- **`web-researcher`** — default research primitive for external claims.
- **`plan-checker`** — Step 5f hallucination scan against this convention.
- **`plan-fixer`** — re-verification before applying replacement content.
- **`plan-execution-checker`** — post-execution claim verification.
- **`plan-quality-gate`** — workflow gate that cannot pass until zero anti-pattern violations remain.
- **`plan-execution`** — workflow Step 2 per-item verification before delegation.

## References

**Related Conventions:**

- [Plans Organization Convention](../../conventions/structure/plans.md) — what goes in a plan; this convention says how to verify what you write.
- [Factual Validation Convention](../../conventions/writing/factual-validation.md) — universal `[Verified]` / `[Outdated]` / `[Unverified]` system this convention extends.
- [Web Research Delegation Convention](../../conventions/writing/web-research-delegation.md) — universal delegation threshold this convention lowers for plan content.
- [Manual Behavioral Verification Convention](./manual-behavioral-verification.md) — runtime verification (Playwright MCP / curl); complementary to anti-hallucination at authoring time.
- [Worktree Path Convention](../../conventions/structure/worktree-path.md) — worktree routing referenced by the Worktree Specification rule in plans.

**Agents:**

- [`plan-maker`](../../../.claude/agents/plan-maker.md), [`plan-checker`](../../../.claude/agents/plan-checker.md), [`plan-fixer`](../../../.claude/agents/plan-fixer.md), [`plan-execution-checker`](../../../.claude/agents/plan-execution-checker.md) — the four agents this convention governs.
- [`web-researcher`](../../../.claude/agents/web-researcher.md) — research primitive.

**Workflows:**

- [Plan Quality Gate](../../workflows/plan/plan-quality-gate.md)
- [Plan Execution](../../workflows/plan/plan-execution.md)

**Agent skills:**

- [`plan-creating-project-plans`](../../../.claude/skills/plan-creating-project-plans/SKILL.md) — authoring guide that consumes this convention.
- [`docs-validating-factual-accuracy`](../../../.claude/skills/docs-validating-factual-accuracy/SKILL.md) — universal factual-validation methodology.

**Repository Architecture:**

- [Repository Governance Architecture](../../repository-governance-architecture.md) — six-layer hierarchy. This convention is Layer 3 (Development), governing Layer 4 agents and Layer 5 workflows that consume Layer 2 conventions (factual-validation, web-research-delegation).

## Conventions Implemented/Respected

- **[File Naming Convention](../../conventions/structure/file-naming.md)**: kebab-case `.md` filename.
- **[Linking Convention](../../conventions/formatting/linking.md)**: GitHub-compatible markdown with `.md` extensions.
- **[Content Quality Principles](../../conventions/writing/quality.md)**: active voice, single H1, proper heading hierarchy.
- **[Factual Validation Convention](../../conventions/writing/factual-validation.md)**: extends the universal confidence-label system (`[Verified]`/`[Outdated]`/`[Unverified]`) with plan-specific repo-grounding labels (`[Repo-grounded]`, `[Web-cited]`, `[Judgment call]`, `[Unverified]`).
- **[Web Research Delegation Convention](../../conventions/writing/web-research-delegation.md)**: lowers the universal delegation threshold — for plan content, any external claim not grepable from the repo requires `web-researcher` delegation.
