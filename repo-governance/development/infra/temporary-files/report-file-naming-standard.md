---
title: "Report File Naming Standard"
description: The 4-part `{agent-family}__{uuid-chain}__{timestamp}__{suffix}.md` pattern, its separators, and why UUIDs/timestamps must be real.
category: explanation
subcategory: development
tags: [temporary-files, ai-agents, file-organization, best-practices]
created: 2025-12-01
when_to_use: Use when constructing a checker or fixer report filename.
---

# Report File Naming Standard

**CRITICAL REQUIREMENT**: All checker/fixer agents use standardized report naming pattern aligned with repository file naming convention.

**Pattern**: `{agent-family}__{uuid-chain}__{YYYY-MM-DD--HH-MM}__{suffix}.md`

**Exempt from ordinal prefixes.** Report filenames never carry a leading `NN-` ordinal, and
[Ordinal Filename Prefixes](../../../conventions/structure/ordinal-filename-prefixes.md) does not
apply to them: they are generated artifacts in `generated-reports/`, ordered by their timestamp
component rather than by a parent index.

**Components** (4 parts):

- `{agent-family}`: Agent name WITHOUT checker/fixer/maker suffix (e.g., `repo-rules`, `ayokoding-web`, `docs`, `plan`, `plan-execution`)
- `{uuid-chain}`: Execution hierarchy as underscore-separated 6-char UUIDs (e.g., `a1b2c3`, `a1b2c3_d4e5f6`)
- `{YYYY-MM-DD--HH-MM}`: Timestamp in UTC+7 with double dash between date and time
- `{suffix}`: Report type suffix (`audit`, `fix`, `validation`)

**Separator Rules**:

- Double underscore (`__`) separates the 4 major components
- Underscore (`_`) separates UUIDs within the uuid-chain
- Double dash (`--`) separates date from time within timestamp
- Single dash (`-`) separates components within date (YYYY-MM-DD) and time (HH-MM)
- NO "report" keyword in filename (redundant - location in `generated-reports/` makes purpose clear)

**Why this pattern**:

- **Alignment**: Uses double-underscore separators to clearly delimit major filename segments (agent family, UUID chain, timestamp, suffix)
- **Consistency**: Same separator style as documentation files (double underscore for major segments)
- **Clarity**: Agent family, UUID chain, timestamp, and suffix all clearly separated
- **Parallelization**: UUID prevents file collisions when multiple agents run simultaneously
- **Traceability**: UUID chain shows parent-child execution hierarchy
- **Sortability**: Agent family first enables grouping; timestamp enables chronological sorting within groups

**Example files**:

```
generated-reports/repo-rules__a1b2c3__2025-12-14--20-45__audit.md
generated-reports/repo-rules__a1b2c3__2025-12-14--20-45__fix.md
generated-reports/ayokoding-web__d4e5f6__2025-12-14--15-30__audit.md
generated-reports/ayokoding-web__a1b2c3_d4e5f6__2025-12-14--15-30__audit.md
generated-reports/ose-web-content__g7h8i9__2025-12-14--15-30__audit.md
generated-reports/docs__b2c3d4__2025-12-15--10-00__validation.md
generated-reports/plan__c3d4e5__2025-12-15--11-30__validation.md
generated-reports/plan-execution__d4e5f6__2025-12-15--14-00__validation.md
```

**Pattern Rules**:

- Use double underscore (`__`) to separate the 4 components (agent-family, uuid-chain, timestamp, suffix)
- Use underscore (`_`) to separate UUIDs within the uuid-chain
- Use double dash (`--`) to separate date from time in timestamp
- UUID MUST be 6 lowercase hex characters (generated via `uuidgen | head -c 6`)
- Timestamp MUST be UTC+7 (YYYY-MM-DD--HH-MM format)
- Zero-pad all timestamp components (01 not 1, 09 not 9)
- Agent family is lowercase with single dashes (multi-word: `ose-web-content`, `plan-execution`)
- Suffix is lowercase, no plurals (`audit` not `audits`)

**CRITICAL - UUID and Timestamp Generation:**

**FAIL: WRONG - Using placeholder values:**

```bash
# DO NOT use placeholder values
filename="repo-rules__abc123__2025-12-14--00-00__audit.md"  # WRONG!
```

**PASS: CORRECT - Execute bash commands for actual UUID and current time:**

```bash
# MUST generate real UUID and timestamp
uuid=$(uuidgen | tr '[:upper:]' '[:lower:]' | head -c 6)
timestamp=$(TZ='Asia/Jakarta' date +"%Y-%m-%d--%H-%M")
filename="repo-rules__${uuid}__${timestamp}__audit.md"
# Example: repo-rules__a1b2c3__2025-12-14--16-43__audit.md (actual values!)
```

**Why this is critical:** Placeholder timestamps like "00-00" defeat the entire purpose of timestamping. Reports must have accurate creation times for audit trails, chronological sorting, and debugging. See [Timestamp Format Convention](../../../conventions/formatting/timestamp.md) for complete details.

Continued in [Report File Naming Standard — Repository Audit and Link Validation Reports](./report-file-naming-early-report-types.md).
