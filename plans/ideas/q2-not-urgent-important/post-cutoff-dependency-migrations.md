# Post-cutoff dependency migrations

One-line summary: track the dependency bumps deferred out of the stack-update plan and promote each to
a real bump plan as its soak window or upstream availability clears.

> Surfaced 2026-05-16 during stack-update execution.

## Problem / context

Several dependency migrations were deliberately deferred out of the stack-update plan — some pending a
60-day production soak (per the dependency-bump policy's Path A/B/C tree), some pending upstream
availability. Left untracked, they silently rot; tracked here, they get re-evaluated as their windows
elapse. This folds the standalone "libraries update" note as well — do not create a second
dependency-update two-pager; add to this one.

## Why now

Soak windows elapse continuously — several deferred bumps may already be eligible (e.g. TypeScript 6.0
was eligible after ~2026-05-23) and should be picked up before they fall further behind.

## Prior art / precedents

- **Dependency Bump Stability & Safety Policy** — the repo's Path A/B/C soak-window gate each deferred
  bump is re-evaluated against. [dependency-bump-policy](../../../repo-governance/development/workflow/dependency-bump-policy.md)
- **Renovate** — established tool that automates exactly this "track deferred bumps, promote as they
  clear" problem via scheduled PRs. [docs.renovatebot.com](https://docs.renovatebot.com/)
- **Dependabot** — GitHub's automated version-update tool for keeping pending dependency upgrades
  tracked. [GitHub docs](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates)
- **Semantic Versioning** — the MAJOR.MINOR.PATCH scheme framing which of these bumps are breaking.
  [semver.org](https://semver.org/)

## Proposed direction (sketch)

Promote each to a dependency-bump plan as it clears its gate. The current deferred set:

- `aws-sdk-go` v1 → v2 (transitive via `narqo/go-badge`; v1 EOL 2025-07-31; S3-crypto CVEs affect only
  unused `s3crypto` codepaths)
- TypeScript 6.0; ESLint 10 + react-hooks 7; Zod 4.x; lucide-react 1.x; @xstate/react 6.x;
  TailwindCSS 4.3.x; @effect/platform 0.96.x + effect 4.x (all post-cutoff, 60-day soak)
- Storybook 10.3/10.4 (currently pinned to 10.2.10 for CVE clearance)
- Volta → mise (Volta last released Dec 2024)
- Microsoft Defender / dotnet 10.0.300 brew bottle (currently via `dotnet-install.sh`)
- `vite` 7.4+ then `@vitejs/plugin-react` 6.0.1 (currently reverted to `^5.1.4` — plugin-react 6 needs
  vite's `./internal` subpath, unavailable on the installed transitive vite)

## Rough scope & non-goals

In scope: the deferred-bump list above, re-evaluated per the dependency-bump policy.

Out of scope (for now): bumps not on this list; any bump that is not CVE-clean across the required
sources.

## Risks & open questions

- Which entries are now eligible vs. still soaking? (open — needs a per-entry date check)
- `aws-sdk-go` v1 → v2 is transitive via `narqo/go-badge`; it cannot move until the upstream does or we
  fork. (open)

## What success looks like + promotion signal

Success: each deferred bump either lands or is explicitly dropped with a reason — none silently rots.
Promote **per-bump** to its own dependency-bump plan as that bump's soak window clears and it passes
the policy gate.
