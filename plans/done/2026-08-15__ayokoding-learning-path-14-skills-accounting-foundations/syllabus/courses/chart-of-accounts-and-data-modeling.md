# Chart of Accounts and Data Modeling (By Example)

**Course ID**: `chart-of-accounts-and-data-modeling` · **Format**: By Example.

**Scope note**: Designs an original, purpose-fit account structure and maps accounting events to it. It links to `sql-essentials` for relational modeling and query work rather than teaching either subject.

## Why this exists · the big idea

- **The problem before the solution**: a balanced ledger cannot answer a question when its account categories hide the needed distinction.
- **Keep-this-if-you-forget-everything**: name accounts for decisions and controls, not for a copied template.

## Prerequisites

- **Prior courses**: `accounting-foundations`, `sql-essentials` (linked, never re-taught).
- **Assumed knowledge**: the accounting equation and basic data-record vocabulary.

## Accuracy notes

- [Verified — stable domain fact] A chart of accounts is organization-specific; all example names and identifiers are original, with no copied chart or vendor schema.

## Concepts

- **co-01 · account-purpose** — an account represents a decision-useful class of balances.
- **co-02 · account-code** — a stable identifier supports posting and review.
- **co-03 · hierarchy** — groups roll up into statement lines without erasing detail.
- **co-04 · normal-balance** — an account’s expected side detects implausible postings.
- **co-05 · dimensions** — optional attributes separate context from account identity.
- **co-06 · posting-rule** — allowed combinations prevent category drift.
- **co-07 · change-governance** — new accounts need a reason, owner, and effective date.
- **co-08 · forward-boundary** — statement assembly is owned by `financial-statements-and-close-cycle`.

## Worked examples

### Beginner

- **ex-01 · starter-service-chart** — define assets, liabilities, equity, revenue, and expense accounts for a small service entity. (co-01, co-03)

### Intermediate

- **ex-02 · separate-deposit-from-revenue** — add accounts that prevent customer deposits from being reported as earned income. (co-04, co-06)

### Advanced

- **ex-03 · governed-new-account-request** — evaluate a requested account and record the approval rationale. (co-05, co-07)

## Applied synthesis (no build — A6)

Review an original chart for a small entity, identify three ambiguous classifications, and propose governed changes; do not design a database or write queries.

## In which paths

- `skills/conventional-accounting` — Stage 1 · turns balanced entries into reportable categories.
- `skills/sharia-accounting` — Stage 1 · supplies the shared structure before later contract-specific additions.

## Read more

- **Conceptual Framework** — IFRS Foundation. https://www.ifrs.org/issued-standards/list-of-standards/conceptual-framework/ — classification context.
