# Verification Log — ayokoding-learning-path-06-skills-accounting

The machine-checkable ledger for this plan's carried verification debt. Every line below is asserted
by an acceptance clause in [delivery.md](./delivery.md); the human-readable statement of each item,
its named primary source, and its escape hatch live in
[tech-docs §Open verification items](./tech-docs.md#open-verification-items-oi-1-through-oi-4).

## Why this file exists

The research seeding this plan marked only **three** items as directly fetched and verified: the
AAOIFI Financial Accounting Standards index, AAOIFI's adoption-by-country page, and IAI's PSAK
Syariah index. Everything else is search-summarised. A4 forbids promoting any of it to fact silently,
so the markers travel here as **status lines a grep can check** rather than as prose a reviewer has
to interpret.

## Status lines (grep-checkable — one per item, first column anchored)

Each line begins at column 0 and matches `^OI-<n>: <STATUS>`. Valid statuses:

| Status          | Meaning                                                                                                                                            |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `OPEN`          | Not yet resolved. **Blocks** the phase named in tech-docs.                                                                                         |
| `RESOLVED`      | Checked against the named primary source. Line carries the source URL and the access date.                                                         |
| `SCOPED-AROUND` | The primary source could not be reached; the affected course teaches the structure without publishing the specific claim. Line carries the reason. |
| `ROUTED`        | Not a research item — a cross-plan seam handed to its owning plan. Line carries the target.                                                        |

Do **not** delete a line when it resolves — rewrite its status in place, so the ledger stays a
complete record.

OI-1: OPEN
OI-2: OPEN
OI-3: OPEN
OI-4: OPEN

## Item summaries

- **OI-1** `[Needs Verification]` — **Indonesian PSAK numbering.** Sources show both a
  "PSAK 59 / SIFAS 101-109" generation and a "PSAK 101-110" series. Both cannot be current. Primary
  source to check: **IAI's published PSAK Syariah standard list**. Blocks course #17.
- **OI-2** `[Needs Verification]` — **Riba doctrinal basis.** Currently sourced only from Wikipedia,
  which is not a primary source. Primary source to check: an **AAOIFI Shari'ah Standard** or an
  **IFSB publication**. The practical consequence is well-attested; the minority
  time-value-of-money position is not settled and is not this corpus's to settle. Blocks course #17.
- **OI-3** `[Unverified]` — **Three-jurisdiction detail beyond the three fetched indexes** —
  governance mechanics, adoption relationships, effective dates. Sources to check: the three fetched
  indexes plus **Bank Negara Malaysia's Shariah Governance Policy 2019**. Blocks courses #17, #18 and
  #20.
- **OI-4** open, **cross-plan** — plan 02's doc-level rule _"A path may omit a prerequisite only if it
  also omits every course that needs it"_ reads as forbidding this plan's link-don't-walk manifest.
  Plan 02's **implemented** `checkPrerequisiteConsistency` already permits it, so only the prose needs
  a cross-domain carve-out. Routed in Phase 0, never edited from here. Blocks nothing mechanically.

## Verified facts carried in (do not re-litigate, do re-confirm at authoring)

`[Verified]` AAOIFI Financial Accounting Standards numbers for the contract types this corpus covers:
**FAS 3** (Mudaraba), **FAS 4** (Musharaka), **FAS 7** (Salam), **FAS 9** (Zakah), **FAS 10**
(Istisnaa), **FAS 28** (Murabaha and deferred payment sales), **FAS 32–34** (Ijarah through
sukuk-holder reporting). AAOIFI keeps **Financial Accounting Standards** and **Shari'ah Standards** as
two separate series — "what to book" versus "what makes the contract compliant". **FAS numbers
outside this list are `[Unverified]`** and are re-verified or dropped, never published on trust.
