# Business Requirements — web-ui Code-Block Copy Button

## Business Goal

Give readers of the platform's public content sites a **frictionless, one-click way to copy code
snippets to the clipboard**, and deliver it as a **single reusable design-system primitive** so every
current and future app inherits the same behaviour, accessibility, and visual treatment for free.

## Business Rationale (WHY)

AyoKoding's teaching style leans heavily on **densely-annotated worked examples**. A representative Lua
block from the live content authors annotations directly inside the fence
(`apps/ayokoding-www/content/en/learn/fundamentally-strong/software-engineer/just-enough-lua/learning/advanced.md`):

```text
-- Example 59: error() can raise ANY value, not just a string
local ok, err = pcall(function()   -- => runs the inner function in protected mode
  error({ code = 42 })             -- => error()'s argument can be any Lua value -- here, a table
end)                                -- => closes the protected function
print(err.code)                    -- => err IS the table passed to error(), untouched
```

Those `--` comments and `-- => output` markers are the pedagogy. A learner who wants to paste the
example into an editor and run it today must **drag-select across syntax-highlight `<span>`s**, which is
error-prone: it is easy to clip a leading line, drop trailing whitespace, or (on some renderers) grab
gutter decorations. A positioned Copy button that yields the **verbatim fenced source** eliminates that
friction and preserves every annotation exactly as authored. `[Judgment call]` — no telemetry exists on
these sites; the reasoning is UX-first, grounded in the annotation-heavy content that already ships.

Building the capability **once in `libs/web-ui`** (rather than per-app) matches the repo's
design-system direction: the resizable-panel primitive established the "impl + hook + model split,
locale-agnostic label props with English defaults" precedent
(`libs/web-ui/src/primitives/resizable-panel/`), and both sites already share a byte-identical
code-block render shape, so a shared component is the minimum-viable abstraction — not premature
generalization. `[Repo-grounded]`

## Business Impact

**Pain points removed**

- Manual, lossy drag-selection of annotated snippets on AyoKoding (bilingual audience: en + id).
- Divergent, copy-pasted per-app implementations if each site solved this independently.

**Expected benefits**

- Higher snippet-reuse and lower reader friction on the platform's flagship learning site. `[Judgment call]`
- A reusable `CopyButton` primitive usable anywhere a value must be copied (a CLI command, a token, a
  URL), not just code blocks — compounding value for later features. `[Repo-grounded]` (API resolved in
  `prd.md`/`tech-docs.md`)
- Cross-app visual and accessibility consistency from a single audited source. `[Repo-grounded]`

## Affected Roles (hats the solo maintainer wears)

- **Design-system owner** — authors and reviews the new `libs/web-ui` primitive.
- **AyoKoding content-platform maintainer** — wires labels (en/id) and validates the live reader flow.
- **OSE-www maintainer** — accepts the latent wiring that ships the capability ahead of code content.
- **Release operator** — runs the two production deploys after merge.

Consuming agents: `swe-ui-maker`/`swe-ui-checker`/`swe-ui-fixer` (primitive), `swe-typescript-dev`
(app wiring), `swe-e2e-dev` (ayokoding live proof), `pr-review-maker`/`pr-review-fixer` (PR cycle),
`apps-ayokoding-www-deployer` + `apps-ose-www-deployer` (production).

## Business-Level Success Signals

- **Observable fact** — after delivery, every non-mermaid fenced block on both sites renders a Copy
  button; clicking it places the verbatim annotated source on the clipboard. Verified by the web-ui
  unit/visual suite, the ayokoding live e2e, and the ose-www unit test. `[Repo-grounded]` once executed.
- **Observable fact** — mermaid blocks render **no** Copy button (they remain diagrams). Verified by a
  dedicated exclusion test in both apps. `[Repo-grounded]` once executed.
- **Qualitative** — a keyboard and screen-reader user can trigger the copy and receive an announced
  confirmation (see `prd.md` accessibility scenarios). `[Judgment call]` on reader benefit; the a11y
  behaviour itself is test-enforced.

## Business-Scope Non-Goals

- No analytics/telemetry on copy usage.
- No inline-code copy.
- No mermaid/diagram copy or export.
- No new content authored to "show off" the ose-www capability.

## Business Risks and Mitigations

| Risk                                                                                        | Mitigation                                                                                                                          |
| ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Copied text silently loses newlines/whitespace (rehype-pretty-code splits lines into spans) | Verbatim multi-line fidelity is an explicit Gherkin acceptance criterion + a live e2e assertion; see `tech-docs.md` extraction note |
| Clipboard write fails on non-secure context (HTTP)                                          | Graceful failure: no false "Copied" state; behaviour specified and tested (`prd.md`)                                                |
| Button invisible/unreachable for keyboard or touch users (hover-only reveal)                | Always-visible on touch + focus-visible is a HARD accessibility requirement with axe + Gherkin coverage                             |
| Regression to the existing mermaid render path                                              | New replace-case is ordered strictly after the mermaid guard; exclusion test pins it                                                |
| Shipping ose-www wiring with no visible change confuses future maintainers                  | The "latent wiring" decision is documented in `prd.md`/`tech-docs.md` and this plan                                                 |
