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
[Plans Organization Convention § Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

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

- [ ] [AI] Provision the worktree from latest `origin/main`:
      `git worktree add worktrees/web-ui-code-block-copy-button -b web-ui-code-block-copy-button origin/main`
      — acceptance: worktree dir exists, branch checked out
- [ ] [AI] Install dependencies in the worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized
- [ ] [AI] Converge the toolchain: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift
- [ ] [AI] Establish baseline for affected projects:
      `npx nx run-many -t typecheck lint test:quick test:specs -p web-ui ayokoding-www ose-www`
      — acceptance: baseline pass/fail recorded; all preexisting failures documented
- [ ] [AI] Establish e2e baseline (build + run) for `ayokoding-www-fe-e2e`:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: baseline recorded (green or documented flakes)
- [ ] [AI] Establish web-ui visual baseline: `npx nx run web-ui:test:visual`
      — acceptance: existing Storybook visual snapshots pass
- [ ] [AI] Resolve all preexisting failures before proceeding — acceptance: no unresolved preexisting failures

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift
- [ ] [AI] `npx nx run-many -t typecheck lint test:quick test:specs -p web-ui ayokoding-www ose-www`
      baseline recorded and every preexisting failure resolved (zero unresolved)
- [ ] [AI] `ayokoding-www-fe-e2e:test:e2e` and `web-ui:test:visual` baselines recorded

> **Pause Safety**: only the worktree/toolchain was set up and the baseline recorded — no feature work
> exists yet. Safe to stop indefinitely. To resume: re-run the baseline `run-many` command and confirm
> it is still clean.

---

## Phase 1: web-ui Primitive (`CopyButton` + `useCopyToClipboard` + `CodeBlock`)

> _Suggested executor: `swe-ui-maker` (primitive authoring) + `swe-ui-checker`_

### Specs & Gherkin Delivery (RED first)

- [ ] [AI] RED: author `specs/libs/web-ui/behavior/gherkin/code-block/copy-button.feature` and
      `code-block.feature` _New files_ with the `@unit`/`@visual` scenarios from `prd.md`
      — acceptance: files exist; `npx nx run web-ui:test:specs` fails (no step defs yet)

### Cycle 1.1 — Clipboard hook writes value

- [ ] [AI] RED: add a failing test in
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

- [ ] [AI] GREEN: implement `use-copy-to-clipboard.ts` _New_ (`copy`, `copied`, `resetMs`) per
      `tech-docs.md` — acceptance: the new test passes
- [ ] [AI] REFACTOR: extract the timeout-cleanup pattern, add "why-not-what" JSDoc matching
      `use-resizable-width.ts` density — acceptance: `web-ui:test:unit` green, no lint warnings

### Cycle 1.2 — Success swaps icon + announces (builds `copy-button.tsx`)

- [ ] [AI] RED: add a failing test in `libs/web-ui/src/primitives/code-block/copy-button.test.tsx` _New_
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

- [ ] [AI] GREEN: implement `copy-button.tsx` _New_ composing `Button` (`variant="ghost"
    size="icon-sm"`), the `Copy`→`Check` swap, `aria-label`, and the
      `<span role="status" aria-live="polite" className="sr-only">` — acceptance: the test passes
- [ ] [AI] REFACTOR: confirm `data-slot="code-block-copy"`; JSDoc density — acceptance: green

### Cycle 1.3 — Success reverts after timeout

- [ ] [AI] RED: add a failing test asserting the icon returns to `Copy` and the announcement clears once
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

- [ ] [AI] GREEN: wire the hook's `resetMs` timeout into the button's icon + announcement state
      — acceptance: the test passes
- [ ] [AI] REFACTOR: ensure timeout cleanup on unmount — acceptance: green

### Cycle 1.4 — Failed clipboard write shows no false success

- [ ] [AI] RED: add a failing test with a rejecting clipboard stub asserting the button stays resting and
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

- [ ] [AI] GREEN: guard the success transition on `writeText` resolving — acceptance: the test passes
- [ ] [AI] REFACTOR: dedupe the resolve/reject branches — acceptance: green

### Cycle 1.5 — Operable by keyboard

- [ ] [AI] RED: add a failing test asserting a focused CopyButton copies its value on `Enter`.
      **Gherkin (binds) →** "The copy button is operable by keyboard"

      ```gherkin
      @unit
      Scenario: The copy button is operable by keyboard
        Given a CopyButton is focused
        When the user presses Enter
        Then the clipboard receives the button's value
      ```

      — acceptance: `web-ui:test:unit` fails on the keyboard test

- [ ] [AI] GREEN: confirm the native `<button>` semantics satisfy it (no custom key handler needed)
      — acceptance: the test passes
- [ ] [AI] REFACTOR: none expected; keep the button element native — acceptance: green

### Cycle 1.6 — Exposes an accessible name (default "Copy")

- [ ] [AI] RED: add a failing test asserting the default accessible name is "Copy".
      **Gherkin (binds) →** "The copy button exposes an accessible name"

      ```gherkin
      @unit
      Scenario: The copy button exposes an accessible name
        Given a CopyButton rendered with the default labels
        When the accessibility tree is inspected
        Then the button has an accessible name of "Copy"
      ```

      — acceptance: `web-ui:test:unit` fails on the default-name test

- [ ] [AI] GREEN: wire `copyLabel` default ("Copy") into `aria-label` — acceptance: the test passes
- [ ] [AI] REFACTOR: none expected — acceptance: green

### Cycle 1.7 — Accessible name can be localized

- [ ] [AI] RED: add a failing test asserting a `copyLabel="Salin"` override sets the accessible name.
      **Gherkin (binds) →** "The copy button's accessible name can be localized"

      ```gherkin
      @unit
      Scenario: The copy button's accessible name can be localized
        Given a CopyButton rendered with copyLabel "Salin"
        When the accessibility tree is inspected
        Then the button has an accessible name of "Salin"
      ```

      — acceptance: `web-ui:test:unit` fails on the override test

- [ ] [AI] GREEN: thread `copyLabel`/`copiedLabel` props into `aria-label` — acceptance: the test passes
- [ ] [AI] REFACTOR: assert BOTH default and override like the resizable-panel precedent — acceptance: green

### Cycle 1.8 — No accessibility violations

- [ ] [AI] RED: add a failing `vitest-axe` test asserting zero violations in the resting state.
      **Gherkin (binds) →** "The copy button has no accessibility violations"

      ```gherkin
      @unit
      Scenario: The copy button has no accessibility violations
        Given a CopyButton is rendered in its resting state
        When an automated accessibility scan runs
        Then no accessibility violations are reported
      ```

      — acceptance: `web-ui:test:unit` fails on the axe test

- [ ] [AI] GREEN: resolve any axe finding (contrast/name) — acceptance: `toHaveNoViolations` passes
- [ ] [AI] REFACTOR: none expected — acceptance: green

### Cycle 1.9 — Meets the minimum target size

- [ ] [AI] RED: add a failing test asserting the rendered box is ≥ 24 × 24 CSS px.
      **Gherkin (binds) →** "The copy button meets the minimum target size"

      ```gherkin
      @unit
      Scenario: The copy button meets the minimum target size
        Given a CopyButton rendered at its default size
        When its rendered box is measured
        Then both dimensions are at least 24 CSS pixels
      ```

      — acceptance: `web-ui:test:unit` fails on the size test

- [ ] [AI] GREEN: confirm `size="icon-sm"` (`size-8` = 32 px) satisfies it — acceptance: the test passes
- [ ] [AI] REFACTOR: none expected — acceptance: green

### Cycle 1.10 — CodeBlock renders children + copy button (builds `code-block.tsx`)

- [ ] [AI] RED: add a failing test in `libs/web-ui/src/primitives/code-block/code-block.test.tsx` _New_
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

- [ ] [AI] GREEN: implement `code-block.tsx` _New_ (`group relative` wrapper, children, positioned
      `CopyButton`, `code`/`copyLabel`/`copiedLabel` props) — acceptance: the test passes
- [ ] [AI] REFACTOR: JSDoc, `cn` merge of passthrough `className` — acceptance: green

### Cycle 1.11 — Copying yields the verbatim multi-line source

- [ ] [AI] RED: add a failing test copying a three-line annotated `code` prop byte-for-byte incl.
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

- [ ] [AI] GREEN: pass the `code` prop straight to the copy value (no trimming) — acceptance: the test passes
- [ ] [AI] REFACTOR: none expected — acceptance: green

### Cycle 1.12 — CodeBlock establishes its own positioning context

- [ ] [AI] RED: add a failing test asserting the wrapper is relatively-positioned with
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

- [ ] [AI] GREEN: ensure the wrapper carries `relative` + `data-slot="code-block"` — acceptance: the test passes
- [ ] [AI] REFACTOR: none expected — acceptance: green

### Gherkin step-def binding + Storybook + visual (GREEN the specs)

- [ ] [AI] GREEN: implement `copy-button.steps.tsx` + `code-block.steps.tsx` _New_ via
      `@amiceli/vitest-cucumber` loading the `.feature` files.
      **Gherkin (aggregate binder) →** binds every `@unit` scenario in `copy-button.feature` +
      `code-block.feature` (whole-feature consumer for `test:specs`; not one-cycle-per-scenario per the
      aggregate-BDD-binder exception) — acceptance: `npx nx run web-ui:test:specs` exits 0
- [ ] [AI] Add `copy-button.stories.tsx` + `code-block.stories.tsx` _New_ (CSF3,
      `title: "Primitives/CopyButton"` / `"Primitives/CodeBlock"`, resting + copied + light/dark stories,
      `tags:["autodocs"]`) — acceptance: `npx nx run web-ui:storybook` builds the stories
- [ ] [AI] Add visual cases to `libs/web-ui/e2e/components.visual.ts` for the resting + copied stories in
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

- [ ] [AI] Export from `libs/web-ui/src/primitives/index.ts`: add
      `export * from "./code-block/code-block";` and `export * from "./code-block/copy-button";`
      — acceptance: `npx nx run web-ui:typecheck` resolves the new exports

### Local Quality Gates (Before Commit) — Phase 1

- [ ] [AI] `npx nx run-many -t typecheck lint test:quick test:specs -p web-ui` — all green
- [ ] [AI] `npx nx run web-ui:test:visual` — visual baselines pass
- [ ] [AI] Fix ALL failures (including any preexisting) and re-run to confirm

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes
> (Root Cause Orientation). Commit preexisting fixes separately with appropriate messages.

### Commit Guidelines — Phase 1

- [ ] [AI] Commit thematically, Conventional Commits, e.g.
      `feat(web-ui): add CopyButton, CodeBlock, and useCopyToClipboard primitives`
- [ ] [AI] Keep Gherkin/spec files and visual baselines in cohesive commits; preexisting fixes separate

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [ ] [AI] `npx nx run-many -t typecheck lint test:unit test:quick test:specs -p web-ui` all green
- [ ] [AI] `npx nx run web-ui:test:visual` green with committed baselines
- [ ] [AI] `CopyButton` + `CodeBlock` exported from the primitives barrel and typecheck-resolvable

> **Pause Safety**: the web-ui primitive is fully implemented, tested, exported, and committed on the
> worktree branch; no app consumes it yet. Safe to stop. To resume: re-run
> `npx nx run-many -t test:quick test:specs -p web-ui`.

---

## Phase 2: ayokoding-www Wiring (bilingual, live proof)

> _Suggested executor: `swe-typescript-dev` (renderer + i18n) + `swe-e2e-dev` (live e2e)_

### Specs & Gherkin Delivery (RED first)

- [ ] [AI] RED: author
      `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/content/code-block-copy.feature` _New_ with
      the ayokoding `@unit @e2e`/`@e2e` scenarios from `prd.md`
      — acceptance: file exists; `npx nx run ayokoding-www:test:specs` fails (no step defs)

### Cycle 2.1 — i18n keys (pure-data underpin)

- [ ] [AI] RED: add a failing test asserting `t("en","copy")==="Copy"`, `t("id","copy")==="Salin"`,
      `t("en","copied")==="Copied"`, `t("id","copied")==="Tersalin"` in
      `apps/ayokoding-www/src/features/i18n/core/translations.test.ts` _New file_ (no i18n-keys test
      exists yet; `html-lang.test.ts` is the sibling-pattern precedent in this folder).
      **Gherkin (underpins) →** "A non-mermaid code block renders a copy button"; "The copy button is
      labelled in Indonesian on the Indonesian site" (a pure-data key test — supplies the localized labels
      those scenarios rely on without binding any single scenario's steps)
      — acceptance: `ayokoding-www:test:unit` fails
- [ ] [AI] GREEN: add `copy`/`copied` keys to BOTH `en` and `id` maps in
      `apps/ayokoding-www/src/features/i18n/core/translations.ts` (near `resizableSidebarHandleLabel`)
      — acceptance: the i18n test passes
- [ ] [AI] REFACTOR: confirm placement mirrored in both locale maps — acceptance: green

### Cycle 2.2 — Renderer wraps a non-mermaid figure (builds the replace-case)

- [ ] [AI] RED: add a failing unit test in the ayokoding `markdown-renderer` test asserting a non-mermaid
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

- [ ] [AI] GREEN: add the non-mermaid replace-case (ordered AFTER the mermaid guard) to
      `apps/ayokoding-www/src/features/content/shell/markdown-renderer.tsx`, threading the previously
      unused `locale` prop into `t(locale,"copy")`/`t(locale,"copied")`, importing `CodeBlock` from
      `@open-sharia-enterprise/web-ui/primitives` and reusing `getTextContent(pre)` per `tech-docs.md`
      — acceptance: the renderer test passes
- [ ] [AI] REFACTOR: dedupe the figure-guard logic; confirm no hydration/`"use client"` boundary change
      — acceptance: `ayokoding-www:test:quick` green

### Cycle 2.3 — Renderer excludes mermaid figures

- [ ] [AI] RED: add a failing unit test asserting a mermaid figure yields `MermaidDiagram` and NO copy
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

- [ ] [AI] GREEN: confirm the new case runs only for `data-language !== "mermaid"` (ordered after the
      mermaid guard) — acceptance: the exclusion test passes; mermaid path unchanged
- [ ] [AI] REFACTOR: none expected — acceptance: green

### Cycle 2.4 — Copy button labelled in Indonesian on the id site

- [ ] [AI] RED: add a failing unit test asserting the `id` locale sets the accessible name "Salin".
      **Gherkin (binds) →** "The copy button is labelled in Indonesian on the Indonesian site"

      ```gherkin
      @unit @e2e
      Scenario: The copy button is labelled in Indonesian on the Indonesian site
        Given a visitor opens an Indonesian content page containing a fenced code block
        When the accessibility tree is inspected
        Then the copy button has the Indonesian accessible name "Salin"
      ```

      — acceptance: `ayokoding-www:test:unit` fails on the id-label test

- [ ] [AI] GREEN: confirm `t("id","copy")` flows to the `CodeBlock`'s `copyLabel` — acceptance: the test passes
- [ ] [AI] REFACTOR: none expected — acceptance: green

### Cycle 2.5 — Live e2e: verbatim annotated clipboard

- [ ] [AI] RED: add a failing Playwright-BDD step def in
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

- [ ] [AI] GREEN: run the e2e; fix any newline-fidelity gap per the `tech-docs.md` contingency (join
      per-`[data-line]` with `\n` only if a test proves loss; normalize `\r\n`→`\n` before comparison per
      the Windows caveat) — acceptance: `ayokoding-www-fe-e2e:test:e2e` green for the new scenario
- [ ] [AI] REFACTOR: fold shared selectors into `common.steps.ts` if reused — acceptance: green

### Cycle 2.6 — Live e2e: Copied confirmation

- [ ] [AI] RED: add a failing e2e step def asserting the button shows a "Copied" confirmation after a
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

- [ ] [AI] GREEN: confirm the icon-swap + live-region announcement satisfy it — acceptance: green
- [ ] [AI] REFACTOR: none expected — acceptance: green

### Cycle 2.7 — Live e2e: reachable on a touch viewport

- [ ] [AI] RED: add a failing e2e step def asserting the button is visible without hover on a touch
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

- [ ] [AI] GREEN: confirm the `@media (hover: none)` always-visible rule satisfies it — acceptance: green
- [ ] [AI] REFACTOR: none expected — acceptance: green

### Gherkin step-def binding (GREEN the specs) — Phase 2

- [ ] [AI] GREEN: implement any remaining `@unit`/`@e2e` step defs so the whole
      `code-block-copy.feature` is consumed.
      **Gherkin (aggregate binder) →** binds every scenario in
      `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/content/code-block-copy.feature`
      (whole-feature consumer for `test:specs` + `playwright-bdd`; not one-cycle-per-scenario per the
      aggregate-BDD-binder exception) — acceptance: `npx nx run ayokoding-www:test:specs` exits 0

### Local Quality Gates (Before Commit) — Phase 2

- [ ] [AI] `npx nx run-many -t typecheck lint test:quick test:specs -p ayokoding-www` — all green
- [ ] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` — all scenarios green
- [ ] [AI] Fix ALL failures (incl. preexisting) and re-run to confirm

### Manual UI Verification (Playwright MCP) — all locales × breakpoints

- [ ] [AI] Start dev server: `npx nx dev ayokoding-www`
- [ ] [AI] Supported locales confirmed: `en`, `id`
      (`apps/ayokoding-www/src/features/i18n/core/config.ts`)
- [ ] [AI] For EACH locale (`/en/...`, `/id/...`) × EACH breakpoint (375 / 768 / 1280 px) navigate to the
      annotated Lua page via `browser_navigate` + `browser_resize` — acceptance: code block + copy button
      render
- [ ] [AI] Click the copy button via `browser_click`; verify Check swap + "Copied" and (via injected
      read) the clipboard holds the verbatim annotated source — acceptance: pass per locale
- [ ] [AI] Verify `id` accessible name "Salin" via `browser_snapshot`; verify zero `browser_console_messages`
      errors per locale
- [ ] [AI] Capture one screenshot per locale per breakpoint via `browser_take_screenshot` →
      `evidence/phase-2-copy-button-[locale]-[breakpoint]px.png` — acceptance: files exist in `evidence/`
- [ ] [AI] Document evidence inline here: reference each screenshot (`![alt](./evidence/...)`) + console
      status per locale

### Commit Guidelines — Phase 2

- [ ] [AI] Commit thematically, e.g. `feat(ayokoding-www): add copy button to content code blocks (en/id)`
      and a separate `test(ayokoding-www-fe-e2e): cover code-block copy` if cleaner

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [ ] [AI] `npx nx run-many -t typecheck lint test:quick test:specs -p ayokoding-www` all green
- [ ] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` green (copy present, mermaid excluded, verbatim
      clipboard, id label, touch-visible)
- [ ] [AI] `evidence/` holds en+id screenshots across the three breakpoints

> **Pause Safety**: ayokoding-www renders and copies verbatim annotated snippets bilingually, proven by
> unit + live e2e + manual evidence, committed on the worktree branch. Safe to stop. To resume: re-run
> `npx nx run ayokoding-www-fe-e2e:test:e2e`.

---

## Phase 3: ose-www Wiring (latent, unit only)

> _Suggested executor: `swe-typescript-dev`_

### Specs & Gherkin Delivery (RED first)

- [ ] [AI] RED: author
      `specs/apps/ose/behavior/platform-web/gherkin/content/code-block-copy.feature` _New_ (ose-www's
      frontend surface is `platform-web`, per `apps/ose-www-fe-e2e/playwright.config.ts`) with the two
      ose-www `@unit` scenarios from `prd.md`
      — acceptance: file exists; `npx nx run ose-www:test:specs` fails

### Cycle 3.1 — Renderer wraps a non-mermaid figure (builds the replace-case)

- [ ] [AI] RED: add a failing unit test in the ose-www `markdown-renderer` test asserting a non-mermaid
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

- [ ] [AI] GREEN: add the non-mermaid replace-case (ordered AFTER the mermaid guard) to
      `apps/ose-www/src/features/content/shell/markdown-renderer.tsx`, importing `CodeBlock` from
      `@open-sharia-enterprise/web-ui/primitives` and reusing `getTextContent(pre)` (no labels →
      English defaults) — acceptance: the wrap test passes; mermaid path unchanged
- [ ] [AI] REFACTOR: confirm no `"use client"`/server-boundary change; add a comment noting the latent
      wiring (no live non-mermaid content today) — acceptance: `ose-www:test:quick` green

### Cycle 3.2 — Renderer leaves a mermaid figure as a diagram

- [ ] [AI] RED: add a failing unit test asserting a mermaid figure renders as a diagram with NO copy
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

- [ ] [AI] GREEN: confirm the new case runs only for `data-language !== "mermaid"` — acceptance: the
      exclusion test passes; mermaid path unchanged
- [ ] [AI] REFACTOR: none expected — acceptance: green

### Gherkin step-def binding (GREEN the specs) — Phase 3

- [ ] [AI] GREEN: implement step defs consuming the whole ose-www feature.
      **Gherkin (aggregate binder) →** binds both scenarios in
      `specs/apps/ose/behavior/platform-web/gherkin/content/code-block-copy.feature` (whole-feature
      consumer for `test:specs`; not one-cycle-per-scenario per the aggregate-BDD-binder exception)
      — acceptance: `npx nx run ose-www:test:specs` exits 0

### Local Quality Gates (Before Commit) — Phase 3

- [ ] [AI] `npx nx run-many -t typecheck lint test:quick test:specs -p ose-www` — all green
- [ ] [AI] Fix ALL failures (incl. preexisting) and re-run to confirm

### Commit Guidelines — Phase 3

- [ ] [AI] Commit, e.g.
      `feat(ose-www): wire copy button into content code blocks (latent, unit-tested)`

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [ ] [AI] `npx nx run-many -t typecheck lint test:quick test:specs -p ose-www` all green
- [ ] [AI] ose-www mermaid figures still render as diagrams (exclusion test green)

> **Pause Safety**: all three projects (web-ui, ayokoding-www, ose-www) build and pass their gates on
> the worktree branch; nothing is pushed. Safe to stop. To resume: re-run
> `npx nx run-many -t test:quick test:specs -p web-ui ayokoding-www ose-www`.

---

## Phase 4: Draft PR + PR-Review Maker→Fixer Cycle

> _Suggested executor: `pr-review-maker` + `pr-review-fixer` for the review cycle._

- [ ] [AI] Push the branch to origin: `git push -u origin web-ui-code-block-copy-button`
- [ ] [AI] Open a **draft PR** into `main` (title:
      `feat(web-ui): code-block copy button across ayokoding-www and ose-www`; body summarizes scope +
      links this plan) — acceptance: PR number recorded

### Post-Push CI Verification

- [ ] [AI] Monitor ALL GitHub Actions workflows triggered by the push (poll every 2 min, one
      `gh run view --json status,conclusion` per wakeup; no `gh run watch`)
- [ ] [AI] Verify ALL CI checks pass — no exceptions; fix root causes and push follow-ups until green

### PR-Review Maker→Fixer Cycle (3 sequential, CI-gated)

- [ ] [AI] Cycle 1 — `pr-review-maker` reviews via the GitHub Reviews API; `pr-review-fixer` addresses
      every finding and pushes to the PR branch; wait for CI green — acceptance: cycle 1 CI green
- [ ] [AI] Cycle 2 — repeat maker→fixer; wait for CI green — acceptance: cycle 2 CI green
- [ ] [AI] Cycle 3 — repeat maker→fixer; wait for CI green — acceptance: cycle 3 CI green, no unresolved
      CRITICAL/HIGH findings

### Rule-15 Three-Tester Retest (before archival/merge)

- [ ] [AI] Run the three live-site testers (`web-exploratory-tester` + `web-usability-tester` +
      `web-design-tester`) against the running ayokoding-www code-block pages across `en` and `id` —
      acceptance: EWT/UWT/DWT findings + SG/USS spec-gaps recorded
- [ ] [AI] Append each finding here as a new unchecked, source-attributed checkbox
      (`- [ ] EWT-NNN:` / `- [ ] UWT-NNN:` / `- [ ] DWT-NNN: <defect> — fix before archival`); route each
      SG-###/USS-### into the specs steps
- [ ] [AI] Fix every rule-15 EWT/UWT/DWT defect finding before archival — deferral requires explicit user
      permission (only when genuinely impossible); SG-###/USS-### may be triaged or deferred with rationale

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [ ] [AI] Draft PR open; 3 review cycles complete; no unresolved CRITICAL/HIGH findings; PR CI green
- [ ] [AI] All rule-15 defect findings fixed (ticked)

> **Pause Safety**: the change lives on a green, fully-reviewed PR branch; nothing is merged or deployed.
> Safe to stop. To resume: re-verify PR CI is green, then proceed to Phase 5 (Knowledge Capture).

---

## Phase 5: Knowledge Capture (before archival)

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch it automatically next time; discard the rest with a one-line reason — acceptance: every entry
      has a route or a discard reason
- [ ] [AI] Apply the **secret/sensitivity gate** — sanitize any secret/credential/token/private hostname
      to a `<placeholder>`, or discard if unsanitizable — acceptance: `learnings.md` contains no raw secret
- [ ] [AI] Apply the **repo-relevance gate** — infra-private content stays out; public-governance content
      may propagate via the parity loop — acceptance: no infra-private content in routed output
- [ ] [AI] Route each surviving learning to exactly one durable home — non-code homes may land inline
      (small) or as a `plans/backlog/` follow-up (large); code homes (`apps/`, `libs/`, tests) are ALWAYS
      filed as a separate `plans/backlog/<slug>/` plan, NEVER inline — acceptance: every entry records a
      terminal routing state
- [ ] [AI] If no generalizable learning surfaced, record `No generalizable learnings — <reason>` in
      `learnings.md` — acceptance: `learnings.md` is never silently empty

### Phase 5 Gate

> All checks below must pass before Phase 6.

- [ ] [AI] Every `learnings.md` entry is terminal (routed inline, filed as backlog, or discarded with
      reason), or the file records the explicit "none" escape
- [ ] [AI] No code-homed learning landed inline in this plan's own commits/PR

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

- [ ] [AI] Verify ALL Phase 0–5 checklist items are ticked (code, tests, review cycles, rule-15 fixes,
      manual evidence in `evidence/`, both locales exercised, Knowledge Capture terminal)
- [ ] [AI] Rename and move on the PR branch:
      `git mv plans/in-progress/web-ui-code-block-copy-button/ plans/done/2026-07-16__web-ui-code-block-copy-button/`
      (use the actual completion date) — the `assets/` + `evidence/` subfolders move with the plan
- [ ] [AI] Update `plans/in-progress/README.md` — remove this plan entry
- [ ] [AI] Update `plans/done/README.md` — add this plan with completion date
- [ ] [AI] Update any other READMEs referencing this plan
- [ ] [AI] Commit + push the archival to the PR branch:
      `chore(plans): move web-ui-code-block-copy-button to done`
      — acceptance: the archival commit is part of the PR
- [ ] [AI] Re-verify PR CI is green on the new PR head after the archival push (poll `gh run view` every
      2 min) — acceptance: all checks pass with the archival commit included

### AI Auto-Merge (maintainer-directed deviation, gated)

> **Merge authority.** The `worktree-to-pr` convention default is a `[HUMAN]` merge. This plan carries an
> explicit, **maintainer-directed** deviation authorized during planning: the AI merges the PR itself
> once every gate below holds — no human merge wait. This matches the maintainer's established practice
> on the recent ayokoding plans (AI merges once CI is green and the review cycle is done). It is a
> per-plan authorization, **not** a new codified Delivery Mode.

- [ ] [AI] Mark the PR ready and **merge it** — **precondition (ALL must hold)**: (a) the 3 review
      cycles are complete with no unresolved CRITICAL/HIGH findings, (b) all local quality gates green,
      (c) PR CI fully green **including the archival commit**, (d) all rule-15 defect findings fixed —
      acceptance: PR merged into `main`

### Phase 6 Gate

> All checks below must pass before starting Phase 7.

- [ ] [AI] Archival commit is part of the merged PR; `plans/done/2026-07-16__web-ui-code-block-copy-button/`
      exists on `main`; `plans/in-progress/` no longer holds this plan
- [ ] [AI] PR merged into `main`; 3 review cycles complete; no unresolved CRITICAL/HIGH; rule-15 fixed

> **Pause Safety**: the change (code + archival) is merged into `main` behind green CI; production is not
> yet updated (deploys are a separate, safe, re-runnable step). Safe to stop. To resume: verify `main` CI
> is green, then proceed to Phase 7 deploys.

---

## Phase 7: Post-Merge Production Deploy (BOTH apps)

> _Suggested executor: `apps-ayokoding-www-deployer` and `apps-ose-www-deployer`._ Deploys run from the
> merged `main`, so this phase is necessarily post-merge (and therefore post-archival). If a deploy fails,
> apply the rule-14 reopen path (move the plan back to `in-progress/` with a dated defect note).

- [ ] [AI] Verify `main` CI is fully green after the merge (poll `gh run view` every 2 min)
      — acceptance: `main` post-merge CI green
- [ ] [AI] Deploy ayokoding-www to production via `apps-ayokoding-www-deployer` → `prod-ayokoding-www`
      — **gated on `main` CI green** — acceptance: deploy succeeds, prod build green
- [ ] [AI] Deploy ose-www to production via `apps-ose-www-deployer` → `prod-ose-www`
      — **gated on `main` CI green** — acceptance: deploy succeeds, prod build green
- [ ] [AI] Smoke-verify prod ayokoding-www: an annotated Lua page shows a working copy button (en + id)
      — acceptance: copy succeeds on live site
- [ ] [AI] Smoke-verify prod ose-www builds/serves unchanged (no visible change expected — latent
      wiring) — acceptance: site healthy

### Phase 7 Gate

> The plan is fully delivered when all checks below pass.

- [ ] [AI] Both prod deploys succeeded and prod builds are green
- [ ] [AI] ayokoding-www prod copy button verified live (en + id); ose-www prod healthy

> **Pause Safety**: both apps are live in production with the capability shipped and verified; the plan is
> already archived in `done/`. Nothing left to do. If prod verification failed, reopen via rule-14.
