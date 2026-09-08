<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: lms-init

## Learning: the mermaid gate threshold is looser than the binding label rule

- **Context**: authoring `tech-docs.md`. `rhino-cli md mermaid validate` reported
  `label_too_long` at 30 characters, so the diagrams were rewritten to sit at or just under 30.
  The gate then passed, but the rendered diagram visibly clipped every label past roughly 27
  characters.
- **Observation**: the binding rule is
  [Rule 3](../../../repo-governance/conventions/formatting/diagrams/common-syntax-errors-label-constraints-rule-3-line-length.md)
  — **20** characters per `<br/>` segment. The gate's default `--max-label-len` is **30**, which
  that document describes as "Mermaid's `wrappingWidth` baseline" and explicitly pairs with the
  advice to "use `--max-label-len 20` for stricter validation". So a green default-threshold run
  proves the diagram is under the backstop, not under the rule. The repository already documents
  this in three places, including a dedicated
  [render-fidelity caveat](../../../repo-governance/conventions/formatting/diagrams/mermaid-render-fidelity-caveat.md)
  stating that a green validate is "necessary, not sufficient".
- **Why it might generalize**: an author who meets the number the gate prints, rather than the
  number the convention states, ships a clipped diagram with a green gate. The failure mode is
  silent and only visible in rendered output. Candidate durable fixes to weigh at triage: lower the
  flowchart default to 20; or emit the Rule-3 number in the violation message so the printed
  threshold and the binding rule agree; or note in the flowchart width-constraints document that
  authors should run the strict flag before committing. The existing
  `plans/ideas/q2-not-urgent-important/mermaid-state-label-render-clipping-warn.md` two-pager
  covers the neighbouring `stateDiagram` case and may be the right place to fold this in rather
  than opening a new brief — check it first, and note that its own analysis warns any such rule
  must WARN rather than FAIL given the corpus size.

## Learning: absolute worktree paths in a delivery document are a leak, not a convenience

- **Date**: 2026-09-08
- **Context**: the plan-authoring PR's required `pr-leak-review` flagged four occurrences of a
  resolved home-directory path inside `delivery.md` — the cross-repository `diff` commands and the
  private-worktree provisioning step. They had been written as fully-resolved absolute paths so the
  commands would be copyable verbatim.
- **What happened**: the paths violate
  [what-counts-as-machine-specific-information.md](../../../repo-governance/development/quality/no-machine-specific-commits/what-counts-as-machine-specific-information.md)
  §Formal Plan Delivery Documents, which names `plans/**/delivery.md` explicitly and requires a
  worktree be identified only by its repository-relative route. The same section states that the
  required PR leak review inspects the changed delivery document for exactly this. The fix resolves
  the private worktree once, at the step that provisions it, into a `PRIVATE_WT` shell variable
  derived from `git worktree list --porcelain`, and expresses every later cross-repository command
  relative to the public worktree root.
- **Why it might generalize**: "make the command copyable verbatim" is a real authoring pressure in
  execution-grade plans, and it pulls directly against the portability rule. Nothing catches it at
  authoring time — the violation surfaces only at the leak review, after the PR is open and its CI
  has already run. Candidate durable fixes to weigh at triage: have `plan-checker` reject a
  home-directory or resolved host path anywhere in a delivery document, not only in the worktree
  identity section it already checks; or state the portable two-repository idiom (resolve once into
  a variable at the provisioning step) directly in the plans convention so authors reach for it
  before inventing an absolute path.

## Learning: implementation notes are part of the delivery document the leak review inspects

- **Date**: 2026-09-08
- **Context**: minutes after fixing four machine-specific absolute paths in `delivery.md`, the very
  first Atomic Sync Ritual note written back into that same file recorded the literal output of
  `rtk pwd` — reintroducing the exact path class that had just been rejected.
- **What happened**: caught on re-read before commit and rewritten to state only that the path ends
  in `worktrees/lms-init`. The pull is structural, not careless: the ritual asks for notes that are
  repo-grounded and quote what was actually run, and the most direct way to evidence "I confirmed
  the location" is to paste the resolved path. But the portability rule in
  [what-counts-as-machine-specific-information.md](../../../repo-governance/development/quality/no-machine-specific-commits/what-counts-as-machine-specific-information.md)
  §Formal Plan Delivery Documents scopes to the whole committed document, notes included — and the
  leak review inspects the complete changed file, not only the prose an author considers "content".
- **Why it might generalize**: the two obligations pull in opposite directions at exactly the
  moment an executor is moving fastest, and the evidence for a location check is precisely the
  thing that must not be committed. The safe form is to record the _property_ that was verified
  ("the path ends in `worktrees/lms-init`"), not the value that satisfied it. Candidate durable
  fixes to weigh at triage: state this explicitly in the Atomic Sync Ritual's notes guidance, so
  the rule is visible where notes are written rather than only where worktree identity is declared;
  and extend whatever check enforces the portability rule to cover HTML-comment note blocks, since
  an author who has just read the rule can still violate it one edit later.

## Learning: the parity-sibling repositories have drifted apart on their pinned npm version

- **Date**: 2026-09-08
- **Context**: Phase 0's `rtk npm run doctor -- --fix` exits 0 in both worktrees, but `ose-public`
  reports 15/16 tools OK with one warning — npm v11.16.0 installed against a required 11.11.0 —
  while `ose-private` reports 16/16 with no warning on the very same host and the same installed
  npm.
- **What happened**: the requirement, not the installation, is what differs. `ose-public`'s
  `package.json` pins `volta.npm` to `11.11.0`; `ose-private` pins `11.16.0`. One host, one npm,
  two verdicts. Left unbumped: this plan is authorized to initialize an LMS backend, and changing a
  pinned toolchain version is a governance change with workspace-wide CI blast radius and its own
  propagation obligation.
- **Why it might generalize**: the two repositories are documented parity siblings, but the parity
  that is actually _enforced_ is narrow — `apps/rhino-cli` byte-identity via
  `parity-manifest.sha256`. Nothing checks that their toolchain pins agree, so this divergence can
  persist indefinitely while every gate stays green, and the only symptom is a warning line one
  repository prints and the other does not. Candidate durable fixes to weigh at triage: extend the
  nightly parity audit to compare `volta` pins across the sibling pair; or state explicitly in the
  related-repositories reference which surfaces are parity-bound and which are deliberately
  independent, so a divergence like this is legible as intentional or accidental rather than
  ambiguous.

## Learning: a controlled vocabulary nobody validates fails open, not closed

- **Context**: DU2 rules-propagation Step 7. The plan expected the `lang:`/`platform:` tag
  vocabulary to be "enforced by `repo-config validate` plus the tag convention". Checking that
  claim disproved it: `repo-config validate` reads `repo-config.yml`, which has no tag schema and
  no `tags` key; no `gates:` entry reads `project.json` tags; `nx.json` declares no tag
  constraints and there is no ESLint config, so `@nx/enforce-module-boundaries` is not configured
  to constrain values either; and no F# validator reads project tags.
- **Observation**: the vocabulary table is enforced by human review and nothing else, and the one
  machine consequence of an undeclared value is silent in the dangerous direction. The `detect`
  job's per-tag `case` has an arm per admitted value; an unrecognized `lang:` value matches no arm,
  so the project gets **no** language quality-gate job. The PR then goes green having run nothing
  for that project. A typo in a tag reads as "this language is not affected" rather than as an
  error.
- **Corroborating evidence that this is already live, not hypothetical**: the table admits `rust`
  and `dotnet`, which no `project.json` uses, and omits `fsharp` and `giraffe`, which 6 and 2
  projects respectively do use. The drift survived because nothing measures it.
- **Why it might generalize**: the pattern is "documented controlled vocabulary + consumer that
  silently ignores unknown values". Any such pair fails open. Candidate durable fixes to weigh at
  triage: a `governance-tag-vocabulary` gate reading every `project.json` `tags` array against the
  four-dimension table; and separately, a `*)` default arm in the `detect` case that emits
  `::error::` for an unrecognized `lang:` value, so an unknown tag fails loudly at the point it
  would otherwise be dropped. Reconcile the four stale table entries first, or the gate lands red
  across 23 existing projects.

## Learning: an Nx-cached target is not evidence that a gate ran

- **Context**: DU2-089. The plan's acceptance was "run `nx run rhino-cli:test:quick`; exit 0",
  intended to prove the word-budget gate measured a newly written `.claude/` file.
- **Observation**: the first run exited 0 while reporting "Nx read the output from the cache
  instead of running the command for 1 out of 1 tasks". The target's declared inputs did not
  include the file just written, so a green exit code proved only that a previous run had been
  green. Re-running with `--skipNxCache` produced a real run, also 0.
- **Why it might generalize**: any acceptance phrased as "run `<nx target>`; it exits 0" is
  satisfiable by a cache hit whose inputs exclude the change under test. This is the same shape as
  Trustworthy Measurement Rule 7 — a green signal that does not prove the thing you wanted proven.
  Candidate durable fixes to weigh at triage: state in the measurement rules that an Nx-cached
  result is not evidence for a file the target's inputs do not declare, and that a verification run
  must either disable the cache or assert the absence of a cache-hit line; or fix the affected
  targets' `inputs` so the relevant files are declared.
