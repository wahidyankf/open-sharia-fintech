# Syllabus Layer — Skills Paths: Accounting

**Custodian**: ayokoding-learning-path-06-skills-accounting

This folder is this plan's own syllabus corpus, created by Phase 1 and never edited into
`ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/` (that corpus is custody-frozen —
see [tech-docs DD-603](../tech-docs.md#design-decisions)). It mirrors the folder convention plan 02
already established for custodied human-readable mirrors, applied inside this plan's own folder.

**The per-course file shape is inherited from plan 02's 121 existing `syllabus/courses/*.md` files,
not invented here** (see [tech-docs DD-627](../tech-docs.md#design-decisions)): same header fields,
same section names and order (`Why this exists · the big idea`, `Prerequisites`, `Accuracy notes`,
`Concepts`, `Worked examples`, `Read more`, `In which paths`), same problem-before-solution framing —
adapted only where the domain genuinely differs (no `Language` field; a "verify" clause means
recompute by hand or spreadsheet, not run code). One inherited section is deliberately **not**
carried over: plan 02's `Capstone spec` (its own `DD-27`, a full runnable per-course capstone) is
replaced by `Applied synthesis (no build — A6)`, because `A6` forbids a build exercise at any
granularity. Every syllabus is authored from domain reasoning and this plan's own grounding file
**first**; external research checks coverage only, per `A12` — see
[tech-docs §Post-authoring verification](../tech-docs.md#syllabus-layer--custody-and-shape).

- `courses/` — one `<course-id>.md` per course, 24 files, each carrying a concept/worked-example
  breakdown an author can write the course from directly (see [tech-docs §Syllabus layer](../tech-docs.md#syllabus-layer--custody-and-shape)).
- `paths/` — the two human-readable path mirrors this plan transcribes into the two manifests'
  `courseOrder`: `manifest-skills-conventional-accounting.md` and
  `manifest-skills-sharia-accounting.md`.

## Course index

**Shared spine (19 courses, referenced by both `conventional-accounting.yaml` and
`sharia-accounting.yaml`, authored exactly once — A11):**

| #   | Course ID                                      | Format            | Stage |
| --- | ---------------------------------------------- | ----------------- | ----- |
| 1   | `accounting-foundations`                       | By Example        | 1     |
| 2   | `chart-of-accounts-and-data-modeling`          | By Example        | 1     |
| 3   | `financial-statements-and-close-cycle`         | By Example        | 1     |
| 4   | `journal-entries-and-posting-mechanics`        | By Example        | 2     |
| 5   | `accrual-accounting-and-revenue-recognition`   | By Example        | 2     |
| 6   | `accounts-payable-and-procure-to-pay`          | By Example        | 2     |
| 7   | `accounts-receivable-and-order-to-cash`        | By Example        | 2     |
| 8   | `managerial-and-cost-accounting`               | By Example        | 2     |
| 9   | `fixed-assets-and-depreciation`                | By Example        | 2     |
| 10  | `inventory-and-cogs-accounting`                | By Example        | 2     |
| 11  | `lease-and-intangible-asset-accounting`        | By Example        | 2     |
| 12  | `multi-currency-accounting-and-fx-translation` | By Example        | 2     |
| 13  | `consolidation-and-multi-entity-accounting`    | By Example        | 2     |
| 14  | `financial-reporting-standards-ifrs-vs-gaap`   | Annotated-concept | 2     |
| 15  | `audit-controls-and-compliance`                | Annotated-concept | 2     |
| 16  | `payroll-and-tax-accounting-essentials`        | By Example        | 2     |
| 17  | `treasury-and-cash-management`                 | By Example        | 2     |
| 18  | `financial-reporting-and-xbrl`                 | Annotated-concept | 2     |
| 19  | `general-ledger-system-architecture`           | By Example        | 2     |

**Sharia-specific extension (5 courses, `sharia-accounting.yaml` only):**

| #   | Course ID                                      | Format            | Stage |
| --- | ---------------------------------------------- | ----------------- | ----- |
| 20  | `sharia-accounting-and-aaoifi-standards`       | Annotated-concept | 3     |
| 21  | `islamic-contract-modeling-for-systems`        | By Example        | 3     |
| 22  | `zakah-computation-and-reporting-for-systems`  | By Example        | 3     |
| 23  | `sukuk-and-islamic-capital-markets-accounting` | Annotated-concept | 3     |
| 24  | `sharia-ledger-system-architecture`            | By Example        | 3     |

See [tech-docs §The twenty-four-course catalog](../tech-docs.md#the-twenty-four-course-catalog) for
the full prerequisite graph.
