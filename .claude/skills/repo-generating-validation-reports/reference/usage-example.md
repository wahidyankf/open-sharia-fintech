# Validation Reports — Usage Example

## Usage Example

**Checker Agent Startup**:

```bash
# Generate UUID and determine chain
MY_UUID=$(uuidgen | tr '[:upper:]' '[:lower:]' | head -c 6)
SCOPE="${EXECUTION_SCOPE:-docs}"
CHAIN_FILE="generated-reports/.execution-chain-${SCOPE}"

if [ -f "$CHAIN_FILE" ]; then
  read PARENT_TIME PARENT_CHAIN < "$CHAIN_FILE"
  CURRENT_TIME=$(date +%s)
  TIME_DIFF=$((CURRENT_TIME - PARENT_TIME))

  if [ $TIME_DIFF -lt 300 ]; then
    UUID_CHAIN="${PARENT_CHAIN}_${MY_UUID}"
  else
    UUID_CHAIN="$MY_UUID"
  fi
else
  UUID_CHAIN="$MY_UUID"
fi

echo "$(date +%s) $UUID_CHAIN" > "$CHAIN_FILE"

# Generate timestamp
TIMESTAMP=$(TZ='Asia/Jakarta' date +"%Y-%m-%d--%H-%M")

# Create report filename
REPORT_FILE="generated-reports/docs__${UUID_CHAIN}__${TIMESTAMP}__audit.md"

# Initialize report (progressive writing starts here)
cat > "$REPORT_FILE" << 'REPORT_HEADER'
# Validation Report: docs-checker

**Status**: In Progress
**Agent**: docs-checker
**Scope**: Documentation validation
**Timestamp**: [timestamp]
**UUID Chain**: [uuid-chain]

---

## Findings

REPORT_HEADER

# Continue with validation, writing findings progressively...
```
