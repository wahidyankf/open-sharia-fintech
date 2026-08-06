# Source-code credential scanning (evaluate Betterleaks)

One-line summary: catch hard-coded credentials in `.rs` / `.ts` / `.tf` source **before** they leave
the developer's machine, rather than only after a push.

> Idea, added 2026-07-21 (original capture undated).

## Problem / context

Today the only credential-scanning coverage is GitHub Secret Scanning, which runs **post-push** — by
the time it fires, the secret has already left the machine and entered git history (permanent). There
is no pre-commit or CI gate that inspects source files for hard-coded credentials before they land.

## Why now

Betterleaks (an MIT-licensed gitleaks successor, v1.0.0 early 2026) is emerging as a maintained option
just as gitleaks itself has gone feature-frozen with an unresolved entropy false-positive regression
([#1830](https://github.com/gitleaks/gitleaks/issues/1830)) that misfires on Rust config struct field
names — so the incumbent tool is not a good fit for this repo's Rust-heavy source.

## Prior art / precedents

- **gitleaks** — the incumbent pre-commit + CI secret scanner; its entropy false-positive
  regression is the exact reason this idea seeks an alternative.
  [gitleaks #1830](https://github.com/gitleaks/gitleaks/issues/1830)
- **TruffleHog** — a maintained pre-commit/CI credential detector, a candidate to evaluate
  alongside Betterleaks. [trufflehog](https://github.com/trufflesecurity/trufflehog)
- **detect-secrets** — a pre-commit secret detector with a tuned false-positive posture, relevant
  to the Rust-source precision concern. [detect-secrets](https://github.com/Yelp/detect-secrets)
- **Betterleaks** — the MIT gitleaks successor this idea proposes evaluating (no stable public URL
  verified).
- **Secrets and Env Standards convention** — the repo's existing no-secrets-in-git policy this gate
  would reinforce pre-push.
  [convention](../../../repo-governance/conventions/security/secrets-and-env-standards.md)

## Proposed direction (sketch)

- Once Betterleaks reaches stable production use, evaluate it for pre-commit + CI credential detection
  across `.rs` / `.ts` / `.tf` source.
- Wire it as a warning-grade gate alongside the existing cross-language linters, not a hard blocker at
  first.
- Keep GitHub Secret Scanning as the post-push backstop — the two are complementary, not exclusive.

## Rough scope & non-goals

In scope: pre-push detection of hard-coded credentials in committed source files.

Out of scope (for now): replacing GitHub Secret Scanning; `.env*` handling (already covered by the
env-file-access guardrails); secret rotation or remediation workflow.

## Risks & open questions

- False-positive rate on Rust struct field names — the exact failure mode that makes gitleaks
  unsuitable. Does Betterleaks avoid it? (open — needs hands-on evaluation)
- Does Betterleaks actually reach stable, maintained production use, or stall like its predecessor?
  (open)
- The 60-day production-soak window (per the dependency-bump policy) has not yet elapsed.

## What success looks like + promotion signal

Success: a hard-coded credential in source is caught on the developer's machine, before it can enter
git history. This is a **time-gated** idea — ready to promote only once Betterleaks has 60+ days of
production soak and a stable release, and a quick evaluation confirms an acceptable false-positive rate
on this repo's Rust source. Until then it correctly stays a two-pager.
