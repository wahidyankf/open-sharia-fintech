# HIGH Confidence Checks (Apply Automatically)

This agent re-implements validation checks from `readme-checker` using the EXACT SAME patterns
(consistency is critical). Apply fixes ONLY for objective, verifiable issues.

## 1. Paragraph Length Check

**What to check:** Paragraphs exceeding 5 lines

**Re-validation method:**

```bash
# Count lines in each paragraph (separated by blank lines)
# Flag any paragraph with >5 lines
```

**Confidence:** HIGH (line count is objective)

**Fix:** Split paragraph into multiple shorter paragraphs

## 2. Jargon Pattern Check

**What to check:** Specific jargon terms

**Re-validation method:**

```bash
# Search for exact patterns
grep -i "vendor lock-in\|vendor-neutral\|utilize\|leverage" README.md
```

**Confidence:** HIGH (pattern matching is objective)

**Fix:** Replace with plain language alternatives (see `readme-writing-readme-files` Skill)

## 3. Acronym Context Check

**What to check:** Acronyms without explanation/context

**Re-validation method:**

```bash
# Find acronyms (3-5 uppercase letters)
grep -E '\b[A-Z]{3,5}\b' README.md
# Verify each has context nearby
```

**Confidence:** HIGH (presence of explanation is objective)

**Fix:** Add English-first context per `readme-writing-readme-files` Skill patterns

## 4. Passive Voice Check

**What to check:** Passive voice patterns

**Re-validation method:**

```bash
# Search for passive voice indicators
grep -E "(is|are|was|were|be|been) (controlled|managed|handled|processed|utilized)" README.md
```

**Confidence:** HIGH (pattern matching is objective)

**Fix:** Transform to active voice
