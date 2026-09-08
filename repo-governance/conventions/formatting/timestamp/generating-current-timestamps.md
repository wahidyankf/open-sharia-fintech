---
description: Bash commands AI agents and scripts must execute to generate real UTC+7 timestamps for full timestamps, dates, and filenames, plus anti-patterns to avoid.
when_to_use: Use when an agent or script needs to generate a real current timestamp instead of a placeholder value.
---

# Generating Current Timestamps

**For AI Agents and Scripts:**

When generating timestamps programmatically, use these bash commands to get the current time in UTC+7.

**CRITICAL REQUIREMENT:** You MUST execute the bash command to get the actual current time. NEVER use placeholder values like "00-00" or hardcoded timestamps.

## Full Timestamp (ISO 8601)

```bash
TZ='Asia/Jakarta' date +"%Y-%m-%dT%H:%M:%S+07:00"
```

**Output example:** `2025-12-14T16:23:00+07:00`

**Use for:**

- Cache file `lastFullScan` and `lastChecked` fields
- Audit report headers
- Log timestamps
- Any full timestamp requirement

## Date Only

```bash
TZ='Asia/Jakarta' date +"%Y-%m-%d"
```

**Output example:** `2025-12-14`

**Use for:**

- Documentation frontmatter (`created` field) — outside `repo-governance/`, which refuses it
- Date-only requirements

## Filename Format (with double dash)

```bash
TZ='Asia/Jakarta' date +"%Y-%m-%d--%H-%M"
```

**Output example:** `2025-12-14--16-23`

**Use for:**

- Report filenames (e.g., `repo-rules__2025-12-14--16-23__audit.md`)
- Any filename requiring timestamp

**CRITICAL:** This command MUST be executed via Bash tool to get the real current time. Never hardcode or use placeholder values.

## Common Format Patterns

| Use Case           | Command                                             | Output Example               |
| ------------------ | --------------------------------------------------- | ---------------------------- |
| Full ISO 8601      | `TZ='Asia/Jakarta' date +"%Y-%m-%dT%H:%M:%S+07:00"` | `2025-12-14T16:23:00+07:00`  |
| Date only          | `TZ='Asia/Jakarta' date +"%Y-%m-%d"`                | `2025-12-14`                 |
| Filename timestamp | `TZ='Asia/Jakarta' date +"%Y-%m-%d--%H-%M"`         | `2025-12-14--16-23`          |
| Human readable     | `TZ='Asia/Jakarta' date +"%B %d, %Y at %H:%M"`      | `December 14, 2025 at 16:23` |

**Note:** All commands use `TZ='Asia/Jakarta'` to ensure UTC+7 timezone regardless of system timezone.

## Anti-Patterns - NEVER Do This

**FAIL: WRONG - Using placeholder timestamps:**

```bash
# DO NOT hardcode placeholder values
filename="repo-rules__2025-12-14--00-00__audit.md"  # WRONG!
timestamp="2025-12-14--00-00"  # WRONG!
```

**Problem:** Using "00-00" or any placeholder defeats the purpose of timestamping. Files will have incorrect creation times and cannot be sorted chronologically.

**PASS: CORRECT - Execute bash command for real time:**

```bash
# Execute the command to get actual current time
timestamp=$(TZ='Asia/Jakarta' date +"%Y-%m-%d--%H-%M")
filename="repo-rules__${timestamp}__audit.md"
# Example output: repo-rules__2025-12-14--16-43__audit.md
```

**Why this matters:**

- Timestamps track when operations actually occurred
- Enable chronological sorting and comparison
- Critical for audit trails and debugging
- Placeholder values render timestamps useless

**For AI agents:** You MUST use the Bash tool to execute the timestamp command. Never generate filenames with hardcoded or placeholder times.
