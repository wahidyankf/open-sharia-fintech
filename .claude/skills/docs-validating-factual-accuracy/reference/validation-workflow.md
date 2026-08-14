# Factual Validation — Step-by-Step Validation Workflow

## 1. Identify Claims to Validate

Extract objective, verifiable claims from content:

```markdown
Content: "Install using `npm install --save-deps prettier`"
Claim: npm flag "--save-deps" is valid syntax
Type: Command syntax
```

## 2. Determine Source Priority

Use authoritative sources in priority order:

1. **Official documentation** (docs.npmjs.com, official GitHub repos)
2. **Package registries** (npmjs.com, pypi.org, crates.io)
3. **Official release notes** (CHANGELOG, GitHub releases)
4. **Well-maintained community sources** (Stack Overflow official answers, MDN)

## 3. Execute Web Search

```
WebSearch query: "npm install flags official documentation"
Target: Find official npm CLI documentation
```

## 4. Fetch Authoritative Content

```
WebFetch: https://docs.npmjs.com/cli/v9/commands/npm-install
Extract: List of valid flags and their purposes
```

## 5. Compare and Classify

```
Claim: "--save-deps" flag
Source: Official npm docs list "--save-dev" (NOT "--save-deps")
Classification: [Error]
Confidence: HIGH (official docs contradict claim)
```

## 6. Document Finding

```markdown
**File**: `docs/tutorials/quick-start.md:42`
**Verification**: [Error] - Command syntax incorrect
**Criticality**: CRITICAL - Breaks user quick start experience
**Category**: Factual Error - Command Syntax

**Finding**: Installation command uses incorrect npm flag `--save-deps` (should be `--save-dev`)

**Impact**: Users following tutorial get command error, cannot complete setup

**Recommendation**: Change `npm install --save-deps prettier` to `npm install --save-dev prettier`

**Verification Source**:
Official npm documentation confirms `--save-dev` is correct flag
https://docs.npmjs.com/cli/v9/commands/npm-install

**Confidence**: HIGH
```
