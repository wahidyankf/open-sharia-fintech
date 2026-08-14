# Validation Reports — Naming and UUID Chains

## Report File Naming Pattern

All reports follow the 4-part pattern:

```
{agent-family}__{uuid-chain}__{YYYY-MM-DD--HH-MM}__{type}.md
```

**Components**:

- `{agent-family}`: Agent name WITHOUT `-checker` suffix (e.g., `docs`, `ayokoding-web`, `plan`)
- `{uuid-chain}`: Execution hierarchy as 6-char hex UUIDs separated by underscores
- `{YYYY-MM-DD--HH-MM}`: UTC+7 timestamp (double dash between date and time)
- `{type}`: Report type (`audit`, `validation`, `fix`)

**Examples**:

```
generated-reports/docs__a1b2c3__2026-01-03--14-30__audit.md
generated-reports/plan__d4e5f6__2026-01-03--15-00__validation.md
generated-reports/ayokoding-facts__a1b2c3_d4e5f6__2026-01-03--16-45__audit.md
```

## UUID Generation

Generate 6-character hexadecimal UUID at agent startup:

```bash
MY_UUID=$(uuidgen | tr '[:upper:]' '[:lower:]' | head -c 6)
# Example output: a1b2c3
```

**Why 6 characters?**

- 16^6 = 16,777,216 combinations
- Collision probability for 1000 parallel executions: ~0.003%
- Short for readability, long enough for uniqueness

## UUID Chain Logic

**Scope-based execution tracking** enables parent-child hierarchy:

**Tracking File Pattern**: `generated-reports/.execution-chain-{scope}`

**Startup Logic**:

```bash
# 1. Generate own UUID
MY_UUID=$(uuidgen | tr '[:upper:]' '[:lower:]' | head -c 6)

# 2. Determine scope (from EXECUTION_SCOPE or default to agent-family)
SCOPE="${EXECUTION_SCOPE:-docs}"

# 3. Read parent chain from scope tracking file
CHAIN_FILE="generated-reports/.execution-chain-${SCOPE}"
if [ -f "$CHAIN_FILE" ]; then
  read PARENT_TIME PARENT_CHAIN < "$CHAIN_FILE"
  CURRENT_TIME=$(date +%s)
  TIME_DIFF=$((CURRENT_TIME - PARENT_TIME))

  # If parent is recent (< 5 min), append to chain
  if [ $TIME_DIFF -lt 300 ]; then
    UUID_CHAIN="${PARENT_CHAIN}_${MY_UUID}"
  else
    UUID_CHAIN="$MY_UUID"  # Start new chain
  fi
else
  UUID_CHAIN="$MY_UUID"  # First execution
fi

# 4. Write own chain to tracking file
echo "$(date +%s) $UUID_CHAIN" > "$CHAIN_FILE"
```

**Chain Examples**:

- `a1b2c3` - Root execution (no parent)
- `a1b2c3_d4e5f6` - Child of a1b2c3
- `a1b2c3_d4e5f6_g7h8i9` - Grandchild (2 levels deep)

## UTC+7 Timestamp Generation

Generate timestamp in UTC+7 timezone:

```bash
TIMESTAMP=$(TZ='Asia/Jakarta' date +"%Y-%m-%d--%H-%M")
# Example output: 2026-01-03--14-30
```

**Format**: `YYYY-MM-DD--HH-MM` (double dash between date and time for filesystem compatibility)
