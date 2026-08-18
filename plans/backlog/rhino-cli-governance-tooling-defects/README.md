# 🔧 rhino-cli Governance Tooling Defects

## Context

Three defects in `apps/rhino-cli`'s governance tooling, all surfaced by executing
[`repo-rules-sweep`](../../in-progress/repo-rules-sweep/README.md) and routed here by its Phase 6
Knowledge Capture (entries 2, 3, 4, and 5 of that plan's `learnings.md`).

Each defect is a **silent** one: the tool exits 0 and reports success while doing less than the
caller believes. That shared shape is why they are one plan — the fix in every case is to make the
tool's blind spot observable, not merely to widen it.

None was fixed inline. All three touch `apps/rhino-cli`, so the
[Code-Routing Downstream Rule](../../../repo-governance/development/quality/knowledge-capture/the-code-routing-downstream-rule.md)
makes a separate plan mandatory: each carries its own TDD cycle, companion Gherkin, and a four-repo
parity-manifest obligation.

## Workstreams

| ID   | Workstream                                                  | Phases | Status    |
| ---- | ----------------------------------------------------------- | ------ | --------- |
| WS-1 | Vendor audit: pair backticks across line wraps              | 1      | Specified |
| WS-2 | `harness bindings validate`: read agent dirs from registry  | 2      | Specified |
| WS-3 | `rewrite-paths`: path-keyed matching and non-markdown reach | 3      | Specified |

### WS-1 — The vendor audit mis-pairs a wrapped inline code span

`repo-governance vendor validate` strips inline code spans **per line** (`strip_non_prose` →
`inline_code_re`). When a span straddles a line wrap, the next line's pairing starts from the span's
closing backtick and mis-pairs from there, so a later genuinely-fenced term is reported as bare
prose.

Observed during `repo-rules-sweep` Phase 3: reflowing a paragraph so that
`` `harness bindings generate` `` wrapped made the audit report `.claude/` on a line containing no
`.claude/` at all. Rejoining the span cleared it with no wording change.

The false positive is the visible half. The invisible half is worse: the same reset can **swallow** a
genuine violation by treating real prose as if it were inside a code span.

### WS-2 — `harness bindings validate` hard-codes `.claude/agents`

`repo-config.yml` carries a `harness:` registry naming every agent-bearing harness and its tier. The
`repo-rules-sweep` Phase 3 withdrawal removed `harness naming validate`, and no surviving command
derives its agent-directory set from that registry: against a synthetic repository whose source tier
lives at `.custom-src/agents`, `bindings validate` fails with
`Failed to read Claude agents directory: .../.claude/agents ... No such file or directory`.

Consequence: adding a twelfth agent-bearing harness needs a **source** edit, not a config edit —
exactly the coupling the registry exists to remove.

This is a repair, not a re-litigation of the withdrawal. The property `bindings validate` checks
(mirror drift against the `.claude/` source) is real, nothing else checks it, and the Phase 3 probe
proved it works in both directions in this repository's real layout.

### WS-3 — `rewrite-paths` matches by basename and reads only `.md`

Two blind spots in the command `repo-rules-sweep` Phase 2 built:

**Basename keying.** `rewrite_one_target` splits a link target at its last `/` and looks up only the
final segment, so the map is basename-keyed. Feeding it full-path rows matched **nothing** and
reported `0 file(s) updated`, exit 0 — indistinguishable from "nothing needed changing". A
basename-only map had to be derived by hand, after separately proving 0 conflicting targets and 0
collisions outside the swept tree; the command asks for neither proof. Directory renames are
unreachable in principle, because the changed segment is not the last one — `ose-private`'s 8
directory renames needed a hand-written path-level pass.

**Markdown-only reach.** After Phase 4 reported a clean sweep, scanning all 12,666 tracked
non-markdown files in `ose-public` found two real stale references — one in `.gitignore`, one in
`repo-config.yml`. Every gate that could have caught them (`md links validate`,
`readme-index validate`) walks markdown only, so a governance path quoted in a config comment, a
shell script, or a CI workflow sits outside every automated check the repository has.

## Scope

**Repositories**: `ose-public` and `ose-private`. Any `apps/rhino-cli` edit opens a four-repo
parity-manifest obligation — see
[the parity boundary](../../../docs/reference/related-repositories.md).

**Trees in scope**: `apps/rhino-cli/src/`, `apps/rhino-cli/tests/`, `specs/apps/rhino/`, and the
parity checksum manifest.

**Out of scope**: withdrawing or re-adding any naming rule; the `file-naming.md` rework (that is
[`file-naming-convention-rework`](../file-naming-convention-rework/README.md)); reformatting the
governance corpus to work around WS-1.

## Approach Summary

Strict TDD per workstream: a RED test reproducing the silent failure, GREEN minimal fix, REFACTOR,
companion Gherkin under `specs/apps/rhino/`, then regenerate and stage the parity manifest in the
same commit. Each workstream is independently shippable, so each is its own delivery boundary.

WS-3 adds one behaviour the other two do not: a **loud** signal when a rename map matches no target.
A tool that can silently do nothing is the root cause here, not the keying scheme alone.

## Documents

- [brd.md](./brd.md) — why this work matters and what it costs to skip.
- [prd.md](./prd.md) — user stories and Gherkin acceptance criteria.
- [tech-docs.md](./tech-docs.md) — the defect anatomy and the fix design for each workstream.
- [delivery.md](./delivery.md) — the phase-by-phase execution checklist.
