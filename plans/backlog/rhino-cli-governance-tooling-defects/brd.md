# Business Requirements — rhino-cli Governance Tooling Defects

## Business Goal

Make three governance tools report what they actually did, so a maintainer can trust a green run.

All three defects share one failure mode: the tool exits 0 while doing less than the caller believes.
That is worse than an outright crash, because a crash gets fixed the same afternoon and a silent
under-run gets built on for months.

## Why It Matters

**The repository's governance is enforced, not merely written.** Every convention here is backed by a
gate, and the gates are how a rule survives contact with twelve harnesses and four repositories. A
gate that passes vacuously converts a real guarantee into a decorative one, and nothing signals the
downgrade.

Concrete cost already paid during `repo-rules-sweep`:

- **WS-1** cost a wrong-cause investigation. The audit named a file and a term that were both
  correct; the actual trigger was a line wrap three lines earlier. The fix that day was to rejoin the
  span — which is a workaround, not a repair, and leaves every future author one reflow away from the
  same dead end.
- **WS-2** cost a spec. `harness-registry-driven.feature` asserted a property of two commands; when
  one was withdrawn, the surviving half looked like a safe place to repoint the claim. It was not —
  the property was never true of the replacement. The scenario had to be narrowed, so the repository
  now proves less than it did.
- **WS-3** cost a false "clean sweep". Phase 4 reported success; a hand scan of 12,666 non-markdown
  files then found two stale governance paths. Had nobody run that scan, both would have shipped.

Added later, from `repository-onboarding-readme-refresh` Phase 0:

- **WS-4** cost a misread in both directions. Baselining that plan, `gate run --surface=pre-push`
  exited 0 with `README INDEX AUDIT FAILED: 425 finding(s)` inside its own output. Trusting the exit
  code meant declaring a surface green while 425 findings scrolled past; trusting the text meant
  declaring a passing surface red. Only reading the Rust settled which the repository meant. The 425
  are a **dark-launched** kind — printed deliberately, gating deliberately not — and the wording
  defeats the point of dark-launching them, because a line that always says `FAILED` is a line
  readers stop reading.

## Business Impact

| If fixed                                                                         | If skipped                                                                                          |
| -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| A green vendor audit means the prose is clean, regardless of how it was wrapped. | Authors avoid reflowing governance prose, or hit an unexplainable audit failure and guess at it.    |
| Adding an agent-bearing harness is a `repo-config.yml` edit.                     | It is a source edit in Rust, in four repositories, gated by a parity manifest.                      |
| A rename sweep that matched nothing says so.                                     | Every future sweep needs the same manual cross-check, and the one that skips it ships broken links. |

## Affected Roles

- **Maintainers** running pre-push and CI gates — the direct consumers of every wrong verdict.
- **AI agents** executing governance plans — they act on the tool's exit code and have no way to
  detect a vacuous pass.
- **Reviewers** on any PR touching `repo-governance/` — they currently need out-of-band knowledge
  (do not wrap code spans; verify rename maps by hand) that no document states.

## Success Metrics

1. A synthetic repository whose agent tier lives outside `.claude/` validates without a source edit.
2. A rename map that matches zero targets produces a non-zero exit and a named reason.
3. A governance path referenced from a tracked non-markdown file is reported by a gate, not by a
   human running `grep` after the fact.
4. Deliberately wrapping an inline code span across a line break in a fixture changes **no** vendor
   audit finding.
5. `gate run --surface=pre-push` exits 0 and prints no `AUDIT FAILED` line — a pair that cannot both
   hold today — while all 425 informational findings remain listed.

## Non-Goals (business scope)

- Re-opening the WS-C withdrawal of the two naming validators. That decision stands; WS-2 fixes a
  survivor, it does not restore a casualty.
- Any reformatting or re-wrapping of the existing governance corpus. If the audit is fixed, the
  corpus needs no accommodation.
- Broadening `md links validate` into a general non-markdown link checker. WS-3's non-markdown reach
  is scoped to **rename propagation**, not to link health at large.

## Risks and Mitigations

| Risk                                                                                            | Mitigation                                                                                                      |
| ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| WS-1's document-level pairing changes findings on the existing corpus in ways nobody predicted. | Capture the full current finding set as a golden master **before** the fix; diff after. Any delta is reviewed.  |
| WS-3's stricter exit code breaks an existing caller that relies on a no-op run exiting 0.       | Enumerate callers first (the registry, hooks, CI matrix, and this plan's own scripts) before changing the code. |
| An `apps/rhino-cli` edit silently desynchronizes the four-repo parity manifest.                 | Regenerate and stage the manifest in the same commit as the source change; the parity gate is a phase gate.     |
| Fixing WS-2 tempts a broader registry refactor.                                                 | Scope is the agent-directory set only. Any other registry coupling found is captured, not fixed here.           |
