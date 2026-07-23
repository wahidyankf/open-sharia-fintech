---
title: "Artifact: Trust-or-Verify Decision Log for One Session"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 88
---

> A table mapping every change in one session to an explicit trust-lightly-or-verify-closely
> decision, with a matching verify entry on every risky row -- exercises co-17, co-24.

| Change                                              | Decision       | Rationale                                          | Verify entry                                                                         |
| --------------------------------------------------- | -------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Add `.gitignore` entry for `build/`                 | Trust-lightly  | Low-stakes, standard, reversible                   | --                                                                                   |
| Rename internal helper `_fmt` -> `_format_currency` | Trust-lightly  | Mechanical rename; the type-checker catches misses | --                                                                                   |
| Add HMAC-based session-token comparison             | Verify-closely | Security-critical; timing-attack surface           | Line-by-line review + human sign-off before merge (ex-41)                            |
| Change discount-cap constant to a config value      | Verify-closely | Affects real money; a wrong value ships silently   | Reconciled against the finance spec; property test added covering 0/10/50/100% cases |
| `DROP COLUMN` migration on `orders`                 | Verify-closely | Irreversible in production                         | Human decision gate + backup confirmed before applying (ex-44)                       |
| Update README wording                               | Trust-lightly  | No runtime effect                                  | --                                                                                   |

The three `Trust-lightly` rows carry no verify entry -- that is the point of trusting them lightly,
per co-17's calibration: a skim was sufficient, and demanding a full verify entry for every row
regardless of risk would defeat the purpose of calibrating review depth at all. Every
`Verify-closely` row, by contrast, carries a specific, named verification step, not a generic
"reviewed."

**Verify**: every row marked `Verify-closely` (the HMAC comparison, the discount-cap constant, the
`DROP COLUMN` migration) has a non-empty, specific `Verify entry` describing what verification
actually happened -- satisfying ex-48's rule that every risky change has a matching verify entry.
