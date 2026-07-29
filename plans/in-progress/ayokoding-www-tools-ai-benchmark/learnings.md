# Learnings: ayokoding-www-tools-ai-benchmark

<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

Append one entry per generalizable learning **as it surfaces** — not reconstructed from memory at the
end. Sanitize per the secret/sensitivity gate before writing anything down.

Entry shape:

```markdown
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized)
- **Why it might generalize**: the litmus reasoning
- **Terminal state**: routed inline to `<path>` / filed as `plans/backlog/<slug>/` / discarded — `<reason>`
```

Phase 11 (Knowledge Capture) triages every entry to a durable home or an explicit discard. Code-homed
learnings (`apps/`, `libs/`, tests) are **always** filed as a separate `plans/backlog/<slug>/` plan and
never landed inline in this plan's commits or PR.

If execution genuinely surfaces nothing generalizable, replace this file's body with the explicit
escape line: `No generalizable learnings — <one-line reason>`.

<!-- ── entries below ── -->

## Learning: `reuseExistingServer: true` can silently mask a stale/broken build in e2e runs

- **Context**: running a scoped e2e Playwright subset during Phase 10's Rule-15 retest fixes; the
  suite exited cleanly against port 3101.
- **Observation**: a long-lived `next dev` process (started hours earlier, before this session's
  code changes) was already listening on port 3101. Playwright's `reuseExistingServer: true` found
  it and skipped running its own configured `webServer.command` entirely — so the e2e run silently
  exercised stale dev-mode code instead of the production build the config actually specifies
  (`NODE_ENV: "production"`, a standalone server, e2e-specific env vars like
  `AYOKODING_WEB_MANIFESTS_DIR`). A later FULL e2e run against the same stale server produced a wall
  of unrelated-looking failures across course-paths/navigation scenarios — all traced to the reused
  server never having the e2e fixture manifests directory wired in.
- **Why it might generalize**: any Playwright config with `reuseExistingServer: true` (the common,
  recommended local-dev convenience setting) will silently reuse ANY process already bound to the
  target port, including one from an unrelated earlier session/purpose, with no warning that the
  configured `webServer.command` (and its env vars) was skipped. Worth a repo-wide check that CI
  always sets `reuseExistingServer: false` (or that CI runners never have a stray process on the
  port) — a local dev habit of leaving `next dev` running can silently invalidate local e2e runs.
- **Terminal state**: not yet triaged — candidate for `plans/backlog/` if a repo-wide audit of
  `reuseExistingServer` usage across e2e projects is warranted; noted here per Phase 11's own
  routing step.

## Learning: cmdk's `CommandItem value` re-filters already server-filtered results

- **Context**: fixing UWT-001 (global search excluding the Tools section) surfaced a follow-on e2e
  regression once the fix let a Tools-page title reach the search results.
- **Observation**: `search-dialog.tsx`'s `<CommandItem value={result.slug}>` fed cmdk's own
  client-side fuzzy filter (`shouldFilter` defaults to `true`) the SLUG, not the title. Since
  results are already filtered server-side, this is redundant filtering that happens to be
  harmless whenever a query's distinctive words also appear in the slug (e.g. "golang" against a
  slug containing `.../golang/...`) — but silently drops an already-correct result whenever the
  title's distinctive words are absent from the slug (e.g. "AI Model Benchmark" vs. slug
  `tools/ai-benchmark`, no "model"). A pre-existing latent defect that had gone unnoticed because
  every previously-tested query happened to hit the lucky case.
- **Why it might generalize**: any cmdk (or similar client-filtered-list) component fed
  server-pre-filtered data should either set `shouldFilter={false}` or make `value` a superset of
  the text the server actually matched against — otherwise the client filter can silently disagree
  with the server and hide correct results, in a way that's invisible until a query targets a field
  the client filter doesn't see.
- **Terminal state**: routed inline — fixed directly in
  `apps/ayokoding-www/src/features/search/shell/search-dialog.tsx` this session (`value` now
  includes the title). No further backlog needed; noting here as the generalizable pattern per
  Phase 11's routing step.

## Learning: Tailwind v4's `@theme {}` compiler silently drops some custom-property declarations from its compiled `:root`

- **Context**: fixing the M-14 band-contrast defect required adding four new
  `--chart-band-*-wash` custom properties to `libs/web-ui-token/src/ayokoding.css`, alongside the
  pre-existing `-ink` declarations in the same `@theme {}` block.
- **Observation**: the four `-wash` declarations, added inside `@theme {}` in the exact same shape
  as the already-working `-ink` declarations right next to them, were silently absent from the
  compiled stylesheet — confirmed via a live browser's
  `getComputedStyle(document.documentElement).getPropertyValue("--chart-band-sonnet-wash")`
  returning an empty string for all four, while the identically-shaped `-ink` declarations in the
  SAME block resolved fine. No build error, no warning — the properties simply did not reach
  `:root`. The workaround: moving the four `-wash` declarations out of `@theme {}` into a plain
  `:root {}` block (declared earlier in the same file) made them resolve correctly with no other
  change.
- **Why it might generalize**: Tailwind v4's `@theme {}` directive is not a transparent pass-through
  to `:root` — it runs through Tailwind's own theme-token compiler (Lightning CSS), which appears to
  drop some custom-property declarations under conditions this session did not fully isolate (the
  four dropped properties and the working `-ink` properties differ only in name suffix and value
  reference target, both alias `var(--warm-0)` no differently in kind than other resolving
  declarations). Any future custom-property addition inside this repo's `@theme {}` blocks
  (`libs/web-ui-token/src/*.css`) should be verified via `getComputedStyle` on a live page before
  being trusted, not assumed to "just work" the way the many pre-existing `@theme` declarations do.
  Standing guidance in
  [`repo-governance/development/frontend/design-tokens.md`](../../../repo-governance/development/frontend/design-tokens.md)
  and the `swe-developing-frontend-ui` skill's own `reference/design-tokens.md` currently state
  uncaveated that "bare variables belong in `:root`/`.dark`, Tailwind aliases belong in `@theme`" —
  neither currently warns that `@theme` can silently drop a declaration.
- **Terminal state**: recorded here per this session's own routing step; whether this generalizes
  into a caveat on the two `design-tokens.md` surfaces above (and whether the drop condition can be
  further isolated — e.g. via a minimal Tailwind v4 reproduction) is Phase 11's triage call, not this
  PR's — Phase 11 has not yet run at the time this entry was written.
