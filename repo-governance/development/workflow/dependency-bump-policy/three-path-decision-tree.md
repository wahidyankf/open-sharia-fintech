---
description: The LTS, 60-day stable, and security-override waiver paths used to classify every dependency bump.
when_to_use: Use when classifying which of the three paths applies to a specific package or runtime bump.
---

# Three-Path Decision Tree

For every version bump, classify the package and apply the corresponding path. Then, within whichever path applies, narrow to a single version using the two
[Selection Rules](./selection-rules-within-every-path.md) below.

## Path A — LTS Path (use latest LTS-line patch)

If the package or runtime has an officially designated LTS line, **use the latest LTS patch** regardless of recency, provided it is CVE-clean.

LTS-track packages and runtimes (non-exhaustive examples):

- Node.js (LTS lines: 22 "Jod", 24 "Krypton", etc.)
- .NET (even-numbered major versions: 6, 8, 10 are LTS)
- PostgreSQL (5-year support model — every major is effectively LTS)
- React (de facto LTS treatment for major versions)

Rationale: LTS lines have a soak and curation process built in by the upstream maintainer. Recent LTS patches inherit that soak.

## Path B — 60-Day Stable + CVE-Clean Path

If the package has no LTS designation, **use the latest version that satisfies BOTH**:

1. Released **at least 60 days** before the bump date (release date ≤ today − 60 days)
2. CVE-clean — zero known unpatched CVEs per NVD, GitHub Security Advisories, Snyk DB, and the project's own security page

Examples of non-LTS packages (most JavaScript libraries, Go, Rust, TypeScript, Tailwind, Vitest, Storybook, ESLint, Playwright, lucide-react, Zod, Shiki, mermaid, etc.).

Rationale: 60 days is the minimum soak window for the community to surface regression bugs and security issues. Most non-LTS upstreams cut patch releases monthly; 60 days catches the next-cycle fixes before the version is adopted here.

## Path C — Security-Override Waiver

When **no version satisfies BOTH the 60-day rule AND CVE-cleanness**, use the most recent CVE-patched version (or the security-recommended LTS) and document a waiver.

The waiver MUST include:

- Package name and version pinned
- The CVE(s) requiring the recent version (with NVD or GHSA URL)
- The CVE severity (Critical / High / Medium / Low)
- The release date of the pinned version
- Brief justification (e.g., "Critical RCE; no older patched version exists")
- Sign-off identity (the engineer or AI agent applying the waiver)

Waivers are documented in the plan that introduces the bump (in `tech-docs.md` under a "Security Waivers" subsection) and propagated to a long-lived `docs/reference/security-waivers.md` file (create if missing).
