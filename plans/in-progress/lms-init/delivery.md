# Delivery Plan — OSE LMS Backend Initialization

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.

This checklist is prospective. It does not authorize implementation, staging, committing, pushing,
opening pull requests, or changing either repository. Execute it only after the user explicitly
names this plan for execution.

Every command below is copyable verbatim. Where a value cannot be known at authoring time (a
resolved version, a generated checksum, a completion date), the step says how to resolve it rather
than guessing it.

> **Suggested-executor note:** `swe-java-dev` does not exist in `.claude/agents/swe/` today. Phase 2
> creates it; only Phase 3 and Phase 4 checkboxes name it. Every other suggested executor cited
> below was verified present in the current commit.

## Delivery Mode

`worktree-to-pr`, applied independently to `ose-public` and `ose-private`. The plan is single-sourced
in `ose-public`. Each repository has its own worktree, branch, commits, pull request,
current-head/base CI, rules-propagation evidence, merge, and cleanup.

`worktree-to-pr` is mandatory in `ose-public`: `main` is branch-protected including for admins, so
neither direct-push mode has an executable path there. `ose-private` retains a narrow
infrastructure-as-code exception that this plan does **not** invoke — DU1 is application source, not
infrastructure.

`[AI]` merges each pull request once exact-current-head/base `pr-quality-gate.yml`, one authenticated
clean current-head `pr-leak-review`, and the applicable surface gates all hold. No `[HUMAN]` merge
gate is declared.

## Worktree

- Public: `R-PUB:worktrees/lms-init/`
- Private: `R-PRI:worktrees/lms-init/`

Provisioning status: public provisioned, private pending.

The public worktree was provisioned before this plan was written and is where every plan document
was authored. The private worktree is provisioned at Step 0 of execution, before any DU1 work.

```bash
# Public — already provisioned; recovery-only, do not re-run for the registered root
claude --worktree lms-init

# Private — provisioned at Step 0, run from the ose-private repository root
claude --worktree lms-init
```

The plan-execution Step 0 gate enters these worktrees by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and — capped at one per
repository per plan and reused across every delivery unit landed there — removes each one
immediately once the plan is done using that repository, not deferred to archival.

### Provisioned Worktree Identity

- Public declared repository-relative route: `worktrees/lms-init/`
- Public initial branch: `worktree/lms-init`
- Private declared repository-relative route: `worktrees/lms-init/`
- Private initial branch: `worktree/lms-init`
- Created by: the plan-authoring session, through `claude --worktree`
- Created at: resolve at Step 0 from `git worktree list --porcelain` and record here; do not
  hardcode a timestamp while authoring
- Runtime location evidence: ignored Phase 0 runtime evidence only

> **Branch-name note, recorded rather than hidden:** the canonical template suggests
> `<plan-identifier>-base`. Both worktrees carry `worktree/<plan-identifier>` instead, which is the
> shape `claude --worktree` actually produces and the shape the archived
> `2026-09-04__adopt-beavernest-test-automation` plan recorded. The deviation is from the template,
> not from repository practice.

### Delivery Branch Inventory

| Branch                                | Repository    | Mode      | Lifecycle state | Proof                                                                               |
| ------------------------------------- | ------------- | --------- | --------------- | ----------------------------------------------------------------------------------- |
| `worktree/lms-init`                   | `ose-public`  | `to-pr`   | `active`        | carries the plan-authoring PR; record its number and 40-character head SHA on merge |
| `worktree/lms-init`                   | `ose-private` | `pending` | `pending`       | `git worktree add` at Step 0                                                        |
| `lms-init/du1-doctor-config`          | `ose-public`  | `to-pr`   | `pending`       | record merged PR number and 40-character head SHA at DU1                            |
| `lms-init/du1-doctor-config`          | `ose-private` | `to-pr`   | `pending`       | record merged PR number and 40-character head SHA at DU1                            |
| `lms-init/du2-java-enablement`        | `ose-public`  | `to-pr`   | `pending`       | record merged PR number and 40-character head SHA at DU2                            |
| `lms-init/du3-contract-and-service`   | `ose-public`  | `to-pr`   | `pending`       | record merged PR number and 40-character head SHA at DU3                            |
| `lms-init/du4-e2e-and-reconciliation` | `ose-public`  | `to-pr`   | `pending`       | record merged PR number and 40-character head SHA at DU4                            |

Append every plan-created delivery branch before use. Before removal, classify every entry as
delivered, unused, or retained/escalated; an active or unrecorded branch blocks cleanup.

### Cross-Repository Parity Identity

- Objective slug: `lms-init`
- Common worktree basename: `lms-init`

| Repository    | Corresponding short-lived branch |
| ------------- | -------------------------------- |
| `ose-public`  | `lms-init/du1-doctor-config`     |
| `ose-private` | `lms-init/du1-doctor-config`     |

DU2, DU3, and DU4 are `ose-public`-only and declare no parity branch.

---

## Phase 0: Environment Setup and Baseline

Phase 0 opens no pull request. Its outcome is a recorded clean baseline in both repositories.

### Environment Setup

- [ ] [AI] Confirm the public work location: run `rtk pwd` and confirm the path ends in
      `worktrees/lms-init`. If it does not, run `rtk git worktree list --porcelain` from the
      `ose-public` repository root and enter the worktree whose route is `worktrees/lms-init`.
- [ ] [AI] Sync the public worktree: `rtk git fetch origin` then
      `rtk git merge --ff-only origin/main`. Acceptance: the command reports either "Already up to
      date" or a fast-forward; a merge conflict here means stop and report, never force.
- [ ] [AI] Provision the private worktree. From `/Users/wkf/ose-projects/ose-private` run
      `claude --worktree lms-init`. Acceptance: `rtk git worktree list --porcelain` in that
      repository lists a worktree whose route ends in `worktrees/lms-init`. Record its route,
      branch, and creation timestamp in the Provisioned Worktree Identity section above.
- [ ] [AI] Install dependencies in the public worktree:
      `rtk ./hippo run --class ephemeral --disk-path . -- npm install`. Acceptance: exit code 0 and
      `node_modules/` exists at the worktree root.
- [ ] [AI] Install dependencies in the private worktree with the same command, run from that
      worktree's root. Acceptance: exit code 0.
- [ ] [AI] Converge tooling in both worktrees: `rtk npm run doctor -- --fix`. Acceptance: the
      command exits 0. If a tool cannot be auto-installed, record the tool name and the failure
      output in `evidence/phase-0-doctor-<repo>.txt` and report it before continuing — do not
      proceed with a broken toolchain.
- [ ] [AI] Create the Knowledge Capture scaffold at
      `plans/in-progress/lms-init/learnings.md` if it does not already exist, containing exactly the
      two HTML comments and the `# Learnings: lms-init` H1. Acceptance: `rtk cat` shows the H1 on
      the first content line — markdownlint MD041 fails the pre-commit gate without it.
- [ ] [AI] Create `plans/in-progress/lms-init/evidence/.gitkeep`. Acceptance: the directory exists
      and every later evidence step has a destination.

### Resolve the Pinned Versions

`tech-docs.md` §3 records versions verified on 2026-09-07. Re-resolve each one now; do not trust the
document. Record every resolved value in `evidence/phase-0-versions.md` as a two-column table.

- [ ] [AI] Resolve the current Java LTS major and the exact Temurin patch release:
      `rtk curl -fsSL https://api.adoptium.net/v3/info/available_releases` and read
      `most_recent_lts`. Acceptance: the value is an integer; if it is not `25`, stop and report —
      a different LTS changes `tech-docs.md` §3 and D-2 before any code is written.
- [ ] [AI] Resolve the latest Spring Boot GA:
      `rtk curl -fsSL https://api.github.com/repos/spring-projects/spring-boot/releases/latest | jq -r .tag_name`.
      Acceptance: a `v4.x.y` tag. Record it; use it in `build.gradle.kts` at DU3.
- [ ] [AI] Resolve the latest Gradle release:
      `rtk curl -fsSL https://api.github.com/repos/gradle/gradle/releases/latest | jq -r .tag_name`.
      Acceptance: a `v9.x.y` tag at or above `v9.1.0` — below that, Gradle cannot run on Java 25 and
      D-3 must be revisited before proceeding.
- [ ] [AI] Resolve the Gradle distribution SHA-256 for that version:
      `rtk curl -fsSL https://services.gradle.org/distributions/gradle-<version>-bin.zip.sha256`.
      Acceptance: a 64-character hex string. This is the `distributionSha256Sum` value for DU3.
- [ ] [AI] Resolve the latest Cucumber-JVM, JaCoCo, Spotless-Gradle, and google-java-format
      versions from their respective `releases/latest` GitHub API endpoints and the Gradle Plugin
      Portal page for `com.diffplug.spotless`. Acceptance: four concrete version strings recorded in
      `evidence/phase-0-versions.md`.

### Record the Baseline

- [ ] [AI] Capture the public baseline:
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run-many -t lint,test:quick --parallel=1`
      with output saved to `evidence/phase-0-baseline-public.txt`. Acceptance: exit code 0.
- [ ] [AI] Capture the private baseline with the same command from the private worktree, saved to
      `evidence/phase-0-baseline-private.txt`. Acceptance: exit code 0.
- [ ] [AI] Verify cross-repository parity is green before touching it: run
      `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- run rhino-cli:test:quick`
      in **both** worktrees, and diff the two manifests:
      `rtk diff -u /Users/wkf/ose-projects/ose-public/worktrees/lms-init/apps/rhino-cli/parity-manifest.sha256 /Users/wkf/ose-projects/ose-private/worktrees/lms-init/apps/rhino-cli/parity-manifest.sha256`.
      Acceptance: the diff is empty. A non-empty diff is preexisting drift that must be fixed before
      DU1 begins, not carried into it.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> This follows the root cause orientation principle — proactively fix preexisting errors encountered
> during work.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] Both worktrees exist, are synced with their `origin/main`, and are recorded in the
      Provisioned Worktree Identity section with real values.
- [ ] [AI] `rtk npm run doctor` exits 0 in both worktrees.
- [ ] [AI] Both baseline captures exit 0 and are saved under `evidence/`.
- [ ] [AI] The two `parity-manifest.sha256` files are byte-identical.
- [ ] [AI] `evidence/phase-0-versions.md` records a resolved value for every row of
      `tech-docs.md` §3, and any divergence from the authored values has been reported.

> **Pause Safety**: nothing has been modified in either repository beyond untracked plan evidence.
> Safe to stop. To resume: re-run the two baseline commands and confirm both still exit 0.

---

## Phase 1 (DU1): Config-Driven Doctor Tool Inventory

Delivers one pull request per repository, byte-identical in `apps/rhino-cli`.

### AC-DOCTOR-01 — A repo-config-declared extra tool is probed like a built-in tool

- **Input:** AC-DOCTOR-01 (canonical Gherkin in `prd.md`), the existing hardcoded inventories at
  `apps/rhino-cli/src/RhinoCli.Application/src/Doctor.fs:779` and
  `.../RepoConfig.fs:172`, and the existing `doctor.skip-tools` wiring at `Doctor.fs:1791`.
- **Outcome:** a tool declared under `doctor.extra-tools` in `repo-config.yml` is accepted by
  `--tools`, probed, and reported exactly like a built-in tool.

- [ ] [AI] **RED (schema):** add the two scenarios from `prd.md` AC-DOCTOR-01 and AC-DOCTOR-02 to
      `specs/apps/rhino/cli/behaviours/system/doctor.feature`, placed after the existing "A
      repo-config-declared tool is skipped from the check" scenario. Run
      `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- run rhino-cli:test:coverage:behaviour`;
      acceptance: it fails reporting `undefined Unit binding` for the new steps. Save the output to
      `evidence/du1-red-coverage.txt`.
  - _Suggested executor: `specs-maker`_
- [ ] [AI] **RED (unit):** add failing unit cases to the RhinoCli unit test project. Discover the
      exact file list first with
      `rtk grep -n "Doctor" apps/rhino-cli/tests/unit/*.fsproj` and add cases to the file that
      already covers `doctorToolInventory`. Cover: an `extra-tools` entry appears in the inventory;
      an entry not in either inventory is still rejected; a probe reading a stderr-only version
      string parses correctly. Run
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run rhino-cli:test:unit`;
      acceptance: the new cases fail because `ExtraTools` does not exist yet.
  - _Suggested executor: `swe-fsharp-dev`_
- [ ] [AI] **GREEN (config schema):** in
      `apps/rhino-cli/src/RhinoCli.Application/src/RepoConfig.fs`, add an `ExtraTools` field to the
      `DoctorSection` record (beside `SkipTools` at line 208) and to its DTO (beside line 331), with
      the shape in `tech-docs.md` §D-5: `name`, `binary`, `version-args`, `version-stream`,
      `required-version`, and an `install` map. Default it to the empty list in both constructors.
      Run `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- run rhino-cli:typecheck`;
      acceptance: exit code 0.
  - _Suggested executor: `swe-fsharp-dev`_
- [ ] [AI] **GREEN (inventory):** replace the module-level `doctorToolInventory` list in
      `RepoConfig.fs` with a `builtinDoctorToolInventory` list plus a
      `doctorToolInventoryFor (config: RepoConfig)` function that appends the configured names.
      Change `doctorToolsSemanticFindings` (line 1238) to take the resolved inventory rather than
      reading the module-level list. Apply the same split in `Doctor.fs` at line 779 and thread the
      resolved inventory into `parseDoctorToolName` at line 811. Rerun
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run rhino-cli:test:unit`;
      acceptance: the previously failing cases pass and no existing case regresses.
  - _Suggested executor: `swe-fsharp-dev`_
- [ ] [AI] **GREEN (probe):** extend the version-probe path in `Doctor.fs` so a `ToolDef` may read
      merged stderr. Build `ToolDef` values for configured extra tools in `buildToolDefs`, appending
      them after the built-ins so `selectToolDefs` (line 1767) filters and selects them unchanged.
      Rerun the unit target; acceptance: the stderr-parsing case passes.
  - _Suggested executor: `swe-fsharp-dev`_
- [ ] [AI] **GREEN (bindings):** bind the two new Gherkin scenarios. Reuse the existing bindings for
      steps already defined by the "unknown selected tool" scenario — declaring a second binding for
      the same step text makes `behaviour-coverage.mjs` report an ambiguity error, not a duplicate
      warning. Rerun
      `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- run rhino-cli:test:coverage:behaviour`;
      acceptance: exit code 0 with no undefined, ambiguous, or unused bindings.
  - _Suggested executor: `swe-fsharp-dev`_
- [ ] [AI] **GREEN (config key, both repos):** add the `doctor.extra-tools` key to `repo-config.yml`
      in **both** worktrees. In `ose-public` set it to an empty list for now — DU2 populates it. In
      `ose-private` set it to an empty list permanently. Run
      `rtk npm run validate:config` in both; acceptance: exit code 0 in both, and
      `rhino-cli repo-config validate` reports the canonical key set matches.
- [ ] [AI] **REFACTOR:** remove any now-duplicated inventory literal so exactly one built-in list
      exists per file, and confirm the two files still express the same list. Run
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run rhino-cli:test:quick`;
      acceptance: exit code 0, including the 99% line-coverage floor, with behaviour and diagnostics
      unchanged.
  - _Suggested executor: `swe-fsharp-dev`_
- **Proof:** `evidence/du1-red-coverage.txt` showing the initial failure, plus a passing
  `rhino-cli:test:quick` in both repositories.

### Byte-Identity Reconciliation

- [ ] [AI] Copy the changed `apps/rhino-cli` sources into the private worktree so both trees are
      byte-identical. Verify per file, not by eye:
      `rtk diff -ru /Users/wkf/ose-projects/ose-public/worktrees/lms-init/apps/rhino-cli/src /Users/wkf/ose-projects/ose-private/worktrees/lms-init/apps/rhino-cli/src`.
      Acceptance: the diff is empty.
- [ ] [AI] Regenerate the parity manifest in both worktrees using the repository's own command —
      discover it first with
      `rtk grep -n "parity" apps/rhino-cli/project.json` and use the target it declares rather than
      hand-editing hashes. Acceptance: `apps/rhino-cli/parity-manifest.sha256` changes in both.
- [ ] [AI] Diff the two regenerated manifests:
      `rtk diff -u /Users/wkf/ose-projects/ose-public/worktrees/lms-init/apps/rhino-cli/parity-manifest.sha256 /Users/wkf/ose-projects/ose-private/worktrees/lms-init/apps/rhino-cli/parity-manifest.sha256`.
      Acceptance: empty diff. A non-empty diff means the source copy was incomplete — fix it, never
      hand-edit the manifest to agree.

### Rules Propagation — DU1, per repository

Run the complete repository-local
[`rules-propagation`](../../../repo-governance/workflows/rules/rules-propagation.md) outcome once
for `ose-public` and once for `ose-private`. Every checkbox below is executed twice, once per
repository, and each run produces its own manifest.

- [ ] [AI] **Step 0 — intake (public):** normalize the stated rule to a falsifiable sentence: "A
      Doctor tool may be declared in `repo-config.yml` under `doctor.extra-tools`; a name absent
      from both the built-in inventory and that list is rejected." Record it in the manifest at
      `local-tmp/rules-propagation/rules-propagation__lms-init-du1-public__manifest.md`.
- [ ] [AI] **Step 0 — intake (private):** same, writing
      `...__lms-init-du1-private__manifest.md`.
- [ ] [AI] **Steps 2–3 — classification and conflict scan (public):** inventory every surface that
      currently states the doctor tool inventory as closed. Search with
      `rtk grep -rln "doctorToolInventory\|doctor-tools\|skip-tools" repo-governance/ docs/ AGENTS.md CLAUDE.md .claude/`.
      Acceptance: a per-surface verdict recorded in the manifest; any higher-layer contradiction
      halts the run rather than being overridden.
- [ ] [AI] **Steps 2–3 — classification and conflict scan (private):** same search, same recording.
- [ ] [AI] **Step 4 — placement (public):** place the rule on the narrowest surface that binds. The
      expected home is the `repo-config.yml` schema documentation plus its inline comment, not
      `AGENTS.md` — the instruction surface is a fixed-size cache and this rule does not need to be
      read on every task. Record the placement decision and, if any admission is proposed to an
      instruction surface, the eviction that makes room.
- [ ] [AI] **Step 4 — placement (private):** same.
- [ ] [AI] **Step 6 — write and tidy (public):** land the canonical edit, then update every other
      surface that states the subject so none contradicts it. Acceptance: no surface still describes
      the inventory as closed.
- [ ] [AI] **Step 6 — write and tidy (private):** same.
- [ ] [AI] **Step 7 — enforcement disposition (public):** record the mandatory three-way outcome.
      The expected disposition is **enforced**: `rhino-cli repo-config validate` rejects an
      `extra-tools` entry missing a required field, and rejects a `doctor-tools` name outside the
      resolved inventory.
- [ ] [AI] **Step 7 — enforcement disposition (private):** same.
- [ ] [AI] **Step 8 — verification (public):** run `rtk npm run validate:config` and
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run rhino-cli:test:quick`.
      Acceptance: both exit 0, and every rule stated in the manifest has a binding gate or an
      explicit unenforced disposition.
- [ ] [AI] **Step 8 — verification (private):** same.
- [ ] [AI] **Step 9 — manifest and final status (public):** record the terminal state as `landed`,
      `halted`, or `partial`, with the pull request URL.
- [ ] [AI] **Step 9 — manifest and final status (private):** same.
- [ ] [AI] **Step 9 — sibling obligation:** record in each manifest that the sibling repository
      carries the matching obligation, naming the other repository and its PR. Neither manifest may
      record `none` — this rule is inherently paired.

### Local Quality Gates (Before Push) — DU1

Run in **both** worktrees.

- [ ] [AI] Run affected typecheck:
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- affected -t typecheck`
- [ ] [AI] Run affected linting: `rtk npm run affected:lint`
- [ ] [AI] Run affected quick tests: `rtk npm run affected:test`
- [ ] [AI] Run affected spec coverage:
      `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- affected -t test:coverage:behaviour`
- [ ] [AI] Fix ALL failures found — including preexisting issues not caused by these changes
- [ ] [AI] Verify all checks pass before pushing

### Commit Guidelines — DU1

- [ ] [AI] Do not stage or commit until the user explicitly authorizes the named change set
- [ ] [AI] Once authorized, use the fewest build-valid, independently reviewable and revertible
      commits, one coherent purpose each; no extra boundary prompt unless the user prescribed one
- [ ] [AI] Follow Conventional Commits: expected shape
      `refactor(rhino-cli): resolve the doctor tool inventory from repo-config`
- [ ] [AI] Keep the Gherkin, unit tests, `repo-config.yml` key, and regenerated
      `parity-manifest.sha256` in the same commit as the source change they complete
- [ ] [AI] Do not extend a commit beyond the user-authorized change set

### Post-Push Verification — DU1

- [ ] [AI] Create the branch and push in the public worktree:
      `rtk git switch -c lms-init/du1-doctor-config` then
      `rtk git push -u origin lms-init/du1-doctor-config`
- [ ] [AI] Create the branch and push in the private worktree with the identical branch name
- [ ] [AI] Open a draft pull request against `main` in each repository, cross-linking the two in
      both bodies. Each body states the new-code cost and benefit; tests are exempt from that
      statement
- [ ] [AI] Poll CI every 2 minutes with
      `rtk gh pr checks <number> --repo wahidyankf/<repo>`. Never use `gh run watch`
- [ ] [AI] Verify the `Quality gate` check from `.github/workflows/pr-quality-gate.yml` passes for
      each pull request's exact current head and base
- [ ] [AI] Verify one authenticated clean current-head `pr-leak-review` on each pull request
- [ ] [AI] If any CI check fails, fix at the root cause and push a follow-up commit; never bypass
- [ ] [AI] Do NOT proceed to Phase 2 until CI is green on both pull requests
- [ ] [AI] Mark both pull requests ready and merge them, public first, then private within the same
      working session so the nightly parity audit never observes a mismatched pair
- [ ] [AI] Record each merged pull request number and its 40-character reviewed-head SHA in the
      Delivery Branch Inventory

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [ ] [AI] Both pull requests are merged and both branches are recorded as delivered in the
      inventory
- [ ] [AI] `rtk gh workflow run rhino-cli-parity-audit.yml --repo wahidyankf/ose-private` completes
      successfully against the merged state; save the run URL to `evidence/du1-parity-audit.txt`
- [ ] [AI] `rtk npm run validate:config` exits 0 in both repositories on the merged `main`
- [ ] [AI] `rtk npm run doctor` still exits 0 in both worktrees with `extra-tools` empty — proving
      the refactor is a no-op until a tool is declared

> **Pause Safety**: both repositories carry an identical, behaviour-preserving `rhino-cli` with an
> unused new configuration key. Nothing depends on it yet. Safe to stop. To resume:
> `rtk npm run validate:config` in both repositories.

---

## Phase 2 (DU2): Java Language Enablement

One pull request in `ose-public`. No Java project exists yet; this phase makes one possible.

### AC-COV-01 through AC-COV-03 — The behaviour-coverage validator reads Java bindings

- **Input:** AC-COV-01..03 (`prd.md`), `scripts/behaviour-coverage.mjs:20` `BINDING_FILE`,
  `:326` `extractTypescriptBindings`, `:352` `extractFsharpBindings`, and `:374` `extractBindings`.
- **Outcome:** a `.java` file is scanned, and each `@Given` / `@When` / `@Then` annotation becomes
  exactly one binding carrying its Cucumber expression.

- [ ] [AI] **RED:** add three cases to `scripts/behaviour-coverage.test.mjs` — one asserting
      `extractBindings("Steps.java", source)` returns a binding per annotation, one asserting an
      unbound scenario produces `undefined Unit binding`, one asserting an unmatched Java binding
      produces `unused Unit binding`. Run `rtk npm run test:validators`; acceptance: all three fail
      because `.java` is not scanned. Save output to `evidence/du2-red-validator.txt`.
- [ ] [AI] **GREEN:** in `scripts/behaviour-coverage.mjs`, extend `BINDING_FILE` to
      `/\.(?:ts|tsx|fs|java)$/iu`, add `extractJavaBindings` matching
      `@(Given|When|Then)("<expression>")` on annotated methods, add `javaFeatureReferences`
      mirroring `fsharpFeatureReferences`, and route `.java` in `extractBindings`. Set
      `keywordSensitive: true` and `expression: true`, matching how Cucumber-JVM actually resolves
      steps. Rerun `rtk npm run test:validators`; acceptance: all three cases pass.
- [ ] [AI] **REFACTOR:** factor the shared quoted-literal feature-reference scan used by the F# and
      Java extractors into one helper rather than a third near-copy. Rerun
      `rtk npm run test:validators` and
      `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- affected -t test:coverage:behaviour`;
      acceptance: both exit 0 and every existing project's coverage result is unchanged.
- **Proof:** `evidence/du2-red-validator.txt` plus a passing `npm run test:validators`.

### AC-FMT-01 and AC-FMT-02 — Java formatting is gated

- **Input:** AC-FMT-01, AC-FMT-02, the `format-elixir` gate pair at `repo-config.yml:566` and
  `:575`, and `scripts/format-elixir.sh`.
- **Outcome:** `.java` files are formatted at pre-commit and verified in the CI
  `formatting-verify` group.

- [ ] [AI] Create `scripts/format-java.sh` modelled on `scripts/format-elixir.sh`: discover each
      Gradle project owning the passed files, run `spotlessApply` by default and `spotlessCheck`
      under `--check`, and exit non-zero on any non-zero sub-command. Run
      `rtk shellcheck scripts/format-java.sh` and `rtk shfmt -d scripts/format-java.sh`;
      acceptance: both exit 0.
- [ ] [AI] Register the gate pair in `repo-config.yml` beside the other formatter pairs:
      `format-java` (`type: mutation`, `category: formatter`, `command: scripts/format-java.sh`,
      `kind: external`, `restages: true`, `surfaces.pre-commit` scoped `affected-file-type` on
      `"*.java"`) and `format-verify-java` (`type: check`,
      `command: scripts/format-java.sh --check`, `ci-group: formatting-verify`,
      `verifies: format-java`, `surfaces.ci` on the same glob). Run
      `rtk npm run validate:config`; acceptance: exit code 0.
- [ ] [AI] Prove both gates actually fire. In a scratch directory outside the worktree, create an
      isolated no-origin git fixture, stage a deliberately misformatted `.java` file, run the gate
      runner, and confirm `Running gate format-java` appears in the output. Repeat with `--check`
      for `format-verify-java`. Save both transcripts to `evidence/du2-gate-trigger.txt`.
      Acceptance: both gate names appear; a gate that never fires reads as green while doing
      nothing.

### AC-CI-01 — CI routes Java work to the Java job only

- **Input:** AC-CI-01, `.github/workflows/pr-quality-gate.yml` `detect` (line 22), `typescript`
  (line 288), `dotnet` (line 304), `flutter` (line 336), and `quality-gate` (line 371).
- **Outcome:** a Java-only change runs a Java gate job and is excluded from the other three.

- [ ] [AI] Create `.github/actions/setup-java/action.yml` as a composite action: install Temurin at
      the Phase 0 resolved LTS via `actions/setup-java@v5`, and cache Gradle via
      `gradle/actions/setup-gradle`. Follow the self-hosted/GitHub-hosted split
      `.github/actions/setup-dotnet/action.yml` already implements rather than inventing a new
      shape. Run `rtk actionlint`; acceptance: exit code 0.
- [ ] [AI] Edit `.github/workflows/pr-quality-gate.yml`: add `has-java` to the `detect` job outputs,
      add `has-java=false` to the initial output block, add `echo "has-java=true"` to the fail-safe
      fallback block, and add a `lang:java) echo "has-java=true" >> "$GITHUB_OUTPUT" ;;` arm to the
      per-tag `case`. Acceptance: `rtk actionlint` exits 0.
- [ ] [AI] Add a `java` job gated on `needs.detect.outputs.has-java == 'true'`, running
      `npx nx affected -t typecheck lint test:quick compat:min-version --exclude='tag:lang:ts,tag:lang:fsharp,tag:lang:csharp,tag:lang:rust,tag:lang:dart' --parallel=1`
      after `setup-node` and `setup-java`. Acceptance: `rtk actionlint` exits 0.
- [ ] [AI] Add `tag:lang:java` to the `--exclude` list of the `typescript`, `dotnet`, and `flutter`
      jobs. Acceptance: `rtk grep -n "tag:lang:java" .github/workflows/pr-quality-gate.yml` returns
      four lines — the new job's siblings plus the three exclusions.
- [ ] [AI] Add `java` to the `quality-gate` job's `needs` list. Acceptance: the aggregate gate
      cannot report success while the Java job failed.

### Language Vocabulary, Documentation, and Agents

- [ ] [AI] Edit
      `repo-governance/development/infra/nx-targets/tag-convention-four-dimension-scheme.md`: add
      `java` to the `lang:` allowed values and `springboot` to the `platform:` allowed values.
      Acceptance: both appear in the controlled-vocabulary table.
  - _Suggested executor: `rules-maker`_
- [ ] [AI] Edit
      `repo-governance/development/infra/nx-targets/tag-convention-current-tags-and-examples.md` to
      add the `ose-lms-be` tag set as a copyable example.
  - _Suggested executor: `rules-maker`_
- [ ] [AI] Create the four Java style-guide documents under
      `docs/explanation/software-engineering/programming-languages/java/`: `README.md` (including
      the Rule-3 prerequisite statement the separation convention requires),
      `coding-standards.md`, `testing-standards.md`, `error-handling-standards.md`. Each documents
      repository-specific conventions only — never a Java language tutorial, which belongs to
      ayokoding-www. Acceptance: `rtk npm run lint:md` exits 0 and each file carries the frontmatter
      the `md-frontmatter` gate requires.
  - _Suggested executor: `docs-maker`_
- [ ] [AI] Edit `docs/explanation/software-engineering/programming-languages/README.md`: add Java to
      the documentation-pattern list, the "Which Language for My Task" table, and the Platform
      Guidance list, stating it is active for the LMS backend only and is not the default for new
      backends.
  - _Suggested executor: `docs-maker`_
- [ ] [AI] Create `.claude/skills/swe-programming-java/SKILL.md`, sourcing the four documents above,
      modelled on `.claude/skills/swe-programming-fsharp/SKILL.md`. Acceptance: the file is under
      the 750-word governance fail threshold — check with
      `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- run rhino-cli:test:quick`
      after the edit, which runs the word-budget gate.
- [ ] [AI] Create `.claude/agents/swe/swe-java-dev.md` modelled on
      `.claude/agents/swe/swe-fsharp-dev.md`, referencing the new skill. Acceptance: same word
      budget check passes.
  - _Suggested executor: `agent-maker`_
- [ ] [AI] Update `.claude/agents/swe/README.md` and `.claude/skills/README.md` with annotated index
      entries. Acceptance: the `governance-readme-completeness` gate reports no `missing` or
      `unannotated` finding for either path.
- [ ] [AI] Regenerate every harness mirror in one command: `rtk npm run generate:bindings`. Then
      validate: `rtk npm run validate:sync` and `rtk npm run harness:bindings-validation`.
      Acceptance: both exit 0, and the generated `.opencode/`, `.codex/`, and `.agents/` files are
      staged in the same commit as their `.claude/` sources. Never hand-edit a mirror.
- [ ] [AI] Declare the `java` tool in `repo-config.yml` under `doctor.extra-tools`, using the shape
      in `tech-docs.md` §D-5 and the Phase 0 resolved LTS. Run `rtk npm run doctor`; acceptance: the
      output now includes a `java` row reporting the installed JDK version, proving the stderr probe
      works on a real machine. Save the output to `evidence/du2-doctor-java.txt`.
- [ ] [AI] Add the `ose-lms-be` row to `docs/reference/web-sites.md` — both the app table (port 8303) and the port-variable table (`OSE_LMS_BE_PORT`). Acceptance: `rtk npm run lint:md` exits
      0 and both tables carry the row.

### Rules Propagation — DU2 (`ose-public` only)

- [ ] [AI] **Step 0 — intake:** normalize each stated rule to a falsifiable sentence: the `lang:`
      and `platform:` vocabulary additions, the `.java` pre-commit formatting obligation, and the
      Java-job CI routing obligation. Record all three in
      `local-tmp/rules-propagation/rules-propagation__lms-init-du2__manifest.md`.
- [ ] [AI] **Steps 2–3 — classification and conflict scan:** inventory every surface stating the
      language vocabulary or the formatter registry. Search with
      `rtk grep -rln "lang:ts\|lang:fsharp\|formatting-verify" repo-governance/ docs/ .github/ AGENTS.md CLAUDE.md`.
      Record a per-surface verdict and halt on any higher-layer contradiction.
- [ ] [AI] **Step 4 — placement and eviction:** place each rule on the narrowest surface that binds
      — the tag convention for vocabulary, `repo-config.yml` for the formatter, the workflow for CI
      routing. Confirm no admission to `AGENTS.md` or `CLAUDE.md` is proposed; if one is, name the
      eviction that makes room rather than raising a threshold.
- [ ] [AI] **Step 6 — write and tidy:** land the canonical edits, then reconcile every other surface
      that states the same subject, including the languages README and the platform-bindings catalog
      if the new agent changes a claim there.
- [ ] [AI] **Step 7 — enforcement disposition:** record the three-way outcome per rule. Expected:
      vocabulary **enforced** by `repo-config validate` plus the tag convention; formatting
      **enforced** by the gate pair; CI routing **enforced** by the `quality-gate` aggregate needing
      the `java` job.
- [ ] [AI] **Step 8 — binding generation and verification:** run `rtk npm run generate:bindings`,
      `rtk npm run validate:sync`, `rtk npm run harness:bindings-validation`,
      `rtk npm run validate:config`, and `rtk npm run lint:md`. Acceptance: all exit 0 and every
      manifest rule has a binding gate or an explicit unenforced disposition.
- [ ] [AI] **Step 9 — manifest, final status, and sibling obligation:** record the terminal state
      and the pull request URL. Record the sibling obligation explicitly as `none` — DU2 changes no
      parity-manifest file and no `repo-config.yml` key, only values on keys that already exist in
      both repositories.

### Local Quality Gates (Before Push) — DU2

- [ ] [AI] Run affected typecheck:
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- affected -t typecheck`
- [ ] [AI] Run affected linting: `rtk npm run affected:lint`
- [ ] [AI] Run affected quick tests: `rtk npm run affected:test`
- [ ] [AI] Run the validator suite: `rtk npm run test:validators`
- [ ] [AI] Run affected spec coverage:
      `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- affected -t test:coverage:behaviour`
- [ ] [AI] Fix ALL failures found — including preexisting issues not caused by these changes

### Commit Guidelines — DU2

- [ ] [AI] Do not stage or commit until the user explicitly authorizes the named change set
- [ ] [AI] Expected commit shape: `feat(repo): enable java projects across the quality surfaces`
- [ ] [AI] Keep each `.claude/` source and its generated mirrors in the same commit; split the
      validator change, the gate change, and the CI change only if each stands alone as build-valid
- [ ] [AI] Do not extend a commit beyond the user-authorized change set

### Post-Push Verification — DU2

- [ ] [AI] `rtk git switch -c lms-init/du2-java-enablement` then
      `rtk git push -u origin lms-init/du2-java-enablement`
- [ ] [AI] Open a draft pull request against `main`; the body states the new-code cost and benefit
- [ ] [AI] Poll CI every 2 minutes with `rtk gh pr checks <number>`. Never use `gh run watch`
- [ ] [AI] Verify exact-current-head/base `Quality gate` passes and one clean current-head
      `pr-leak-review` is recorded
- [ ] [AI] Confirm the `Java quality gate` job reports **skipped** on this pull request — no Java
      project exists yet, and a job that runs here would mean the detection is wrong
- [ ] [AI] If any check fails, fix at the root cause and push a follow-up commit; never bypass
- [ ] [AI] Mark ready, merge, and record the pull request number and 40-character head SHA

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [ ] [AI] `rtk npm run test:validators` exits 0 with the three Java binding cases passing
- [ ] [AI] `rtk npm run validate:config` exits 0 with the `java` extra tool declared
- [ ] [AI] `rtk npm run doctor` reports a `java` row with a real version
- [ ] [AI] `rtk actionlint` exits 0 and `tag:lang:java` appears in all three existing job excludes
- [ ] [AI] `evidence/du2-gate-trigger.txt` shows both formatter gates firing
- [ ] [AI] `rtk npm run validate:sync` and `rtk npm run harness:bindings-validation` exit 0
- [ ] [AI] The full baseline still passes:
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run-many -t lint,test:quick --parallel=1`

> **Pause Safety**: the repository can now build, format, test, and gate a Java project. No Java
> project exists, so every new gate is inert. `main` is deployable and no behaviour changed. Safe to
> stop. To resume: re-run the Phase 2 Gate checks.

---

## Phase 3 (DU3): Contract and Service

One pull request in `ose-public`.

### Specs Corpus and Contract

- [ ] [AI] Create the owner corpus skeleton at `specs/apps/ose/lms-be/`: `README.md`,
      `architecture.md` (C4 context, containers, and components as sections in one document), and
      `behaviours/README.md`. Acceptance:
      `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- run ose-be:specs:structure-validation`
      reports no `adoption` finding for `specs/apps/ose/lms-be` — the validator discovers new owners
      by folder walk and needs no registration.
  - _Suggested executor: `specs-maker`_
- [ ] [AI] Write the four feature files verbatim from `prd.md`: `behaviours/health/health.feature`,
      `behaviours/health/actuator.feature`, `behaviours/hello/hello.feature`, and
      `behaviours/config/port-resolution.feature`, each with a domain `README.md` stating its
      scenario count. Acceptance: the structure validator reports no `count` finding.
  - _Suggested executor: `specs-maker`_
- [ ] [AI] Create `specs/apps/ose/lms-be/contracts/` mirroring
      `specs/apps/ose/be/contracts/`: `openapi.yaml`, `.spectral.yaml`, `paths/` with one file per
      endpoint, `schemas/` with `HealthResponse` and `HelloResponse`, `README.md`, and a
      `project.json` named `ose-lms-contracts` with `lint`, `bundle`, `docs`, `typecheck`,
      `test:quick`, `deps:audit`, `compat:min-version`, `specs:structure-validation`, and a
      `namedInputs.specs` entry — the last is required of every Nx-registered project by the
      byte-identity standard's rule 2. Acceptance:
      `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- run ose-lms-contracts:lint`
      exits 0.
- [ ] [AI] Add `specs/apps/ose/lms-be/contracts/generated/` to `.gitignore`, matching the `ose-be`
      sibling's treatment of build output. Acceptance: `rtk git status --short` shows no generated
      contract artifacts after a bundle run.
- [ ] [AI] Update `specs/apps/ose/README.md` Contents and `specs/apps/ose/overview.md` with an OSE
      LMS product section. Acceptance: `rtk npm run lint:md` exits 0 and the structure validator
      reports no `links` finding.

### Project Scaffold

- [ ] [AI] Generate the Gradle wrapper at the Phase 0 resolved version:
      `rtk ./hippo run --class transactional --disk-path apps/ose-lms-be -- gradle wrapper --gradle-version <resolved>`.
      Then set `distributionSha256Sum` in `apps/ose-lms-be/gradle/wrapper/gradle-wrapper.properties`
      to the Phase 0 resolved checksum. Acceptance:
      `rtk ./hippo run --class ephemeral --disk-path apps/ose-lms-be -- ./gradlew --version` prints
      the expected version without a checksum warning.
- [ ] [AI] Write `apps/ose-lms-be/build.gradle.kts` with: the Spring Boot and dependency-management
      plugins at the resolved version; `java { toolchain { languageVersion = JavaLanguageVersion.of(25) } }`;
      Spotless applying `googleJavaFormat()`; JaCoCo with a `jacocoTestCoverageVerification` rule at
      `LINE` `0.99` excluding only `**/OseLmsBeApplication.class`; and Cucumber-JVM with
      `cucumber-java`, `cucumber-spring`, and `cucumber-junit-platform-engine`. Acceptance:
      `rtk ./hippo run --class transactional --disk-path apps/ose-lms-be -- ./gradlew build -x test`
      exits 0.
  - _Suggested executor: `swe-java-dev`_
- [ ] [AI] Create `apps/ose-lms-be/project.json` with tags
      `["type:app", "platform:springboot", "lang:java", "domain:ose"]`, `implicitDependencies:
  ["ose-lms-contracts"]`, and targets `codegen`, `build`, `typecheck`, `lint`, `dev`, `run`,
      `test:unit`, `test:quick`, `test:coverage:unit`, `test:coverage:behaviour`, `test:coverage`,
      `deps:audit`, `compat:min-version`,
      `specs:structure-validation`, plus `namedInputs.specs`. Declare **no** `test:coverage:e2e`
      yet — Phase 4 adds it together with the project it validates, so no phase ever leaves a
      coverage target pointing at a directory that does not exist. Declare **no** `test:integration` or
      `test:coverage:integration` — the service owns no local resource boundary and an echo target
      is forbidden. Compose `test:quick` with `nx:run-commands`, object-form commands,
      `"forwardAllArgs": false` on every command and on the options object, and
      `"parallel": false`. Acceptance:
      `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- show project ose-lms-be --json`
      lists every target above and no others.
- [ ] [AI] Create `apps/ose-lms-be/behaviour-coverage.json` with `project: "ose-lms-be"`,
      `corpus: ["../../specs/apps/ose/lms-be/behaviours"]`, and the `unit` adapter only (bindings
      `["src/test/java"]`, driver `build.gradle.kts`). Phase 4 adds the `e2e` adapter alongside the
      project it points at. Acceptance: the file parses, names no `integration` adapter, and
      `ose-lms-be:test:coverage:unit` exits 0.
- [ ] [AI] Create `apps/ose-lms-be/README.md` stating the corpus path, both adapters, every target
      name, and an explicit paragraph explaining why the Integration layer is inapplicable.
      Acceptance: `rtk npm run lint:md` exits 0.
- [ ] [AI] Create `apps/ose-lms-be/.gitignore` (`build/`, `.gradle/`, `generated-contracts/`),
      `.editorconfig`, `LICENSE` copied from `apps/ose-be/LICENSE`, and `.env.example` declaring
      `OSE_LMS_BE_PORT` with no real value. Acceptance: `rtk npm run validate:config` and the
      `env-staged-guard` gate both pass.
- [ ] [AI] Wire the `codegen` target: `npx openapi-generator-cli generate` against
      `specs/apps/ose/lms-be/contracts/generated/openapi-bundled.yaml` with `-g spring`,
      `--model-package com.oseplatform.lms.contracts`,
      `--global-property=models,modelDocs=false,apiDocs=false`, and
      `--additional-properties=useJakartaEe=true`, with `dependsOn: ["ose-lms-contracts:bundle"]`.
      Run `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run ose-lms-be:codegen`;
      acceptance: exit code 0 and `generated-contracts/` contains model sources importing
      `jakarta.validation`, not `javax.validation`. If the models do not compile against Spring
      Boot 4, apply the pre-authorized D-7 fallback and record it in `learnings.md`.

### AC-PORT-01 through AC-PORT-03 — Listener port resolution

- **Input:** AC-PORT-01..03, `specs/apps/ose/lms-be/behaviours/config/port-resolution.feature`, and
  the resolution order documented in `docs/reference/web-sites.md`: explicit flag, then the
  prefixed variable, then the default.
- **Outcome:** the port resolves in that order and a malformed value fails at startup rather than
  falling back silently.

- [ ] [AI] **RED:** create `apps/ose-lms-be/src/test/java/com/oseplatform/lms/steps/PortResolutionSteps.java`
      binding the six distinct steps of the three scenarios. Run
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run ose-lms-be:test:unit`;
      acceptance: it fails because `PortResolver` does not exist. Save output to
      `evidence/du3-red-port.txt`.
  - _Suggested executor: `swe-java-dev`_
- [ ] [AI] **GREEN:** create `apps/ose-lms-be/src/main/java/com/oseplatform/lms/config/PortResolver.java`
      as a pure class taking the flag value and the environment value as parameters — no Spring
      annotations, no direct `System.getenv` call, so it is provable in-process. Rerun the unit
      target; acceptance: all three scenarios pass.
  - _Suggested executor: `swe-java-dev`_
- [ ] [AI] **REFACTOR:** extract the default `8303` and the variable name `OSE_LMS_BE_PORT` to named
      constants and reference them from `application.yaml` rather than repeating literals. Rerun
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run ose-lms-be:test:quick`;
      acceptance: exit code 0 and behaviour is unchanged.
  - _Suggested executor: `swe-java-dev`_
- **Proof:** `evidence/du3-red-port.txt` plus a passing `ose-lms-be:test:unit`.

### AC-HEALTH-01 and AC-HELLO-01 — The two endpoints

- **Input:** AC-HEALTH-01, AC-HELLO-01, and the generated contract models.
- **Outcome:** both endpoints return `200` with the contracted body.

- [ ] [AI] **RED:** create `RunCucumberTest.java` (the JUnit Platform suite entry point),
      `steps/CucumberSpringConfiguration.java` annotated `@CucumberContextConfiguration` and
      `@SpringBootTest(webEnvironment = MOCK)` with `@AutoConfigureMockMvc`, and `steps/HttpSteps.java`
      binding exactly three step expressions — `the ose-lms-be service is running`,
      `I send GET {word}`, `the response status is {int}`, and
      `the response body has a {string} field equal to {string}`. Declare each expression exactly
      once across the whole test source set; a second binding for the same text is an ambiguity
      error, not a duplicate. Run
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run ose-lms-be:test:unit`;
      acceptance: the health and hello scenarios fail with `404`.
  - _Suggested executor: `swe-java-dev`_
- [ ] [AI] **GREEN:** create `health/HealthController.java` returning
      `{"status":"healthy"}` at `GET /api/v1/health` and `hello/HelloController.java` returning
      `{"message":"Hello, world!"}` at `GET /api/v1/hello`, both using the generated contract models
      rather than inline maps. Rerun the unit target; acceptance: both scenarios pass.
  - _Suggested executor: `swe-java-dev`_
- [ ] [AI] **REFACTOR:** remove any response construction duplicated between the two controllers and
      confirm each still maps to its contract schema. Rerun
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run ose-lms-be:test:quick`;
      acceptance: exit code 0 including the 99% coverage floor.
  - _Suggested executor: `swe-java-dev`_
- **Proof:** a passing `ose-lms-be:test:unit` and a `test:coverage:unit` run reporting every
  scenario resolved exactly once.

### AC-ACT-01 and AC-ACT-02 — Actuator exposes health and nothing else

- **Input:** AC-ACT-01, AC-ACT-02, and decision D-8.
- **Outcome:** `/actuator/health` reports `UP`; a non-exposed Actuator endpoint is unreachable.

- [ ] [AI] **RED:** add no new step bindings — both scenarios reuse the three expressions bound in
      the previous outcome. Run
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run ose-lms-be:test:unit`;
      acceptance: both Actuator scenarios fail because the dependency is absent.
  - _Suggested executor: `swe-java-dev`_
- [ ] [AI] **GREEN:** add `spring-boot-starter-actuator` to `build.gradle.kts` and set
      `management.endpoints.web.exposure.include: health` with
      `management.endpoint.health.show-details: never` in
      `src/main/resources/application.yaml`. Rerun the unit target; acceptance: AC-ACT-01 passes.
      For AC-ACT-02, observe the status the framework actually returns for the unexposed endpoint
      and, if it is not `404`, update the Gherkin in `prd.md` and the feature file to the observed
      value — the specification follows the framework's real behaviour, never the reverse.
  - _Suggested executor: `swe-java-dev`_
- [ ] [AI] **REFACTOR:** confirm no Actuator endpoint beyond health is exposed by asserting the
      configuration rather than by enumerating endpoints. Rerun
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run ose-lms-be:test:quick`;
      acceptance: exit code 0.
  - _Suggested executor: `swe-java-dev`_
- **Proof:** a passing `ose-lms-be:test:unit` covering all four HTTP scenarios.

### Manual API Verification (curl) — DU3

- [ ] [AI] Start the service:
      `rtk ./hippo run --class service --disk-path . -- npm exec nx -- run ose-lms-be:dev`
- [ ] [AI] Verify the health endpoint: `rtk curl -s -i http://localhost:8303/api/v1/health` — paste
      the status line and body inline in this checklist
- [ ] [AI] Verify the hello endpoint: `rtk curl -s -i http://localhost:8303/api/v1/hello` — paste
      the status line and body inline
- [ ] [AI] Verify the Actuator health endpoint: `rtk curl -s -i http://localhost:8303/actuator/health`
      — paste the status line and body inline
- [ ] [AI] Verify a non-exposed Actuator endpoint: `rtk curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8303/actuator/env`
      — paste the status code inline and confirm it matches AC-ACT-02
- [ ] [AI] Verify the port override: stop the service, restart with
      `OSE_LMS_BE_PORT=8399 rtk ./hippo run --class service --disk-path . -- npm exec nx -- run ose-lms-be:dev`,
      and confirm `rtk curl -s http://localhost:8399/api/v1/health` succeeds while port 8303 refuses
- [ ] [AI] Verify malformed-value handling: restart with `OSE_LMS_BE_PORT=not-a-port` and confirm
      the process exits with a startup error rather than binding a fallback port — paste the error
      inline
- [ ] [AI] Test error cases: `rtk curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8303/api/v1/nonexistent`
      and a `POST` to `/api/v1/health` — paste both status codes inline
- [ ] [AI] Save any response longer than 20 lines to `evidence/du3-curl-<endpoint>.txt` rather than
      inlining it
- [ ] [AI] Locale coverage is not applicable: the service returns no localized content and declares
      no locale set. Record that explicitly rather than omitting the check

### Local Quality Gates, Commits, and Post-Push — DU3

- [ ] [AI] Run affected typecheck:
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- affected -t typecheck`
- [ ] [AI] Run affected linting: `rtk npm run affected:lint`
- [ ] [AI] Run affected quick tests: `rtk npm run affected:test`
- [ ] [AI] Run affected spec coverage:
      `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- affected -t test:coverage:behaviour`
- [ ] [AI] Fix ALL failures found — including preexisting issues not caused by these changes
- [ ] [AI] Do not stage or commit until the user explicitly authorizes the named change set
- [ ] [AI] Expected commit shape: `feat(ose-lms-be): scaffold the LMS backend with health and hello`
- [ ] [AI] Keep the contract, its generated-output gitignore entry, the service, its tests, and the
      specs corpus in the same commit set; never commit generated output
- [ ] [AI] `rtk git switch -c lms-init/du3-contract-and-service` then
      `rtk git push -u origin lms-init/du3-contract-and-service`
- [ ] [AI] Open a draft pull request against `main`; the body states the new-code cost and benefit
- [ ] [AI] Poll CI every 2 minutes with `rtk gh pr checks <number>`. Never use `gh run watch`
- [ ] [AI] Confirm the `Java quality gate` job now **runs** and passes — the first proof that
      AC-CI-01 detection works on a real Java project
- [ ] [AI] Confirm the `TypeScript quality gate`, `.NET quality gate`, and `Flutter quality gate`
      jobs do not execute any `ose-lms-be` target; record the job logs proving the exclusion in
      `evidence/du3-ci-routing.txt`
- [ ] [AI] Verify exact-current-head/base `Quality gate` and one clean current-head
      `pr-leak-review`
- [ ] [AI] If any check fails, fix at the root cause and push a follow-up commit; never bypass
- [ ] [AI] Mark ready, merge, and record the pull request number and 40-character head SHA

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [ ] [AI] `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run ose-lms-be:test:quick`
      exits 0, including the 99% JaCoCo line floor
- [ ] [AI] `ose-lms-be:test:coverage:behaviour` reports every scenario resolved exactly once in the
      Unit adapter, with the three `@e2e-exempt` scenarios recognized
- [ ] [AI] Every curl assertion above is recorded with a real status and body
- [ ] [AI] `evidence/du3-ci-routing.txt` proves the Java job ran and the other three did not touch
      `ose-lms-be`
- [ ] [AI] `rtk git status --short` shows no generated contract or build output tracked

> **Pause Safety**: `ose-lms-be` builds, serves both endpoints, and proves every scenario in the
> Unit adapter — the one adapter with no exemption, so every scenario is genuinely proven. The E2E
> adapter is neither declared nor referenced yet, so nothing dangles. `main` is deployable. Safe to
> stop. To resume:
> `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run ose-lms-be:test:quick`.

---

## Phase 4 (DU4): E2E Project and Reconciliation

One pull request in `ose-public`.

### AC-HEALTH-01, AC-HELLO-01, AC-ACT-01, AC-ACT-02 — E2E adapter

- **Input:** the four HTTP-observable scenarios and `apps/ose-be-e2e/` as the structural model.
- **Outcome:** each of the four scenarios resolves in the E2E adapter against a really-started
  service over real HTTP.

- [ ] [AI] **RED:** create `apps/ose-lms-be-e2e/` with `project.json` (tags
      `["type:e2e", "platform:playwright", "lang:ts", "domain:ose"]`, targets `test:e2e`, `lint`,
      `typecheck`, `test:quick`, `test:coverage:e2e`, `test:coverage:behaviour`, `test:coverage`,
      and `namedInputs.specs`; **no** `test:unit`), `package.json`, `tsconfig.json`,
      `playwright.config.ts`, `behaviour-coverage.json`, `e2e-coverage-baseline.json`, `.gitignore`,
      and `README.md`, all modelled on the `ose-be-e2e` sibling. Add `steps/http.steps.ts` binding
      the same four step expressions the Unit adapter binds, and `utils/response-store.ts`. Run
      `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- run ose-lms-be-e2e:test:coverage:behaviour`;
      acceptance: it fails on the missing `steps/backend-process.ts` starter.
  - _Suggested executor: `swe-e2e-dev`_
- [ ] [AI] **GREEN:** create `steps/backend-process.ts` starting the Gradle-built jar on a test port
      and stopping it on teardown, modelled on `apps/ose-be-e2e/steps/backend-process.ts`. Run
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run ose-lms-be-e2e:test:e2e`;
      acceptance: all four scenarios pass against real HTTP.
  - _Suggested executor: `swe-e2e-dev`_
- [ ] [AI] **REFACTOR:** confirm the three `@e2e-exempt` port-resolution scenarios are skipped by the
      E2E adapter and that no E2E binding is left unused. Run
      `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- run ose-lms-be-e2e:test:quick`;
      acceptance: exit code 0 with no unused-binding error.
  - _Suggested executor: `swe-e2e-dev`_
- [ ] [AI] Add the `e2e` adapter to `apps/ose-lms-be/behaviour-coverage.json` (bindings
      `["../ose-lms-be-e2e/steps"]`, driver `../ose-lms-be-e2e/playwright.config.ts`), add the
      `test:coverage:e2e` target to `apps/ose-lms-be/project.json`, and wire it into that project's
      aggregate `test:coverage` — all three deliberately deferred from Phase 3. Run
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run ose-lms-be:test:quick`;
      acceptance: exit code 0 with the E2E static validator now reached through the aggregate.
- **Proof:** passing `ose-lms-be-e2e:test:e2e` and `ose-lms-be:test:quick` with all four static
  validators reached.

### Registry and Index Reconciliation

- [ ] [AI] Add `ose-lms-be` and `ose-lms-be-e2e` to the Current Apps list in
      `docs/reference/monorepo-structure.md`, each with a one-line description and the port.
      Acceptance: `rtk npm run lint:md` exits 0.
  - _Suggested executor: `docs-maker`_
- [ ] [AI] Verify `docs/reference/web-sites.md` still carries the DU2 rows and that port 8303 is
      claimed by exactly one app: `rtk grep -n "8303" docs/reference/web-sites.md`.
- [ ] [AI] Reconcile every README index the plan touched — `specs/apps/ose/README.md`,
      `specs/apps/ose/lms-be/README.md`, each `behaviours/*/README.md` scenario count, and
      `apps/README.md`. Acceptance: the structure validator reports no `count` or `links` finding,
      and `governance-readme-completeness` reports no `missing` or `unannotated` finding.
- [ ] [AI] Reconcile the file ledger with reality: run `rtk git status --short` and confirm every
      changed path appears in `tech-docs.md` §5, and every `[N]` entry in that tree that was
      intended for this plan now exists. Record any divergence in `learnings.md` rather than
      silently editing the tree.

### Rule-16 API Exploratory Retest

Applicable: this plan changes an API surface. Rule 15 (the three-tester web triad) is **not
applicable** — no web UI, no browser surface, no locales.

- [ ] [AI] Start the service:
      `rtk ./hippo run --class service --disk-path . -- npm exec nx -- run ose-lms-be:dev`
- [ ] [AI] Run `api-exploratory-tester` with `output-mode: delivery` and
      `plan-path: plans/in-progress/lms-init/`, against `http://localhost:8303`, with
      `specs/apps/ose/lms-be/contracts/openapi.yaml` as the contract ground truth
- [ ] [AI] Append every finding to this checklist as a new unchecked checkbox, source-attributed
      `AET-###`
- [ ] [AI] Fix every `AET-###` defect finding during this phase. Deferral requires explicit user
      permission and only when genuinely impossible
- [ ] [AI] Triage each `SG-###` spec-gap proposal: either fix it in the contract or record the
      explicit reason it is out of scope

### Local Quality Gates, Commits, and Post-Push — DU4

- [ ] [AI] Run affected typecheck:
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- affected -t typecheck`
- [ ] [AI] Run affected linting: `rtk npm run affected:lint`
- [ ] [AI] Run affected quick tests: `rtk npm run affected:test`
- [ ] [AI] Run affected spec coverage:
      `rtk ./hippo run --class ephemeral --disk-path . -- npm exec nx -- affected -t test:coverage:behaviour`
- [ ] [AI] Run the E2E suite once explicitly:
      `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run ose-lms-be-e2e:test:e2e`
- [ ] [AI] Fix ALL failures found — including preexisting issues not caused by these changes
- [ ] [AI] Do not stage or commit until the user explicitly authorizes the named change set
- [ ] [AI] Expected commit shape: `test(ose-lms-be-e2e): prove the LMS backend over real HTTP`
- [ ] [AI] `rtk git switch -c lms-init/du4-e2e-and-reconciliation` then
      `rtk git push -u origin lms-init/du4-e2e-and-reconciliation`
- [ ] [AI] Open a draft pull request against `main`; the body states the new-code cost and benefit
- [ ] [AI] Poll CI every 2 minutes with `rtk gh pr checks <number>`. Never use `gh run watch`
- [ ] [AI] Verify exact-current-head/base `Quality gate` and one clean current-head
      `pr-leak-review`
- [ ] [AI] If any check fails, fix at the root cause and push a follow-up commit; never bypass
- [ ] [AI] Mark ready, merge, and record the pull request number and 40-character head SHA

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [ ] [AI] `rtk ./hippo run --class transactional --disk-path . -- npm exec nx -- run-many -t lint,test:quick --parallel=1`
      exits 0 across the whole workspace
- [ ] [AI] `ose-lms-be-e2e:test:e2e` passes all four HTTP scenarios
- [ ] [AI] Every `AET-###` defect finding is ticked, or carries recorded explicit user permission to
      defer
- [ ] [AI] Every README index and registry table the plan touched is reconciled
- [ ] [AI] `rtk git status --short` is clean apart from plan evidence

> **Pause Safety**: the LMS backend is complete for its declared scope — built, formatted, gated,
> proven in two adapters, and reachable over real HTTP. `main` is deployable. Safe to stop. To
> resume: re-run the workspace-wide command in the first gate check.

---

## Phase 5: Knowledge Capture

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only entries where a durable
      surface would catch this automatically next time; discard the rest with a one-line reason.
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize to
      `<placeholder>` tokens or discard if the entry cannot be sanitized without losing its meaning.
- [ ] [AI] Apply the **repo-relevance gate** to every surviving entry — infra-private content stays
      in `ose-private` only; public-governance content may route to `ose-public`; never cross-route
      private content into a public repo.
- [ ] [AI] Route each surviving entry to exactly one durable home. The rubric is open-ended — route
      to whichever surface owns that kind of knowledge (`repo-governance/`, `docs/`,
      `.claude/agents/`, `.claude/skills/`, a post-mortem, or any other durable home), landing a
      small non-code edit inline. Create or update a `plans/ideas/<slug>.md` two-pager only when the
      user has literally authorized that plan artifact; otherwise report the follow-up and record
      `Reported without plan authorization` with handoff evidence.
- [ ] [AI] For any entry routed to `plans/ideas/`, scan `plans/ideas/README.md` and the existing
      two-pagers FIRST after the user literally authorizes an idea artifact. Fold the learning into
      an authorized overlapping brief instead of creating a new file; only create a new authorized
      `plans/ideas/<slug>.md` when the scan confirms no existing brief overlaps.
- [ ] [AI] **Code-routing rule**: if a learning's home is `apps/`, `libs/`, or tests, NEVER land it
      inline in this plan's commits or pull requests. File a separate `plans/ideas/` two-pager only
      with literal plan-artifact authorization; never create a `plans/backlog/` folder directly
      because the promotion ripeness gate owns that transition. Otherwise use the reported terminal
      state. The sole carve-out is a bug, lint, or test failure that blocks THIS plan's own scope —
      that is fixed inline as ordinary Root Cause Orientation work, not routed as a deferred
      learning.
- [ ] [AI] Record the terminal state of every entry (routed inline / explicitly authorized two-pager
      at `<path>` / reported without plan authorization with handoff evidence / discarded with
      reason) directly in `learnings.md`.
- [ ] [AI] If execution genuinely surfaced no generalizable learning, record the explicit escape
      `No generalizable learnings — <one-line reason>` instead of individual entries.

### Phase 5 Gate

> All checks below must pass before starting Plan Archival.

- [ ] [AI] Verify every `learnings.md` entry has reached a terminal state (routed / authorized and
      filed / reported without plan authorization / discarded) or the explicit "none" escape is
      present — no entry left open.
- [ ] [AI] Verify no code-homed learning landed inline — every code-routed learning has a
      corresponding explicitly authorized `plans/ideas/` two-pager or a report with handoff
      evidence.

> **Pause Safety**: all learnings are routed, authorized and filed, reported without plan
> authorization, or explicitly discarded; nothing is left dangling in `learnings.md`. Safe to stop.
> To resume: re-check `learnings.md` for any entry without a terminal-state marker.

---

### Plan Archival

- [ ] [AI] Perform the **preliminary** plan-execution end-to-end delivery completeness audit: trace
      approved scope and every canonical PRD acceptance criterion through delivery units, as-built
      artifacts, automated and manual proof, applicable migration/rollout/rollback evidence,
      conditional recovery dispositions, and Knowledge Capture. Reopen execution at the earliest
      affected packet for every missing or unsupported non-delivery row; only final-delivery proof
      may remain explicitly pending. Checked boxes alone are not proof.
- [ ] [AI] Verify ALL delivery checklist items are ticked
- [ ] [AI] Verify ALL quality gates pass (local + CI)
- [ ] [AI] Verify ALL manual assertions pass with committed evidence in `evidence/` (curl output;
      no screenshots apply — this plan has no UI surface)
- [ ] [AI] Locale coverage in UI verification is not applicable — recorded, not skipped
- [ ] [AI] Rule-15 EWT/UWT/DWT findings are not applicable — this plan touches no web UI
- [ ] [AI] Verify every rule-16 AET defect finding is fixed (ticked) — deferral requires explicit
      user permission (only when genuinely impossible) for AET defect findings; `SG-###` spec-gap
      proposals may be triaged or deferred
- [ ] [AI] Register the workflow-owned terminal audit task and its required post-delivery proof
      fields; do not mark that gate complete before merge or direct-push confirmation. Its result
      belongs in the plan-execution final report, not a speculative pre-merge checkbox.
- [ ] [AI] Classify every `Delivery Branch Inventory` entry as delivered, unused, or
      retained/escalated; a retained entry names who owns it and why it outlives the plan, and an
      entry whose state is ambiguous or whose proof is missing is escalated, never deleted. Both
      repositories' entries are classified.
- [ ] [AI] Remove each worktree this plan provisioned, non-force, from each repository root:
      `rtk git worktree remove worktrees/lms-init`, after the checks in
      `repo-governance/development/workflow/worktree-and-artifact-cleanup/mandatory-pre-removal-checks.md`.
      Run this in `ose-private` first, then `ose-public` — the public worktree hosts this plan file
      and must be the last removed.
- [ ] [AI] Complete branch cleanup for every branch this plan created, in **both** repositories, per
      `repo-governance/development/workflow/worktree-and-artifact-cleanup/branch-cleanup.md`, then
      run `rtk git worktree prune` in each. Follow that convention's proof gates; never relax them
      here.
- [ ] [AI] After every pre-archival gate, including the preliminary audit, passes, run
      `rtk date +%F`; record the output as `<completion-date>`. Do not hardcode or predict this value
      while authoring the plan.
- [ ] [AI] Move the plan via
      `rtk git mv plans/in-progress/lms-init/ plans/done/<completion-date>__lms-init/` (the
      `evidence/` subfolder moves with it)
- [ ] [AI] Update `plans/in-progress/README.md` — remove the plan entry
- [ ] [AI] Update `plans/done/README.md` — add the plan entry using the same resolved completion date
- [ ] [AI] Update any other READMEs that reference this plan
- [ ] [AI] Commit: `chore(plans): move lms-init to done`

---

### Validation Checklist

- [ ] Every code outcome has separate detailed RED, GREEN, and REFACTOR checkboxes.
- [ ] All tests pass (`rtk npm run affected:test`, the existing guarded root alias).
- [ ] Code meets quality standards.
- [ ] Documentation and rules are reconciled.
- [ ] Acceptance criteria are verified.
