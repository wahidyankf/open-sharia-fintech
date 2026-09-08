---
description: The two optional post-mortem sections (Background, Supporting Data) and the authoritative Sev-1 through Sev-4 severity tier scale with software examples
when_to_use: Read this when deciding whether to add optional Background or Supporting Data content, or when classifying an incident's severity tier.
---

# Optional Sections and Severity Scale

## Optional Sections

These sections are encouraged when they add clarity:

- **Background** — relevant system context a reader outside the incident would need
- **Supporting Data** — graphs, log excerpts, metrics snapshots (use Mermaid or fenced code
  blocks; never paste raw secrets or credential material)

**Placement**: `Background` may appear **before Summary** when substantial up-front context is
required to understand the incident; otherwise place optional sections after References. Their
placement is flexible — clarity for the reader wins.

## Severity Scale

Every post-mortem must classify the incident with one of the following tiers. This scale is
the single source of truth for incident severity in this repository.

| Tier      | Label    | Definition                                                                                                            |
| --------- | -------- | --------------------------------------------------------------------------------------------------------------------- |
| **Sev-1** | Critical | Data loss, corrupted production state, or total outage of a production site or critical API                           |
| **Sev-2** | Major    | Significant production degradation, sustained CI blockage affecting all merges, or multi-app deployment failure       |
| **Sev-3** | Moderate | Intermittent failure, single-app degradation, coverage-threshold regression, or parity-guard breakage with workaround |
| **Sev-4** | Minor    | Cosmetic or low-impact issue; affects dev workflow but not production users                                           |

Use the format `Sev-N — Label` in the metadata table, e.g., `Sev-3 — Moderate`.

**Software severity examples**:

- **Sev-1**: Production database migration gone wrong corrupts user records across all OrganicLever
  accounts; Vercel deployment serves a broken build to all visitors of `www.organiclever.com`.
- **Sev-2**: GitHub Actions CI is blocked for all PRs due to a broken Nx Cloud integration;
  multi-site Vercel outage takes `ayokoding.com` and `oseplatform.com` offline simultaneously.
- **Sev-3**: Prettier post-tool hook reformats generated `.amazonq/` binding files, breaking the
  cross-vendor parity guard on every `Edit` operation; coverage-threshold regression blocks
  `test:quick` for one app after a dependency bump.
- **Sev-4**: A linting rule produces spurious warnings on an infrequently edited markdown file;
  a `dev` server hot-reload fails to pick up a CSS change.
