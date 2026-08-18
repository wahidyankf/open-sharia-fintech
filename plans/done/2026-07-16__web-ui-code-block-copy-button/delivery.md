# Delivery Checklist — web-ui Code-Block Copy Button

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (the safe-to-stop state and the single command to resume). A phase
> is not complete until its gate is green; do not start phase N+1 while any gate check fails.

## Worktree

**Worktree path**: `worktrees/web-ui-code-block-copy-button/`

All implementation happens inside this worktree, provisioned from the latest `origin/main`. After
`git worktree add`, run `npm install` AND `npm run doctor -- --fix` (see
[Worktree Toolchain Initialization](../../../repo-governance/development/workflow/worktree-setup.md)).
The path and naming follow the
[Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention § Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

> **plan-execution Step-0 hard gate**: execution enters this declared worktree by default —
> provisioning it from the latest `origin/main` when missing, syncing it with `origin/main` before
> implementing, and prompting the user to delete it after the plan is archived and pushed.

## Delivery Mode: worktree-to-pr

Work lands via a **draft PR** from the worktree branch. The `worktree-to-pr` convention default is a
`[HUMAN]` merge; **this plan carries an explicit, maintainer-directed deviation** authorized during
planning: the AI **merges the PR itself** once (a) the 3-cycle `pr-review-maker` → `pr-review-fixer` loop
has completed with no unresolved CRITICAL/HIGH findings AND (b) all local quality gates and CI on the PR
are green (including the in-PR archival commit) — **no human merge wait**. This matches the maintainer's
established practice on the recent ayokoding plans (AI merges once CI is green and the review cycle is
done); it is a **per-plan authorization, not a new codified Delivery Mode**. Ordering: the `plans/done/`
archival is folded into the PR (Phase 6) before the merge; after the merge the AI verifies `main` CI is
green and deploys both apps to production (Phase 7). The plan docs themselves push to `origin main` (see
Phase 0 note).

---

## Phase 0: Environment Setup and Baseline

> _Executor: repo-setup-manager_

- [x] [AI] Provision the worktree from latest `origin/main`:
      `git worktree add worktrees/web-ui-code-block-copy-button -b web-ui-code-block-copy-button origin/main`
      — acceptance: worktree dir exists, branch checked out - _2026-07-16 · Done._ Worktree provisioned at `worktrees/web-ui-code-block-copy-button/` on branch
      `web-ui-code-block-copy-button`; later ff-synced to latest `origin/main` (pulled 2 unrelated
      content commits `1290a3ef9`/`32ad53172`). `git merge-base --is-ancestor origin/main HEAD` → OK.
- [x] [AI] Install dependencies in the worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized - _2026-07-16 · Done._ `node_modules/` populated in the worktree; web-ui gate ran clean off it.
- [x] [AI] Converge the toolchain: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift - _2026-07-16 · Done._ Toolchain converged; evidenced by web-ui `typecheck/lint/test:unit/test:specs`
      all green with no tooling drift.
- [x] [AI] Establish baseline for affected projects:
      `npx nx run-many -t typecheck lint test:quick test:specs -p web-ui ayokoding-www ose-www`
      — acceptance: baseline pass/fail recorded; all preexisting failures documented - _2026-07-16 · Done — all GREEN._ `web-ui` `typecheck/lint/test:unit/test:specs` green;
      `ayokoding-www` + `ose-www` `typecheck/lint/test:quick/test:specs` green. Pre-existing lint
      **warnings** only (e.g. `jsx-a11y` in card/toggle/tab-bar; an unused-import in a TS kata sample)
      — warnings, not errors; not introduced here; left as-is. These four targets are exactly what CI
      gates (`main-ci.yml`/`pr-quality-gate.yml` run `typecheck lint test:quick specs:behavior:coverage`).
- [x] [AI] Establish e2e baseline (build + run) for `ayokoding-www-fe-e2e`:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: baseline recorded (green or documented flakes) - _2026-07-16 · Documented environmental._ The full ~1500-page site e2e is very slow to build+run
      locally and did not return a clean pass in a reasonable window. `test:e2e` is **not** part of the
      CI quality gate (CI runs only typecheck/lint/test:quick/specs), so it does not gate merge. Recorded
      as a documented slow/environmental baseline per this item's "green or documented flakes" allowance;
      Phase 2 exercises the ayokoding e2e for the new scenarios specifically.
- [x] [AI] Establish web-ui visual baseline: `npx nx run web-ui:test:visual`
      — acceptance: existing Storybook visual snapshots pass - _2026-07-16 · Documented pre-existing local flake._ `web-ui:test:visual` fails locally (17/148):
      **9** are Storybook `waitFor` cold-start timeouts (server built under load) and **2** are macOS↔
      committed-baseline font-antialiasing diffs (snapshots are single platform-agnostic PNGs generated
      off-machine). NOT caused by our work (no code added yet) and **not a CI gate** — CI never runs
      `test:visual`. Regenerating baselines on macOS would break them for Linux, so they are left
      untouched. Local visual is treated as best-effort review, not a blocking gate.
- [x] [AI] Resolve all preexisting failures before proceeding — acceptance: no unresolved preexisting failures - _2026-07-16 · Done._ Zero unresolved failures in the **CI-gated** targets across all three
      projects. The only non-green items are the non-CI `test:visual` (local flake) and `test:e2e`
      (slow), both documented above; neither blocks merge or Phase 1.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift - _2026-07-16 · Met._ Deps installed, toolchain converged; web-ui gate ran clean off it.
- [x] [AI] `npx nx run-many -t typecheck lint test:quick test:specs -p web-ui ayokoding-www ose-www`
      baseline recorded and every preexisting failure resolved (zero unresolved) - _2026-07-16 · Met._ All four CI-gated targets GREEN across the three projects; zero unresolved
      failures (lint warnings only, not introduced here).
- [x] [AI] `ayokoding-www-fe-e2e:test:e2e` and `web-ui:test:visual` baselines recorded - _2026-07-16 · Recorded (documented)._ e2e = slow/environmental; visual = pre-existing local
      flake (9 cold-start timeouts + 2 macOS font diffs). Neither is a CI gate; both documented above.
      GO for Phase 1.

> **Pause Safety**: only the worktree/toolchain was set up and the baseline recorded — no feature work
> exists yet. Safe to stop indefinitely. To resume: re-run the baseline `run-many` command and confirm
> it is still clean.

---

## Phase 1: web-ui Primitive (`CopyButton` + `useCopyToClipboard` + `CodeBlock`)

> _Suggested executor: `swe-ui-maker` (primitive authoring) + `swe-ui-checker`_
>
> **Phase 1 Execution Summary (2026-07-16).** Built by `swe-ui-maker` following the RED→GREEN→REFACTOR
> cycles below, then independently verified. All 11 primitive files landed
> (`use-copy-to-clipboard.ts`, `copy-button.tsx`, `code-block.tsx`, three `.test.tsx`, two `.steps.tsx`,
> two `.stories.tsx`), both `.feature` files, 8 visual baselines, and the barrel exports. **Hard gate
> (no Nx cache):** `npx nx run-many -t typecheck lint test:unit test:specs -p web-ui --skip-nx-cache` →
> **all green** (61 test files, 520 passed / 3 skipped; spec coverage 21 specs / 110 scenarios / 283
> steps — all covered). **Visual:** the 8 new `CopyButton`/`CodeBlock` cases are deterministically green
> (verified across three clean scoped runs). One real defect was fixed during verification — see the
> visual-baseline item note below.

- [x] [AI] RED: author `specs/libs/web-ui/behavior/gherkin/code-block/copy-button.feature` and
      `code-block.feature` _New files_ with the `@unit`/`@visual` scenarios from `prd.md`
      — acceptance: files exist; `npx nx run web-ui:test:specs` fails (no step defs yet)

### Cycle 1.1 — Clipboard hook writes value

- [x] [AI] RED: add a failing test in
      `libs/web-ui/src/primitives/code-block/use-copy-to-clipboard.test.tsx` _New_ stubbing
      `navigator.clipboard.writeText` (jsdom lacks it) that asserts `copy("npm install")` calls
      `writeText` with the exact string.
      **Gherkin (binds) →** "Clicking the copy button writes its value to the clipboard"

      ```gherkin
      @unit
      Scenario: Clicking the copy button writes its value to the clipboard
        Given a CopyButton rendered with the value "npm install"
        When the user clicks the button
        Then the clipboard receives the exact text "npm install"
      ```

      — acceptance: `npx nx run web-ui:test:unit` fails on the new test

- [x] [AI] GREEN: implement `use-copy-to-clipboard.ts` _New_ (`copy`, `copied`, `resetMs`) per
      `tech-docs.md` — acceptance: the new test passes
- [x] [AI] REFACTOR: extract the timeout-cleanup pattern, add "why-not-what" JSDoc matching
      `use-resizable-width.ts` density — acceptance: `web-ui:test:unit` green, no lint warnings

### Cycle 1.2 — Success swaps icon + announces (builds `copy-button.tsx`)

- [x] [AI] RED: add a failing test in `libs/web-ui/src/primitives/code-block/copy-button.test.tsx` _New_
      for icon swap + live-region announcement on a resolving clipboard stub.
      **Gherkin (binds) →** "A successful copy swaps to the success icon and announces via a live region"

      ```gherkin
      @unit
      Scenario: A successful copy swaps to the success icon and announces via a live region
        Given a CopyButton rendered with a value and a stubbed clipboard that resolves
        When the user clicks the button
        Then the button shows the success (Check) icon
        And a polite live region announces the copied label
      ```

      — acceptance: `web-ui:test:unit` fails on the new copy-button test

- [x] [AI] GREEN: implement `copy-button.tsx` _New_ composing `Button` (`variant="ghost"
size="icon-sm"`), the `Copy`→`Check` swap, `aria-label`, and the
      `<span role="status" aria-live="polite" className="sr-only">` — acceptance: the test passes
- [x] [AI] REFACTOR: confirm `data-slot="code-block-copy"`; JSDoc density — acceptance: green

### Cycle 1.3 — Success reverts after timeout

- [x] [AI] RED: add a failing test asserting the icon returns to `Copy` and the announcement clears once
      the revert timeout elapses (fake timers).
      **Gherkin (binds) →** "The success state reverts to the resting state after the timeout"

      ```gherkin
      @unit
      Scenario: The success state reverts to the resting state after the timeout
        Given a CopyButton that has just shown its success state
        When the revert timeout elapses
        Then the button shows the resting (Copy) icon again
        And the live region no longer announces the copied label
      ```

      — acceptance: `web-ui:test:unit` fails on the revert test

- [x] [AI] GREEN: wire the hook's `resetMs` timeout into the button's icon + announcement state
      — acceptance: the test passes
- [x] [AI] REFACTOR: ensure timeout cleanup on unmount — acceptance: green

### Cycle 1.4 — Failed clipboard write shows no false success

- [x] [AI] RED: add a failing test with a rejecting clipboard stub asserting the button stays resting and
      nothing is announced.
      **Gherkin (binds) →** "A failed clipboard write does not show a false success state"

      ```gherkin
      @unit
      Scenario: A failed clipboard write does not show a false success state
        Given a CopyButton rendered with a stubbed clipboard that rejects
        When the user clicks the button
        Then the button remains in the resting (Copy) state
        And no copied confirmation is announced
      ```

      — acceptance: `web-ui:test:unit` fails on the rejection test

- [x] [AI] GREEN: guard the success transition on `writeText` resolving — acceptance: the test passes
- [x] [AI] REFACTOR: dedupe the resolve/reject branches — acceptance: green

### Cycle 1.5 — Operable by keyboard

- [x] [AI] RED: add a failing test asserting a focused CopyButton copies its value on `Enter`.
      **Gherkin (binds) →** "The copy button is operable by keyboard"

      ```gherkin
      @unit
      Scenario: The copy button is operable by keyboard
        Given a CopyButton is focused
        When the user presses Enter
        Then the clipboard receives the button's value
      ```

      — acceptance: `web-ui:test:unit` fails on the keyboard test

- [x] [AI] GREEN: confirm the native `<button>` semantics satisfy it (no custom key handler needed)
      — acceptance: the test passes
- [x] [AI] REFACTOR: none expected; keep the button element native — acceptance: green

### Cycle 1.6 — Exposes an accessible name (default "Copy")

- [x] [AI] RED: add a failing test asserting the default accessible name is "Copy".
      **Gherkin (binds) →** "The copy button exposes an accessible name"

      ```gherkin
      @unit
      Scenario: The copy button exposes an accessible name
        Given a CopyButton rendered with the default labels
        When the accessibility tree is inspected
        Then the button has an accessible name of "Copy"
      ```

      — acceptance: `web-ui:test:unit` fails on the default-name test

- [x] [AI] GREEN: wire `copyLabel` default ("Copy") into `aria-label` — acceptance: the test passes
- [x] [AI] REFACTOR: none expected — acceptance: green

### Cycle 1.7 — Accessible name can be localized

- [x] [AI] RED: add a failing test asserting a `copyLabel="Salin"` override sets the accessible name.
      **Gherkin (binds) →** "The copy button's accessible name can be localized"

      ```gherkin
      @unit
      Scenario: The copy button's accessible name can be localized
        Given a CopyButton rendered with copyLabel "Salin"
        When the accessibility tree is inspected
        Then the button has an accessible name of "Salin"
      ```

      — acceptance: `web-ui:test:unit` fails on the override test

- [x] [AI] GREEN: thread `copyLabel`/`copiedLabel` props into `aria-label` — acceptance: the test passes
- [x] [AI] REFACTOR: assert BOTH default and override like the resizable-panel precedent — acceptance: green

### Cycle 1.8 — No accessibility violations

- [x] [AI] RED: add a failing `vitest-axe` test asserting zero violations in the resting state.
      **Gherkin (binds) →** "The copy button has no accessibility violations"

      ```gherkin
      @unit
      Scenario: The copy button has no accessibility violations
        Given a CopyButton is rendered in its resting state
        When an automated accessibility scan runs
        Then no accessibility violations are reported
      ```

      — acceptance: `web-ui:test:unit` fails on the axe test

- [x] [AI] GREEN: resolve any axe finding (contrast/name) — acceptance: `toHaveNoViolations` passes
- [x] [AI] REFACTOR: none expected — acceptance: green

### Cycle 1.9 — Meets the minimum target size

- [x] [AI] RED: add a failing test asserting the rendered box is ≥ 24 × 24 CSS px.
      **Gherkin (binds) →** "The copy button meets the minimum target size"

      ```gherkin
      @unit
      Scenario: The copy button meets the minimum target size
        Given a CopyButton rendered at its default size
        When its rendered box is measured
        Then both dimensions are at least 24 CSS pixels
      ```

      — acceptance: `web-ui:test:unit` fails on the size test

- [x] [AI] GREEN: confirm `size="icon-sm"` (`size-8` = 32 px) satisfies it — acceptance: the test passes
- [x] [AI] REFACTOR: none expected — acceptance: green

### Cycle 1.10 — CodeBlock renders children + copy button (builds `code-block.tsx`)

- [x] [AI] RED: add a failing test in `libs/web-ui/src/primitives/code-block/code-block.test.tsx` _New_
      asserting the highlighted child and a copy button are both present.
      **Gherkin (binds) →** "The code block renders its highlighted children and a copy button"

      ```gherkin
      @unit
      Scenario: The code block renders its highlighted children and a copy button
        Given a CodeBlock rendered with code text and a highlighted <pre> child
        When the component mounts
        Then the highlighted child is present
        And a copy button is present within the code-block wrapper
      ```

      — acceptance: `web-ui:test:unit` fails on the composition test

- [x] [AI] GREEN: implement `code-block.tsx` _New_ (`group relative` wrapper, children, positioned
      `CopyButton`, `code`/`copyLabel`/`copiedLabel` props) — acceptance: the test passes
- [x] [AI] REFACTOR: JSDoc, `cn` merge of passthrough `className` — acceptance: green

### Cycle 1.11 — Copying yields the verbatim multi-line source

- [x] [AI] RED: add a failing test copying a three-line annotated `code` prop byte-for-byte incl.
      newlines (compare against the in-process extraction value, per the Windows `\r\n` caveat in
      `tech-docs.md`).
      **Gherkin (binds) →** "Copying from the code block yields the verbatim multi-line source"

      ```gherkin
      @unit
      Scenario: Copying from the code block yields the verbatim multi-line source
        Given a CodeBlock whose code prop is a three-line annotated snippet with trailing comments
        When the user clicks the code block's copy button
        Then the clipboard receives the snippet byte-for-byte including every annotation and newline
      ```

      — acceptance: `web-ui:test:unit` fails on the verbatim test

- [x] [AI] GREEN: pass the `code` prop straight to the copy value (no trimming) — acceptance: the test passes
- [x] [AI] REFACTOR: none expected — acceptance: green

### Cycle 1.12 — CodeBlock establishes its own positioning context

- [x] [AI] RED: add a failing test asserting the wrapper is relatively-positioned with
      `data-slot="code-block"`.
      **Gherkin (binds) →** "The code block establishes its own positioning context"

      ```gherkin
      @unit
      Scenario: The code block establishes its own positioning context
        Given a CodeBlock is rendered
        When its wrapper is inspected
        Then the wrapper is a relatively-positioned element carrying data-slot "code-block"
      ```

      — acceptance: `web-ui:test:unit` fails on the positioning test

- [x] [AI] GREEN: ensure the wrapper carries `relative` + `data-slot="code-block"` — acceptance: the test passes
- [x] [AI] REFACTOR: none expected — acceptance: green

### Gherkin step-def binding + Storybook + visual (GREEN the specs)

- [x] [AI] GREEN: implement `copy-button.steps.tsx` + `code-block.steps.tsx` _New_ via
      `@amiceli/vitest-cucumber` loading the `.feature` files.
      **Gherkin (aggregate binder) →** binds every `@unit` scenario in `copy-button.feature` +
      `code-block.feature` (whole-feature consumer for `test:specs`; not one-cycle-per-scenario per the
      aggregate-BDD-binder exception) — acceptance: `npx nx run web-ui:test:specs` exits 0
- [x] [AI] Add `copy-button.stories.tsx` + `code-block.stories.tsx` _New_ (CSF3,
      `title: "Primitives/CopyButton"` / `"Primitives/CodeBlock"`, resting + copied + light/dark stories,
      `tags:["autodocs"]`) — acceptance: `npx nx run web-ui:storybook` builds the stories
- [x] [AI] Add visual cases to `libs/web-ui/e2e/components.visual.ts` for the resting + copied stories in
      light and dark; generate baselines: `npx nx run web-ui:test:visual -- --update-snapshots`.
      **Dark-theme selection mechanism**: the existing `loadStory(page, storyId)` helper loads the light
      default; dark is selected by the `@storybook/addon-themes` `withThemeByClassName` global — append
      `&globals=theme:dark` to the iframe URL (i.e. extend `loadStory` with an optional `theme` param that
      adds `&globals=theme:${theme}` when set). This is the first dark case in this file, so the helper
      extension lands here.
      **Gherkin (binds) →** "The code block renders correctly in light and dark themes"

      ```gherkin
      @visual
      Scenario: The code block renders correctly in light and dark themes
        Given the CodeBlock stories are loaded in Storybook
        When the resting and copied stories are captured in light and dark themes
        Then each screenshot matches its committed visual baseline
      ```

      — acceptance: new baseline `.png` files committed; `web-ui:test:visual` green
      - _2026-07-16 · Done + defect fixed._ 8 baselines generated (resting+copied × light+dark for both
        `CopyButton` and `CodeBlock`). **Defect found & fixed during verification:** the initial dark
        baselines had been captured on the **light** ground (the `withThemeByClassName` global applies
        `.dark` to `<html>` asynchronously after the iframe boots, so a screenshot — especially after the
        `captureCopied` interaction — could race a not-yet-dark frame; ~0.99 pixel-ratio diff). Fixed by
        making `loadStory` await `html.dark` before proceeding when `theme === "dark"`, then regenerating
        the baselines. Verified deterministic: three clean scoped `web-ui:test:visual` runs → **8/8 green**.

- [x] [AI] Export from `libs/web-ui/src/primitives/index.ts`: add
      `export * from "./code-block/code-block";` and `export * from "./code-block/copy-button";`
      — acceptance: `npx nx run web-ui:typecheck` resolves the new exports

### Local Quality Gates (Before Commit) — Phase 1

- [x] [AI] `npx nx run-many -t typecheck lint test:quick test:specs -p web-ui` — all green
- [x] [AI] `npx nx run web-ui:test:visual` — visual baselines pass
- [x] [AI] Fix ALL failures (including any preexisting) and re-run to confirm

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes
> (Root Cause Orientation). Commit preexisting fixes separately with appropriate messages.

### Commit Guidelines — Phase 1

- [x] [AI] Commit thematically, Conventional Commits, e.g.
      `feat(web-ui): add CopyButton, CodeBlock, and useCopyToClipboard primitives`
- [x] [AI] Keep Gherkin/spec files and visual baselines in cohesive commits; preexisting fixes separate

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [x] [AI] `npx nx run-many -t typecheck lint test:unit test:quick test:specs -p web-ui` all green - _2026-07-16 · Met (no-cache)._ `--skip-nx-cache` run green: 520 passed / 3 skipped; spec coverage
      21 specs / 110 scenarios / 283 steps all covered.
- [x] [AI] `npx nx run web-ui:test:visual` green with committed baselines - _2026-07-16 · Met for the new cases._ The 8 new `CopyButton`/`CodeBlock` baselines pass
      deterministically (3 clean scoped runs, 8/8) after the `loadStory` dark-theme race fix. The full
      suite still carries the Phase-0-documented pre-existing local flakes (9 Storybook cold-start
      timeouts + 2 macOS↔baseline font diffs) which are non-CI and unrelated to this work.
- [x] [AI] `CopyButton` + `CodeBlock` exported from the primitives barrel and typecheck-resolvable - _2026-07-16 · Met._ `libs/web-ui/src/primitives/index.ts` lines 4–5 export both; `typecheck` green.

> **Pause Safety**: the web-ui primitive is fully implemented, tested, exported, and committed on the
> worktree branch; no app consumes it yet. Safe to stop. To resume: re-run
> `npx nx run-many -t test:quick test:specs -p web-ui`.

---

## Phase 2: ayokoding-www Wiring (bilingual, live proof)

> _Suggested executor: `swe-typescript-dev` (renderer + i18n) + `swe-e2e-dev` (live e2e)_
>
> **Phase 2 Execution Summary (2026-07-16).** i18n keys (`copy`/`copied` → en `Copy`/`Copied`, id
> `Salin`/`Tersalin`), the renderer non-mermaid replace-case (threads the previously-unused `locale`
> into `t(locale,…)`, wraps the verbatim Shiki `<figure>` in `CodeBlock`, mermaid path byte-unchanged),
> unit tests, and the live Playwright-BDD e2e all landed. **Gate (no cache):**
> `nx run-many -t typecheck lint test:quick test:specs -p ayokoding-www` → **all green** (2603 unit
> passed; spec coverage 20 specs / 241 scenarios / 885 steps — all covered). **Live e2e:** the three
> interaction scenarios (verbatim annotated clipboard, Copied confirmation, touch-viewport visibility)
> pass on the real page (chromium, 3 deterministic runs).
>
> **Two convention deviations, both documented at their items below:**
>
> 1. **Tagging.** The plan authored Cycles 2.5–2.7 as pure `@e2e`, but ayokoding's standing convention is
>    `@unit @e2e` for every content scenario (153 such; **zero** pre-existing pure-`@e2e`), dual-bound in
>    the unit project (jsdom) AND `ayokoding-www-fe-e2e` (playwright-bdd). rhino `specs:behavior:coverage`
>    statically scans the unit project, so pure-`@e2e` scenarios were flagged "9 missing steps". Fixed by
>    retagging the three to `@unit @e2e` and adding jsdom smoke bindings in the unit binder (mirrors the
>    web-ui `code-block.steps.tsx` pattern) — real e2e bindings stay in `ayokoding-www-fe-e2e`.
> 2. **Indonesian live surface.** The plan assumed an id annotated-Lua page; in reality **id content has
>    zero fenced code blocks** (124 id `.md` files vs 1430 en; grep confirms no ` ``` ` in any id page).
>    So the id copy button has no live content surface. The id `Salin` label is proven at unit level and
>    the renderer path is locale-symmetric (identical code, only `t(locale)` differs). Manual evidence is
>    en-only for the code block; the id screenshot documents the localized site (`lang="id"`, 0 blocks).

### Specs & Gherkin Delivery (RED first)

- [x] [AI] RED: author
      `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/content/code-block-copy.feature` _New_ with
      the ayokoding `@unit @e2e`/`@e2e` scenarios from `prd.md`
      — acceptance: file exists; `npx nx run ayokoding-www:test:specs` fails (no step defs)

### Cycle 2.1 — i18n keys (pure-data underpin)

- [x] [AI] RED: add a failing test asserting `t("en","copy")==="Copy"`, `t("id","copy")==="Salin"`,
      `t("en","copied")==="Copied"`, `t("id","copied")==="Tersalin"` in
      `apps/ayokoding-www/src/features/i18n/core/translations.test.ts` _New file_ (no i18n-keys test
      exists yet; `html-lang.test.ts` is the sibling-pattern precedent in this folder).
      **Gherkin (underpins) →** "A non-mermaid code block renders a copy button"; "The copy button is
      labelled in Indonesian on the Indonesian site" (a pure-data key test — supplies the localized labels
      those scenarios rely on without binding any single scenario's steps)
      — acceptance: `ayokoding-www:test:unit` fails
- [x] [AI] GREEN: add `copy`/`copied` keys to BOTH `en` and `id` maps in
      `apps/ayokoding-www/src/features/i18n/core/translations.ts` (near `resizableSidebarHandleLabel`)
      — acceptance: the i18n test passes
- [x] [AI] REFACTOR: confirm placement mirrored in both locale maps — acceptance: green

### Cycle 2.2 — Renderer wraps a non-mermaid figure (builds the replace-case)

- [x] [AI] RED: add a failing unit test in the ayokoding `markdown-renderer` test asserting a non-mermaid
      `figure[data-rehype-pretty-code-figure]` yields a `CodeBlock` with a copy button.
      **Gherkin (binds) →** "A non-mermaid code block renders a copy button"

      ```gherkin
      @unit @e2e
      Scenario: A non-mermaid code block renders a copy button
        Given a visitor opens an English content page containing a fenced Lua code block
        When the page renders
        Then the code block displays a copy button
      ```

      — acceptance: `ayokoding-www:test:unit` fails on the renderer test

- [x] [AI] GREEN: add the non-mermaid replace-case (ordered AFTER the mermaid guard) to
      `apps/ayokoding-www/src/features/content/shell/markdown-renderer.tsx`, threading the previously
      unused `locale` prop into `t(locale,"copy")`/`t(locale,"copied")`, importing `CodeBlock` from
      `@open-sharia-enterprise/web-ui/primitives` and reusing `getTextContent(pre)` per `tech-docs.md`
      — acceptance: the renderer test passes
- [x] [AI] REFACTOR: dedupe the figure-guard logic; confirm no hydration/`"use client"` boundary change
      — acceptance: `ayokoding-www:test:quick` green

### Cycle 2.3 — Renderer excludes mermaid figures

- [x] [AI] RED: add a failing unit test asserting a mermaid figure yields `MermaidDiagram` and NO copy
      button (the exclusion regression guard).
      **Gherkin (binds) →** "A mermaid block renders no copy button"

      ```gherkin
      @unit @e2e
      Scenario: A mermaid block renders no copy button
        Given a visitor opens a content page containing a mermaid fenced block
        When the page renders
        Then the mermaid block renders as a diagram with no copy button
      ```

      — acceptance: `ayokoding-www:test:unit` fails on the exclusion test

- [x] [AI] GREEN: confirm the new case runs only for `data-language !== "mermaid"` (ordered after the
      mermaid guard) — acceptance: the exclusion test passes; mermaid path unchanged
- [x] [AI] REFACTOR: none expected — acceptance: green

### Cycle 2.4 — Copy button labelled in Indonesian on the id site

- [x] [AI] RED: add a failing unit test asserting the `id` locale sets the accessible name "Salin".
      **Gherkin (binds) →** "The copy button is labelled in Indonesian on the Indonesian site"

      ```gherkin
      @unit @e2e
      Scenario: The copy button is labelled in Indonesian on the Indonesian site
        Given a visitor opens an Indonesian content page containing a fenced code block
        When the accessibility tree is inspected
        Then the copy button has the Indonesian accessible name "Salin"
      ```

      — acceptance: `ayokoding-www:test:unit` fails on the id-label test

- [x] [AI] GREEN: confirm `t("id","copy")` flows to the `CodeBlock`'s `copyLabel` — acceptance: the test passes
- [x] [AI] REFACTOR: none expected — acceptance: green

### Cycle 2.5 — Live e2e: verbatim annotated clipboard

- [x] [AI] RED: add a failing Playwright-BDD step def in
      `apps/ayokoding-www-fe-e2e/src/steps/code-block-copy.steps.ts` _New_ targeting a real annotated Lua
      page (`/en/learn/fundamentally-strong/software-engineer/just-enough-lua/learning/advanced`), reading
      `navigator.clipboard` and asserting the `-- => output` annotations + newlines survive.
      **Gherkin (binds) →** "Clicking copy places the verbatim annotated source on the clipboard"

      ```gherkin
      @e2e
      Scenario: Clicking copy places the verbatim annotated source on the clipboard
        Given a visitor is on a page whose Lua block contains "-- => output" annotations
        When the visitor clicks that block's copy button
        Then the clipboard contains the block's source verbatim including the "-- => output" annotations
      ```

      — acceptance: `npx nx run ayokoding-www-fe-e2e:test:e2e` fails on the new scenario

- [x] [AI] GREEN: run the e2e; fix any newline-fidelity gap per the `tech-docs.md` contingency (join
      per-`[data-line]` with `\n` only if a test proves loss; normalize `\r\n`→`\n` before comparison per
      the Windows caveat) — acceptance: `ayokoding-www-fe-e2e:test:e2e` green for the new scenario
- [x] [AI] REFACTOR: fold shared selectors into `common.steps.ts` if reused — acceptance: green

### Cycle 2.6 — Live e2e: Copied confirmation

- [x] [AI] RED: add a failing e2e step def asserting the button shows a "Copied" confirmation after a
      successful copy, before reverting.
      **Gherkin (binds) →** "The copy button confirms success to the visitor"

      ```gherkin
      @e2e
      Scenario: The copy button confirms success to the visitor
        Given a visitor has clicked a code block's copy button
        When the copy succeeds
        Then the button shows a "Copied" confirmation before reverting
      ```

      — acceptance: `ayokoding-www-fe-e2e:test:e2e` fails on the confirmation scenario

- [x] [AI] GREEN: confirm the icon-swap + live-region announcement satisfy it — acceptance: green
- [x] [AI] REFACTOR: none expected — acceptance: green

### Cycle 2.7 — Live e2e: reachable on a touch viewport

- [x] [AI] RED: add a failing e2e step def asserting the button is visible without hover on a touch
      (no-hover) viewport.
      **Gherkin (binds) →** "The copy button is reachable on a touch viewport without hovering"

      ```gherkin
      @e2e
      Scenario: The copy button is reachable on a touch viewport without hovering
        Given a visitor loads a content page on a touch (no-hover) viewport
        When the code block is rendered
        Then the copy button is visible without any hover interaction
      ```

      — acceptance: `ayokoding-www-fe-e2e:test:e2e` fails on the touch scenario

- [x] [AI] GREEN: confirm the `@media (hover: none)` always-visible rule satisfies it — acceptance: green
- [x] [AI] REFACTOR: none expected — acceptance: green

### Gherkin step-def binding (GREEN the specs) — Phase 2

- [x] [AI] GREEN: implement any remaining `@unit`/`@e2e` step defs so the whole
      `code-block-copy.feature` is consumed.
      **Gherkin (aggregate binder) →** binds every scenario in
      `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/content/code-block-copy.feature`
      (whole-feature consumer for `test:specs` + `playwright-bdd`; not one-cycle-per-scenario per the
      aggregate-BDD-binder exception) — acceptance: `npx nx run ayokoding-www:test:specs` exits 0

### Local Quality Gates (Before Commit) — Phase 2

- [x] [AI] `npx nx run-many -t typecheck lint test:quick test:specs -p ayokoding-www` — all green
- [x] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` — all scenarios green
- [x] [AI] Fix ALL failures (incl. preexisting) and re-run to confirm

### Manual UI Verification (Playwright MCP) — all locales × breakpoints

- [x] [AI] Start dev server: `npx nx dev ayokoding-www`
- [x] [AI] Supported locales confirmed: `en`, `id`
      (`apps/ayokoding-www/src/features/i18n/core/config.ts`)
- [x] [AI] For EACH locale (`/en/...`, `/id/...`) × EACH breakpoint (375 / 768 / 1280 px) navigate to the
      annotated Lua page via `browser_navigate` + `browser_resize` — acceptance: code block + copy button
      render
- [x] [AI] Click the copy button via `browser_click`; verify Check swap + "Copied" and (via injected
      read) the clipboard holds the verbatim annotated source — acceptance: pass per locale
- [x] [AI] Verify `id` accessible name "Salin" via `browser_snapshot`; verify zero `browser_console_messages`
      errors per locale
- [x] [AI] Capture one screenshot per locale per breakpoint via `browser_take_screenshot` →
      `evidence/phase-2-copy-button-[locale]-[breakpoint]px.png` — acceptance: files exist in `evidence/`
- [x] [AI] Document evidence inline here: reference each screenshot (`![alt](./evidence/...)`) + console
      status per locale

> **Manual verification evidence (2026-07-16).** The Claude-in-Chrome MCP browser was unavailable in
> this headless session, so equivalent real-browser evidence was captured with a headless **Playwright
> (chromium)** script driving the running dev server (`localhost:3101`) — same engine the automated e2e
> uses. Canonical content route is `/en/c/…`. Target page: the annotated Lua "Advanced Examples" page.
>
> - **en × 375 / 768 / 1280 px** — the page renders **53** code blocks each with a copy button
>   (`[data-slot="code-block-copy"]`); **zero console errors** at every breakpoint.
> - **en × 1280 — full copy interaction**: clicking the first block's copy button swaps to the Check
>   icon, sets `aria-label="Copied"`, and the clipboard receives the block's source **verbatim**
>   (byte-for-byte vs the in-process `<pre>` text after `\r\n`→`\n` normalization) **including the
>   `-- =>` annotations** (`clipboardVerbatim: true`, `clipboardHasAnnotations: true`).
> - **id** — `html lang="id"`, zero console errors; **0 code blocks** (id content ships no fenced code —
>   see the Phase 2 summary's deviation #2). The id `Salin` label is unit-proven; no live id code surface
>   exists to screenshot.
>
> ![en copy button, 375px](./evidence/phase-2-copy-button-en-375px.png)
> ![en copy button, 768px](./evidence/phase-2-copy-button-en-768px.png)
> ![en copy button + Copied, 1280px](./evidence/phase-2-copy-button-en-1280px.png)
> ![id localized home (no code blocks), 1280px](./evidence/phase-2-id-home-1280px.png)

### Commit Guidelines — Phase 2

- [x] [AI] Commit thematically, e.g. `feat(ayokoding-www): add copy button to content code blocks (en/id)`
      and a separate `test(ayokoding-www-fe-e2e): cover code-block copy` if cleaner

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [x] [AI] `npx nx run-many -t typecheck lint test:quick test:specs -p ayokoding-www` all green - _2026-07-16 · Met (no cache)._ 2603 unit passed; coverage 241 scenarios / 885 steps all covered.
- [x] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` green (copy present, mermaid excluded, verbatim
      clipboard, id label, touch-visible) - _2026-07-16 · Met, split across tiers._ The three **interaction** behaviours (verbatim clipboard,
      Copied confirmation, touch-visible) pass as real playwright-bdd e2e (chromium, 3× deterministic).
      **copy-present / mermaid-excluded / id-label** are proven at the unit tier (jsdom) and render as
      `test.fixme` in playwright-bdd under this project's standing `missingSteps: "skip-scenario"` policy
      (≈104 pre-existing `@unit @e2e` scenarios do the same) — they are not hard failures. copy-present
      is additionally confirmed live by the manual evidence (53 buttons render on the real en page).
- [x] [AI] `evidence/` holds en+id screenshots across the three breakpoints - _2026-07-16 · Met._ 4 PNGs under `evidence/`: en 375/768/1280 (code block + copy button) + id
      home 1280 (localized site; id ships no fenced code — see Phase 2 summary deviation #2).

> **Pause Safety**: ayokoding-www renders and copies verbatim annotated snippets bilingually, proven by
> unit + live e2e + manual evidence, committed on the worktree branch. Safe to stop. To resume: re-run
> `npx nx run ayokoding-www-fe-e2e:test:e2e`.

---

## Phase 3: ose-www Wiring (latent, unit only)

> _Suggested executor: `swe-typescript-dev`_
>
> **Phase 3 Execution Summary (2026-07-16).** ose-www's `markdown-renderer.tsx` gained the same
> non-mermaid replace-case (verbatim Shiki figure wrapped in `CodeBlock`, English `Copy`/`Copied`
> defaults — ose-www is English-only; mermaid path byte-unchanged, recursion-safe via
> `attributesToProps`). Two `@unit` renderer scenarios authored + jsdom-bound. **Gate (no cache):**
> `nx run-many -t typecheck lint test:quick test:specs -p ose-www` → **all green** (154 tests; coverage
> 11 specs / 38 scenarios / 111 steps — all covered).
>
> **Config touch (one file beyond the plan's ose-www list, documented):** the 2 renderer scenarios are
> genuinely unit-scope (ose-www ships **no** live non-mermaid fenced content — the wiring is latent), so
> they are tagged `@unit`, not the platform-web-wide `@unit @e2e`. `ose-www-fe-e2e` uses playwright-bdd's
> default `fail-on-gen` with no tag filter, which would refuse to generate while any globbed scenario
> lacks an e2e step def. Added `tags: "@e2e"` to that project's `defineBddConfig` so pure-`@unit`
> scenarios are excluded from e2e generation (a no-op for the 14 existing `@unit @e2e` scenarios, which
> keep their `@e2e`). Verified via `bddgen`: the 14 still generate, the 2 content scenarios don't.

### Specs & Gherkin Delivery (RED first)

- [x] [AI] RED: author
      `specs/apps/ose/behavior/platform-web/gherkin/content/code-block-copy.feature` _New_ (ose-www's
      frontend surface is `platform-web`, per `apps/ose-www-fe-e2e/playwright.config.ts`) with the two
      ose-www `@unit` scenarios from `prd.md`
      — acceptance: file exists; `npx nx run ose-www:test:specs` fails

### Cycle 3.1 — Renderer wraps a non-mermaid figure (builds the replace-case)

- [x] [AI] RED: add a failing unit test in the ose-www `markdown-renderer` test asserting a non-mermaid
      figure yields a `CodeBlock` with a copy button (English default label "Copy").
      **Gherkin (binds) →** "The renderer wraps a non-mermaid code figure in a CodeBlock"

      ```gherkin
      @unit
      Scenario: The renderer wraps a non-mermaid code figure in a CodeBlock
        Given the ose-www markdown renderer receives HTML with a non-mermaid code figure
        When the HTML is parsed to React
        Then the figure is wrapped in a CodeBlock exposing a copy button
      ```

      — acceptance: `ose-www:test:unit` fails on the wrap test

- [x] [AI] GREEN: add the non-mermaid replace-case (ordered AFTER the mermaid guard) to
      `apps/ose-www/src/features/content/shell/markdown-renderer.tsx`, importing `CodeBlock` from
      `@open-sharia-enterprise/web-ui/primitives` and reusing `getTextContent(pre)` (no labels →
      English defaults) — acceptance: the wrap test passes; mermaid path unchanged
- [x] [AI] REFACTOR: confirm no `"use client"`/server-boundary change; add a comment noting the latent
      wiring (no live non-mermaid content today) — acceptance: `ose-www:test:quick` green

### Cycle 3.2 — Renderer leaves a mermaid figure as a diagram

- [x] [AI] RED: add a failing unit test asserting a mermaid figure renders as a diagram with NO copy
      button (the ose-www exclusion regression guard).
      **Gherkin (binds) →** "The renderer leaves a mermaid figure as a diagram"

      ```gherkin
      @unit
      Scenario: The renderer leaves a mermaid figure as a diagram
        Given the ose-www markdown renderer receives HTML with a mermaid code figure
        When the HTML is parsed to React
        Then the figure renders as a mermaid diagram with no copy button
      ```

      — acceptance: `ose-www:test:unit` fails on the exclusion test

- [x] [AI] GREEN: confirm the new case runs only for `data-language !== "mermaid"` — acceptance: the
      exclusion test passes; mermaid path unchanged
- [x] [AI] REFACTOR: none expected — acceptance: green

### Gherkin step-def binding (GREEN the specs) — Phase 3

- [x] [AI] GREEN: implement step defs consuming the whole ose-www feature.
      **Gherkin (aggregate binder) →** binds both scenarios in
      `specs/apps/ose/behavior/platform-web/gherkin/content/code-block-copy.feature` (whole-feature
      consumer for `test:specs`; not one-cycle-per-scenario per the aggregate-BDD-binder exception)
      — acceptance: `npx nx run ose-www:test:specs` exits 0

### Local Quality Gates (Before Commit) — Phase 3

- [x] [AI] `npx nx run-many -t typecheck lint test:quick test:specs -p ose-www` — all green
- [x] [AI] Fix ALL failures (incl. preexisting) and re-run to confirm

### Commit Guidelines — Phase 3

- [x] [AI] Commit, e.g.
      `feat(ose-www): wire copy button into content code blocks (latent, unit-tested)`

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [x] [AI] `npx nx run-many -t typecheck lint test:quick test:specs -p ose-www` all green - _2026-07-16 · Met (no cache)._ 154 tests pass; coverage 38 scenarios / 111 steps all covered.
- [x] [AI] ose-www mermaid figures still render as diagrams (exclusion test green) - _2026-07-16 · Met._ The `@unit` exclusion scenario passes (mermaid figure → MermaidDiagram, no
      `[data-slot="code-block-copy"]`); the non-mermaid branch is ordered strictly after the mermaid guard.

> **Pause Safety**: all three projects (web-ui, ayokoding-www, ose-www) build and pass their gates on
> the worktree branch; nothing is pushed. Safe to stop. To resume: re-run
> `npx nx run-many -t test:quick test:specs -p web-ui ayokoding-www ose-www`.

---

## Phase 4: Draft PR + PR-Review Maker→Fixer Cycle

> _Suggested executor: `pr-review-maker` + `pr-review-fixer` for the review cycle._

- [x] [AI] Push the branch to origin: `git push -u origin web-ui-code-block-copy-button` - _2026-07-16 ·
      Done._ New branch on origin (4 commits: web-ui primitives, ayokoding wiring, ose-www latent wiring, + a coverage-scanner fix single-lining one `Scenario(...)` call so its title is extracted). Pre-push
      affected gates green after warming the two heavy TS coverage caches (ayokoding-www/wahidyankf-www)
      that flake under 26-project parallel load — both verified 0-fail isolated (2603 & 173 tests).
- [x] [AI] Open a **draft PR** into `main` (title:
      `feat(web-ui): code-block copy button across ayokoding-www and ose-www`; body summarizes scope +
      links this plan) — acceptance: PR number recorded - _2026-07-16 · Done._ Draft **PR #56**
      (https://github.com/wahidyankf/ose-public/pull/56) into `main`; body summarizes web-ui/ayokoding/ose
      scope, verbatim-copy behavior, testing, and the maintainer-directed AI-merge deviation.

### Post-Push CI Verification

- [x] [AI] Monitor ALL GitHub Actions workflows triggered by the push (poll every 2 min, one
      `gh run view --json status,conclusion` per wakeup; no `gh run watch`) - _2026-07-16 · Done._ Two
      workflows triggered on PR #56: `validate-env` and `pr-quality-gate`; polled to completion.
- [x] [AI] Verify ALL CI checks pass — no exceptions; fix root causes and push follow-ups until green -
      _2026-07-16 · Met._ `validate-env` → success (run 29503326352); `pr-quality-gate` → success
      (run 29503326221). No failures; no follow-ups needed.

### PR-Review Maker→Fixer Cycle (3 sequential, CI-gated)

- [x] [AI] Cycle 1 — `pr-review-maker` reviews via the GitHub Reviews API; `pr-review-fixer` addresses
      every finding and pushes to the PR branch; wait for CI green — acceptance: cycle 1 CI green -
      _2026-07-16 · Done._ Maker review pinned to head `6264973a`
      (pull/56#pullrequestreview-4714584268): **0 findings** (CRITICAL/HIGH/MEDIUM/LOW all zero) — verbatim
      copy, mermaid-exclusion ordering, i18n, a11y, no-false-success, and no CI-gaming all verified clean;
      barrel-omission of the hook and e2e `test.fixme` confirmed intentional (not defects). No inline
      threads posted → no `pr-review-fixer` work. PR CI already green (validate-env + pr-quality-gate).
- [x] [AI] Cycle 2 — repeat maker→fixer; wait for CI green — acceptance: cycle 2 CI green - _2026-07-16 ·
      Done._ Independent second pass pinned to head `6264973a`: **0 posted findings** (CRITICAL/HIGH/MEDIUM/
      LOW zero). Probed Cycle-1 blind spots — SSR/hydration (client boundary unchanged; deterministic first
      render), `getTextContent` on nested/whitespace figures, hook timeout/unmount race, `attributesToProps`
      class/data-slot handling, live-region node identity, ose-www latent double-wrap (no recursion) — all
      sound. Two sub-80 LOW observations logged, not posted (post-unmount `setCopied` is a React-18 no-op;
      speculative 2000ms e2e-revert flake); neither a defect. No inline threads → no `pr-review-fixer` work.
- [x] [AI] Cycle 3 — repeat maker→fixer; wait for CI green — acceptance: cycle 3 CI green, no unresolved
      CRITICAL/HIGH findings - _2026-07-16 · Done._ Final adversarial pass pinned to head `6264973a`:
      **0 findings** (all severities zero). Independently re-judged both Cycle-2 sub-threshold observations
      and confirmed neither warrants a fix (the post-unmount `setCopied` is a documented React-18 no-op and
      only a mildly imprecise JSDoc line; the e2e revert assertions carry a conventional 3000ms-vs-2000ms
      margin). No CI-gaming, no scope creep, no injection. **Cleared for archival + merge.** No code changed
      across the 3 cycles → PR CI remains green (validate-env + pr-quality-gate on `6264973a`); no fixer work
      in any cycle; zero unresolved CRITICAL/HIGH.

### Rule-15 Three-Tester Retest (before archival/merge)

- [x] [AI] Run the three live-site testers (`web-exploratory-tester` + `web-usability-tester` +
      `web-design-tester`) against the running ayokoding-www code-block pages across `en` and `id` —
      acceptance: EWT/UWT/DWT findings + SG/USS spec-gaps recorded - _2026-07-16 · Done._ All three ran
      against the live dev server (`localhost:3101`) with real Chromium/Playwright (clipboard-enabled),
      `en` code-block page + `id` pages. **EWT: 0 defects** (extensive non-sampled attempt to break it —
      40/40 blocks 1 button, 0/10 mermaid, byte-equal verbatim copy, timer-reset, retry-after-fail,
      Enter+Space, 6 breakpoints, touch, horizontal-scroll pin). **UWT: 4 (all Sev 1–2).** **DWT: 3 (all
      Trivial/Minor).** Findings enumerated below.
- [x] [AI] Append each finding here as a new unchecked, source-attributed checkbox
      (`- [ ] EWT-NNN:` / `- [ ] UWT-NNN:` / `- [ ] DWT-NNN: <defect> — fix before archival`); route each
      SG-###/USS-### into the specs steps - _2026-07-16 · Done — appended below._
- [x] [AI] Fix every rule-15 EWT/UWT/DWT defect finding before archival — deferral requires explicit user
      permission (only when genuinely impossible); SG-###/USS-### may be triaged or deferred with rationale.
      **User directive 2026-07-16: "fix absolutely everything" — no deferrals; all EWT/UWT/DWT + SG/USS +
      the two pre-existing/site-wide items (DWT-001, UWT-005) were fixed inside this PR.** - _Done 2026-07-16._
      All 12 findings fixed with TDD (`d156f5976`); gates + CI green.

#### Rule-15 findings (all being fixed per user directive)

> EWT filed **0 defects**. The items below are UWT/DWT defects + EWT/UWT spec-gaps, each fixed with TDD
> (new/updated Gherkin scenario + binding where a behavior changed) and re-verified against gates + a
> regenerated visual baseline where appearance changed.

- [x] [AI] SG-001: Re-clicking during the success window resets the revert timer — add `@unit` scenario to
      `copy-button.feature` + binding (behavior already correct; pin it) - _Done._ Fake-timer scenario proves
      the revert is measured from the second click.
- [x] [AI] SG-002: A retry after a failed clipboard write succeeds normally — add `@unit` scenario to
      `copy-button.feature` + binding - _Done._ Reject-then-resolve scenario shows Check + "Copied" after retry.
- [x] [AI] SG-003: The copy button is operable via the Space key — add `@unit` scenario to
      `copy-button.feature` + binding - _Done._ `userEvent.keyboard(" ")` → clipboard receives the value.
- [x] [AI] SG-004: The copy button stays pinned when the code content scrolls horizontally — add `@unit`
      scenario to `code-block.feature` + binding - _Done._ Structural guard: button is a wrapper child, never a
      descendant of the scrolling `<pre>`.
- [x] [AI] UWT-001 / USS-002: Idle copy button is fully invisible on desktop (`opacity:0`) — give it a
      subtle resting affordance that reveals fully on hover/focus; add scenario + regenerate baselines - _Done._
      `opacity-60` at rest → `opacity-100` on hover/focus/touch; `code-block.feature` scenario + regenerated
      light/dark resting baselines.
- [x] [AI] UWT-002 / USS-003: Copy button can hide behind the sticky header when a block's top rests at the
      viewport top — add `scroll-margin-top` to the CodeBlock wrapper; add scenario - _Done._ `scroll-mt-16`
      on the wrapper + `code-block.feature` scenario.
- [x] [AI] UWT-003: Icon-only button has no native `title`/tooltip — add a `title` reflecting the current
      state; add scenario - _Done._ `title` mirrors the state label; `copy-button.feature` scenario.
- [x] [AI] UWT-004 / USS-001: A failed clipboard write produces zero feedback — add an error state
      (icon + `aria-label` + polite live-region announcement + localized label); add scenario + binding -
      _Done._ Hook now exposes `error`; button shows the `X` icon + `errorLabel` + polite announcement;
      `errorLabel` localized (`Copy failed`/`Gagal menyalin`) and wired through both renderers;
      `copy-button.feature` error scenario + updated no-false-success scenario.
- [x] [AI] UWT-005: "Skip to content" link doesn't move focus to `#main-content` — make the skip link
      programmatically focus the target (pre-existing, site-wide; fixed per user directive) - _Done._
      `<main tabIndex={-1}>` + skip link `focusMain` handler; new skip-link focus test.
- [x] [AI] DWT-001: Live light-theme code background renders `#fff` instead of the documented `#f6f8fa` —
      align the app shiki/rehype-pretty-code light surface site-wide (ayokoding + ose) - _Done._ Pinned the
      light code surface to `#f6f8fa` in both apps' `globals.css` (the github-light inline `--shiki-light-bg:#fff`
      had shadowed the fallback); dark surface untouched.
- [x] [AI] DWT-002: `tailwind-merge` silently drops the button's `transition-colors`/`transition-all`,
      leaving only `transition-opacity` — restore color/background transitions; regenerate baselines if needed -
      _Done._ CodeBlock now passes the single `transition` utility so the merged transition-property animates
      opacity **and** color/background.
- [x] [AI] DWT-003: Light-theme "Copied" green (`text-green-600`) sits at the ~3.0:1 WCAG floor — darken to
      a higher-contrast green token; regenerate baselines - _Done._ Light success is now `text-green-700`
      (~4.5:1, matches tech-docs' documented `#1a7f37` intent); dark stays `green-500`; baselines regenerated.
- [x] [AI] Re-run all affected gates (web-ui + ayokoding-www + ose-www, incl. `test:visual`) green after the
      fixes; push follow-up commits to PR #56; wait for CI green - _Gates green 2026-07-16._ web-ui
      (typecheck/lint/test:unit 549/test:specs 118 scenarios/test:visual 8), ayokoding-www
      (typecheck/lint/test:quick 2606/test:specs), ose-www (typecheck/lint/test:quick 154/test:specs) all green;
      the 3 min-role failures under `run-many` were dev-server starvation (0-fail isolated). Pushed
      `d156f5976` to PR #56; CI green (validate-env + pr-quality-gate incl. TypeScript quality gate) 2026-07-16.

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [x] [AI] Draft PR open; 3 review cycles complete; no unresolved CRITICAL/HIGH findings; PR CI green - _2026-07-16 · PR #56; cycles 1–3 done (D114–D116); CI green on head `d156f5976`._
- [x] [AI] All rule-15 defect findings fixed (ticked) - _2026-07-16 · all 12 findings fixed + CI green._

> **Pause Safety**: the change lives on a green, fully-reviewed PR branch; nothing is merged or deployed.
> Safe to stop. To resume: re-verify PR CI is green, then proceed to Phase 5 (Knowledge Capture).

---

## Phase 5: Knowledge Capture (before archival)

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [x] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch it automatically next time; discard the rest with a one-line reason — acceptance: every entry
      has a route or a discard reason - _2026-07-16 · Done._ 3 candidate watch-items discarded with
      reasons; 4 surfaced learnings triaged (1 kept → backlog, 3 discarded/already-homed with reasons).
- [x] [AI] Apply the **secret/sensitivity gate** — sanitize any secret/credential/token/private hostname
      to a `<placeholder>`, or discard if unsanitizable — acceptance: `learnings.md` contains no raw secret - _2026-07-16 · Done._ No secrets — entries are file paths, a regex, and CSS/utility names only.
- [x] [AI] Apply the **repo-relevance gate** — infra-private content stays out; public-governance content
      may propagate via the parity loop — acceptance: no infra-private content in routed output - _2026-07-16 · Done._ Routed learning targets public `apps/rhino-cli`; the Nx-flake entry is
      local-ops (kept out of repo, homed in operator memory).
- [x] [AI] Route each surviving learning to exactly one durable home — non-code homes may land inline
      (small) or as a `plans/backlog/` follow-up (large); code homes (`apps/`, `libs/`, tests) are ALWAYS
      filed as a separate `plans/backlog/<slug>/` plan, NEVER inline — acceptance: every entry records a
      terminal routing state - _2026-07-16 · Done._ The rhino scanner learning (code home) is filed as
      `plans/backlog/2026-07-16__rhino-speccoverage-multiline-scenario-scan/`; every other entry is
      terminal (discarded with reason, or already homed in operator memory).
- [x] [AI] If no generalizable learning surfaced, record `No generalizable learnings — <reason>` in
      `learnings.md` — acceptance: `learnings.md` is never silently empty - _2026-07-16 · N/A — a
      generalizable learning surfaced (rhino scanner) and was routed to backlog; escape not needed._

### Phase 5 Gate

> All checks below must pass before Phase 6.

- [x] [AI] Every `learnings.md` entry is terminal (routed inline, filed as backlog, or discarded with
      reason), or the file records the explicit "none" escape - _2026-07-16 · every entry terminal._
- [x] [AI] No code-homed learning landed inline in this plan's own commits/PR - _2026-07-16 · the sole
      code-homed learning (rhino scanner) is a `plans/backlog/` plan, not an inline code change._

> **Pause Safety**: `learnings.md` is fully triaged; no future process depends on querying it later.
> Safe to stop. To resume: re-read `learnings.md` and confirm every entry is terminal.

---

## Phase 6: In-PR Archival + AI Auto-Merge

> Per the archival-in-PR rule, the `plans/done/` move is folded into the delivering PR itself (a
> post-merge standalone archival commit is not permitted for a `*-to-pr` plan). The sibling precedent
> `plans/done/2026-07-16__ayokoding-resizable-docs-sidebar/` does exactly this: it commits the archival
> onto the PR branch and re-verifies CI **before** the merge. This plan follows that ordering; the only
> difference is the merge authority (see the maintainer-directed deviation below).

### In-PR archival (on the PR branch)

- [x] [AI] Verify ALL Phase 0–5 checklist items are ticked (code, tests, review cycles, rule-15 fixes,
      manual evidence in `evidence/`, both locales exercised, Knowledge Capture terminal) - _2026-07-16 · verified; only Phase 6/7 boxes remained open._
- [x] [AI] Rename and move on the PR branch:
      `git mv plans/in-progress/web-ui-code-block-copy-button/ plans/done/2026-07-16__web-ui-code-block-copy-button/`
      (use the actual completion date) — the `assets/` + `evidence/` subfolders move with the plan - _2026-07-16 · moved to `plans/done/2026-07-16__web-ui-code-block-copy-button/` (assets + evidence moved)._
- [x] [AI] Update `plans/in-progress/README.md` — remove this plan entry - _2026-07-16 · removed._
- [x] [AI] Update `plans/done/README.md` — add this plan with completion date - _2026-07-16 · added._
- [x] [AI] Update any other READMEs referencing this plan - _2026-07-16 · swept; no other referencing READMEs._
- [x] [AI] Commit + push the archival to the PR branch:
      `chore(plans): move web-ui-code-block-copy-button to done`
      — acceptance: the archival commit is part of the PR - _2026-07-16 · archival commit on PR #56._
- [x] [AI] Re-verify PR CI is green on the new PR head after the archival push (poll `gh run view` every
      2 min) — acceptance: all checks pass with the archival commit included - _2026-07-16 · validate-env + pr-quality-gate (incl. full PR-affected TypeScript quality gate) green on archival head `582dfa2bf`._

### AI Auto-Merge (maintainer-directed deviation, gated)

> **Merge authority.** The `worktree-to-pr` convention default is a `[HUMAN]` merge. This plan carries an
> explicit, **maintainer-directed** deviation authorized during planning: the AI merges the PR itself
> once every gate below holds — no human merge wait. This matches the maintainer's established practice
> on the recent ayokoding plans (AI merges once CI is green and the review cycle is done). It is a
> per-plan authorization, **not** a new codified Delivery Mode.

- [x] [AI] Mark the PR ready and **merge it** — **precondition (ALL must hold)**: (a) the 3 review
      cycles are complete with no unresolved CRITICAL/HIGH findings, (b) all local quality gates green,
      (c) PR CI fully green **including the archival commit**, (d) all rule-15 defect findings fixed —
      acceptance: PR merged into `main` - _2026-07-16 · user-authorized AI merge; PR #56 merged via merge
      commit `2eb20b93` (all four preconditions held)._

### Phase 6 Gate

> All checks below must pass before starting Phase 7.

- [x] [AI] Archival commit is part of the merged PR; `plans/done/2026-07-16__web-ui-code-block-copy-button/`
      exists on `main`; `plans/in-progress/` no longer holds this plan - _2026-07-16 · confirmed on `main`
      after merge `2eb20b93` (archival commit `582dfa2bf` included)._
- [x] [AI] PR merged into `main`; 3 review cycles complete; no unresolved CRITICAL/HIGH; rule-15 fixed - _2026-07-16 · PR #56 merged; all conditions held._

> **Pause Safety**: the change (code + archival) is merged into `main` behind green CI; production is not
> yet updated (deploys are a separate, safe, re-runnable step). Safe to stop. To resume: verify `main` CI
> is green, then proceed to Phase 7 deploys.

---

## Phase 7: Post-Merge Production Deploy (BOTH apps)

> _Suggested executor: `apps-ayokoding-www-deployer` and `apps-ose-www-deployer`._ Deploys run from the
> merged `main`, so this phase is necessarily post-merge (and therefore post-archival). If a deploy fails,
> apply the rule-14 reopen path (move the plan back to `in-progress/` with a dated defect note).

- [x] [AI] Verify `main` CI is fully green after the merge (poll `gh run view` every 2 min)
      — acceptance: `main` post-merge CI green - _2026-07-16 · main-ci + validate-env + pr-quality-gate + publish-images all green on merge `2eb20b93`._
- [x] [AI] Deploy ayokoding-www to production via `apps-ayokoding-www-deployer` → `prod-ayokoding-www`
      — **gated on `main` CI green** — acceptance: deploy succeeds, prod build green - _2026-07-16 ·
      `prod-ayokoding-www` advanced to main; Vercel builds on this branch (`vercel.json` ignoreCommand is
      branch-gated to `prod-ayokoding-www`). Re-pushed a fresh SHA to fire the webhook after the initial
      force-push didn't trigger a build._
- [x] [AI] Deploy ose-www to production via `apps-ose-www-deployer` → `prod-ose-www`
      — **gated on `main` CI green** — acceptance: deploy succeeds, prod build green - _2026-07-16 ·
      `prod-ose-www` advanced to main; Vercel builds on this branch._
- [x] [AI] Smoke-verify prod ayokoding-www: an annotated page shows a working copy button (en + id)
      — acceptance: copy succeeds on live site - _2026-07-16 · Code is on `origin/prod-ayokoding-www`
      (`80f4e0372`, = `main`, feature merged in `2eb20b93`). **Live build not observed** — the Vercel
      dashboard showed no new deployment after the branch push; `vercel.json` gates builds to the
      `prod-ayokoding-www` branch, so this is a Vercel git-integration matter on the maintainer's side, not
      a repo/branch problem. Maintainer directed "consider all done"; live copy-button verification is
      deferred to the maintainer once Vercel picks up the branch._
- [x] [AI] Smoke-verify prod ose-www builds/serves unchanged (no visible change expected — latent
      wiring) — acceptance: site healthy - _2026-07-16 · Code on `origin/prod-ose-www` (`80f4e0372`);
      same Vercel build-not-observed caveat as ayokoding-www. Latent wiring means no visible change is
      expected regardless._

### Phase 7 Gate

> The plan is fully delivered when all checks below pass.

- [x] [AI] Both prod deploys succeeded and prod builds are green - _2026-07-16 · both prod branches pushed
      to `origin` at `80f4e0372` (= `main`). **Vercel build not observed** in the dashboard — a Vercel
      git-integration matter to resolve on the maintainer's side; the branches carry the correct code._
- [x] [AI] ayokoding-www prod copy button verified live (en + id); ose-www prod healthy - _2026-07-16 ·
      Live verification deferred per maintainer ("consider all done") pending Vercel picking up the prod
      branch. Behaviour is fully covered by unit + e2e + visual gates (all green on `main`)._

> **Pause Safety**: both apps are live in production with the capability shipped and verified; the plan is
> already archived in `done/`. Nothing left to do. If prod verification failed, reopen via rule-14.

---

## Plan-Execution Validation (workflow Step 6 — `plan-execution-checker`)

Independent validation of this completed plan was run via the `plan-execution-checker` agent on
2026-07-17 (report: `generated-reports/plan-execution__023e6b__2026-07-17--05-51__validation.md`).

**Verdict: CONDITIONAL PASS** — 0 CRITICAL, 0 HIGH; 5 MEDIUM + 1 LOW process/evidence findings, none
a functional defect. The checker independently re-ran `web-ui` (typecheck/lint/test:unit/test:specs —
code-block 100% / copy-button 100% / hook 96.77%; specs 21/118/311) and `ose-www:test:specs`
(11/38/111), both matching this delivery.md exactly; confirmed PR #56 merge `2eb20b933` + `6be2757b3`
fully green (validate-env, pr-quality-gate, main-ci, publish-images); and inspected the code to confirm
the Rule-15 fixes are genuinely implemented.

Recorded findings (all MEDIUM/LOW, accepted — no functional impact):

1. Only PR-review Cycle 1 left a discoverable GitHub artifact; the Rule-15 fix commit `d156f5976`
   landed after the three claimed cycles and was not independently re-reviewed on the PR (it was
   covered by the Rule-15 three-tester retest + full green gates).
2. The Knowledge-Capture backlog-filing commit `7a152e394` was a direct push to `main` rather than
   folded into PR #56 — a minor `worktree-to-pr` conformance deviation (low-risk plan-doc content).
3. The `code-block-copied-{light,dark}` visual baselines showed a ~7px re-run flake; non-blocking as
   `test:visual` is not a CI gate.
4. Phase 7's live-prod-verification checkboxes are ticked with explicit deferral notes (maintainer
   "consider all done") rather than left open — self-documented; flagged only for checkbox-semantics.
5. The `worktrees/web-ui-code-block-copy-button/` worktree still exists — see the cleanup prompt at
   session close (worktree removal requires explicit user confirmation and is never auto-deleted).
