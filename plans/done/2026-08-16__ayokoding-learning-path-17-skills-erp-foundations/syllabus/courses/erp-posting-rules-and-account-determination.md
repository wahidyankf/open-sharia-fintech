# ERP Posting Rules and Account Determination (By Example)

**Course ID**: `erp-posting-rules-and-account-determination` · **Format**: By Example.

**Scope note**: Designs deterministic account-selection evidence; it excludes general-ledger engine implementation. License-aware.

**Short summary**: Posting policy must be inspectable from its input facts and chosen rule.

## Why this exists · the big idea

- **The problem before the solution**: manual account choices make identical events diverge.
- **Keep-this-if-you-forget-everything**: store why an account was determined, not just the account.

## Prerequisites

- **Prior courses**: `erp-document-lifecycle-and-state-machines`.
- **Assumed knowledge**: debit and credit basics.

## Accuracy notes

- [Repo-grounded, tech-docs.md] Examples use original account labels and rules.

## Concepts

- **co-01 · posting-event** — approved business transition requiring accounting effect.
- **co-02 · determination-key** — facts used to select a posting rule.
- **co-03 · rule-precedence** — explicit tie-breaking among valid rules.
- **co-04 · account-mapping** — controlled mapping from facts to account role.
- **co-05 · effective-policy** — version active for the event date.
- **co-06 · exception-queue** — accountable route for unmatched facts.
- **co-07 · balanced-entry** — equal debits and credits produced by a rule.
- **co-08 · explanation-trace** — evidence of input, rule, and output.

## Worked examples

### Beginner

- **ex-01 · item-group-rule** — determine a stock account from an item group — verify the selected rule id. (co-02, co-04)

### Intermediate

- **ex-02 · effective-date-rule** — apply the policy active at posting date — verify superseded policy is not used. (co-05)

### Advanced

- **ex-03 · unmatched-event** — route missing facts to an exception queue — verify no guessed account posts. (co-06)

## In which paths

- `skills/conventional-erp` — Stage A · posting foundation.
- `skills/sharia-erp` — Stage A · posting foundation.
