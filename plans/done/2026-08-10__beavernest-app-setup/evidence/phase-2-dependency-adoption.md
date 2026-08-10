# Phase 2 Dependency Adoption Evidence

## Selection Record

- Selection date: 2026-08-03
- Path B cutoff: 2026-06-04

| Package                      | Exact version | Path | Release date | Rule 5a                                                                        | Rule 5b                                                                                                          | Clearance                                                       |
| ---------------------------- | ------------- | ---- | ------------ | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| `dbup-sqlite`                | `6.0.4`       | B    | 2025-11-06   | Latest stable NuGet release eligible before the cutoff                         | NuGet shows no deprecation and the DbUp vendor repository has no release-blocker notice for this package version | CLEAR                                                           |
| `Microsoft.Data.Sqlite`      | `10.0.10`     | A    | 2026-07-14   | Latest .NET 10 LTS-line patch                                                  | NuGet shows a stable, non-deprecated release and the Microsoft vendor repository has no release-blocker notice   | CLEAR (patch-of via the explicit native-library override below) |
| `SQLitePCLRaw.lib.e_sqlite3` | `2.1.12`      | C    | 2026-07-14   | Latest patched compatible 2.1-line release required by `Microsoft.Data.Sqlite` | NuGet marks 2.1.11 deprecated and vulnerable; 2.1.12 is not deprecated and has no release-blocker notice         | WAIVER                                                          |

## Security Clearance

For `dbup-sqlite` and the effective `Microsoft.Data.Sqlite` dependency graph on 2026-08-03:

- NVD keyword query returned zero matching CVE records.
- GitHub Advisory Database's NuGet package filter returned zero matching advisories.
- Snyk package pages reported "No vulnerabilities found in the latest version."
- Vendor sources reviewed: the DbUp project/release history and the Microsoft.Data.Sqlite repository and
  NuGet package page; neither reported a fatal functional defect for the selected release.
- CISA KEV has no selected-package CVE to cross-reference. No KEV fast-track applies.
- The direct override fixes the otherwise-selected transitive `SQLitePCLRaw.lib.e_sqlite3` 2.1.11,
  which has **CVE-2025-6965 / GHSA-2m69-gcr7-jv3q** (High, CVSS 7.7). NVD, GitHub Advisories,
  Snyk, the package/vendor pages, and CISA KEV were checked for the override. It is not KEV-listed.
  EPSS is 0.7439 (99.442 percentile), so the policy's EPSS escalation requires Path C urgency.

## Path C Security Waiver

`SQLitePCLRaw.lib.e_sqlite3` `2.1.12` was released 2026-07-14, after the Path B cutoff. It is pinned
as the direct compatible override for the vulnerable `2.1.11` pulled by `Microsoft.Data.Sqlite`
`10.0.10`; no eligible CVE-clean 2.1-line release existed before the cutoff. The waiver is required
to patch CVE-2025-6965 (High, CVSS 7.7; EPSS 0.7439) and is signed by Codex (AI executor). It is also
recorded in `docs/reference/security-waivers.md`.
