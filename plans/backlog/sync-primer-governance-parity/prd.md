# Product Requirements: Sync `ose-primer` Governance Parity

## Product Overview

Bring `ose-primer`'s `apps/rhino-cli` boundary and governance-Markdown surface to parity with the
already-shipped `optimize-governance-md` state in `ose-public`/`ose-private`: byte-identical
rhino-cli source, a 500-word ceiling on governance Markdown (400 warn / 500 fail, zero exemptions),
mandatory `README.md` reachability for every covered directory, and `when_to_use` +
`description`-complete frontmatter — enforced by two armed gates
(`governance-word-budget`, `governance-readme-completeness`) plus the `md-frontmatter` gate's
FAIL-severity `description` check.

## Personas

Solo-maintainer repo; personas are hats worn and agents consuming the surface, per `brd.md`
§Affected Roles:

- **Maintainer-as-implementer** — executes this plan's delivery checklist.
- **Maintainer-as-downstream-adopter** — clones `ose-primer` to bootstrap a new product later and
  inherits whatever governance shape is live.
- **Governance-consuming agent** (`plan-maker`, `plan-checker`, `repo-rules-checker`, any agent
  reading `repo-governance/**` or `.claude/**`) — the direct consumer of the reachability and
  retrieval guarantees this plan installs.

## User Stories

**US-1**: As a governance-consuming agent operating in `ose-primer`, I want every
`repo-governance/**/*.md` and `.claude/**/*.md` file to carry a machine-checkable `when_to_use`
trigger, so that I can decide whether to open a file without reading its full body first.

**US-2**: As a maintainer running `rhino-cli gate run --surface=pre-push` in `ose-primer`, I want
the same `governance-word-budget` and `governance-readme-completeness` gates that already run in
`ose-public`/`ose-private`, so that oversized or unreachable governance content cannot land in any
of the three sibling repos.

**US-3**: As a maintainer diffing `apps/rhino-cli/src` across the three sibling repos, I want
`ose-primer`'s boundary to be byte-identical to `ose-public`'s, so that the
[rhino-cli byte-identity guarantee](../../../docs/reference/sdlc-gate-standard.md#rhino-cli-byte-identity-boundary)
holds across all three repos, not just two.

**US-4**: As a downstream adopter cloning `ose-primer` to bootstrap a new product, I want the
governance tree I inherit to already be split and indexed, so that I do not start from the same
over-grown state `optimize-governance-md` fixed in `ose-public`.

## Acceptance Criteria (Gherkin)

### FR-1 — rhino-cli boundary byte-identity sync

**Scenario: The rhino-cli boundary is byte-identical to `ose-public` after sync**

```gherkin
Scenario: The rhino-cli boundary is byte-identical to ose-public after sync
  Given the ose-primer worktree has received the byte-for-byte copy of ose-public's apps/rhino-cli
    src, tests, Cargo.toml, Cargo.lock, project.json, LICENSE, and Gherkin behavior tree
  When I run "diff -rq" across each of the seven boundary paths between the ose-public checkout and
    the ose-primer worktree
  Then every diff reports no differences
  And "rhino-cli parity manifest validate" exits 0 in the ose-primer worktree
```

**Scenario: The new governance commands exist in `ose-primer` after sync**

```gherkin
Scenario: The new governance commands exist in ose-primer after sync
  Given the rhino-cli boundary sync from FR-1 has completed
  When I run "rhino-cli governance word-budget validate --help" and
    "rhino-cli governance readme-index validate --help" in the ose-primer worktree
  Then both commands are recognized and print usage text
  And the pre-sync command names "harness instruction-size validate" and "md readme-index validate"
    (the un-renamed form) no longer resolve, except where md-readme-index's underlying binary is
    reused unrenamed pending FR-2's repo-config.yml rename
```

### FR-2 — Dark-launch gate registration and the `md-frontmatter` mitigation

**Scenario: The two new gates are registered but not yet enforced**

```gherkin
Scenario: The two new gates are registered but not yet enforced
  Given ose-primer's repo-config.yml has been updated per FR-2's registration step
  When I run "rhino-cli gate run --surface=pre-push" against ose-primer's real, not-yet-split
    repo-governance/ tree
  Then the exit code is 0
  And "governance-word-budget" and "governance-readme-completeness" are absent from the executed
    gate list (dark-launched, no pre-push/ci surface registered yet)
```

**Scenario: `md-frontmatter`'s `ci` surface is dropped before the FAIL-severity source lands**

```gherkin
Scenario: md-frontmatter's ci surface is dropped before the FAIL-severity source lands
  Given ose-primer's repo-config.yml already registers "ci: { scope: all-file-type }" for
    md-frontmatter, and the copied frontmatter.rs hardcodes FAIL severity for governance docs with
    no config toggle
  When Phase 1's repo-config.yml edit drops the "ci" surface from the md-frontmatter entry, keeping
    only "pre-commit"
  Then a full-tree "rhino-cli md frontmatter validate" run against the not-yet-split
    repo-governance/ tree is not part of any armed pre-push or ci surface
  And CI on Phase 1's own PR does not fail on pre-existing missing-description/missing-when_to_use
    debt that Phases 2-3 have not yet cleared
```

### FR-3 — `repo-governance/` and root instruction files reach word-budget compliance

**Scenario: A split file's index parent and children are all within budget**

```gherkin
Scenario: A split file's index parent and children are all within budget
  Given a repo-governance/**/*.md file exceeded 500 words before this plan
  When the file is split into an index parent plus a sibling directory of capped children per the
    progressive-disclosure pattern
  Then "rhino-cli governance word-budget validate repo-governance/" run directly (unarmed) reports 0
    failures for that file's parent and every child
  And every inbound link to the original file's path still resolves, because the parent keeps the
    original filename
```

**Scenario: Every split child is reachable from its parent's `README.md`**

```gherkin
Scenario: Every split child is reachable from its parent's README.md
  Given a directory under repo-governance/ contains one or more newly split child files
  When I run "rhino-cli governance readme-index validate repo-governance/" directly (unarmed
    invocation, matching FR-2's dark-launch state)
  Then the report contains 0 "orphan", "missing", or "unannotated" findings for that directory
  And each annotated entry's one-line summary is derived from the target file's own frontmatter
    description
```

**Scenario: `AGENTS.md` and `CLAUDE.md` are rewritten as directive indexes within budget**

```gherkin
Scenario: AGENTS.md and CLAUDE.md are rewritten as directive indexes within budget
  Given ose-primer's AGENTS.md (3,109 words) and CLAUDE.md (756 words) both exceed 500 words
  When both files are rewritten as directive indexes per FR-3's split, preserving ose-primer's own
    repo-specific directives rather than copying ose-public's post-split content verbatim
  Then "wc -w AGENTS.md" and "wc -w CLAUDE.md" each report 500 or fewer words
  And the resolved tree ("wc -w CLAUDE.md" plus every "@"-imported file's word count) is 1,500 words
    or fewer
```

### FR-4 — `.claude/agents/`, `.claude/skills/`, and generated mirrors reach parity

**Scenario: An oversized agent body is migrated to a skill reference module**

```gherkin
Scenario: An oversized agent body is migrated to a skill reference module
  Given a .claude/agents/*.md file exceeds 500 words
  When its non-charter content is migrated to .claude/skills/<name>/reference/*.md, leaving a
    charter of 500 words or fewer that unconditionally instructs reading every reference module
    before acting
  Then "rhino-cli governance word-budget validate .claude/" reports 0 failures for that agent file
  And invoking the migrated agent on a real task demonstrates it reads its reference modules and
    applies a rule that lives only in one of them
```

**Scenario: Generated mirrors regenerate within budget after source is split**

```gherkin
Scenario: Generated mirrors regenerate within budget after source is split
  Given every .claude/agents/*.md and .claude/skills/*/SKILL.md file is within the 500-word ceiling
  When I run "npm run generate:bindings" in the ose-primer worktree
  Then every regenerated file under .cursor/, .opencode/agents/, and .amazonq/ is within the same
    500-word ceiling
  And "npm run validate:sync" exits 0, confirming no hand-edited mirror drift
```

### FR-5 — Arm the gates

**Scenario: The armed gates fail on a deliberately reintroduced violation**

```gherkin
Scenario: The armed gates fail on a deliberately reintroduced violation
  Given governance-word-budget and governance-readme-completeness are registered with pre-push and
    ci surfaces per FR-5's repo-config.yml edit
  When a fixture file over 900 words is added under repo-governance/ and
    "rhino-cli gate run --surface=pre-push" is run
  Then the exit code is 1
  And the finding names the fixture file
```

**Scenario: `md-frontmatter`'s `ci` surface is re-registered once content is compliant**

```gherkin
Scenario: md-frontmatter's ci surface is re-registered once content is compliant
  Given every repo-governance/**/*.md file now carries when_to_use and description per FR-3/FR-4
  When Phase 4 re-adds "ci: { scope: all-file-type }" to md-frontmatter's repo-config.yml entry
  Then "rhino-cli md frontmatter validate" run against the full real repo reports 0 findings
  And the re-added ci surface does not reintroduce the Phase 1 premature-FAIL break, because the
    content it scans is now compliant
```

## Product Scope

**In scope**: `ose-primer`'s `apps/rhino-cli` boundary, `repo-governance/**/*.md`,
`.claude/agents/**/*.md`, `.claude/skills/**/*.md`, the generated mirrors
(`.cursor/`, `.opencode/`, `.amazonq/`) to the extent `npm run generate:bindings` regenerates them,
`AGENTS.md`, `CLAUDE.md`, and `repo-config.yml`'s gate registrations.

**Out of scope**: `ose-public`, `ose-private`, any `ose-primer` content outside the covered
governance surfaces (`apps/`, `libs/`, `docs/`, `specs/`, `plans/` — all already excluded from the
word-budget gate's scope via `args.exclude`, matching `ose-public`'s own exclusion list), and any
redesign of the gate mechanism itself.

## Product-Level Risks

- **Content-authoring judgment, not a scripted transform** — see `brd.md` §Business Risks; the
  delivery checklist budgets full phases for this rather than a single mechanical step.
- **The `md-frontmatter` mitigation must land in the same commit as the rhino-cli sync**, not as a
  follow-up fix, or Phase 1's own PR reproduces the exact CI break `ose-private`'s PR10 already
  hit — see FR-2's second scenario.
