# Common Separation Violations

## Common Separation Violations

### Violation 1: Duplicating Educational Content

**FAIL** (docs/explanation/.../golang/):

```markdown
## Variables in Go

Go variables can be declared multiple ways:
var x int = 10
y := 20
```

**Why**: Teaching Go syntax (belongs in AyoKoding)

**PASS** (docs/explanation/.../golang/):

```markdown
**Prerequisite**: Complete [AyoKoding Golang](...)

## Variable Naming in OSE Platform

- Domain entities: ZakatPayment, WaqfDonation
- Repository variables: zakatRepo, waqfRepo
```

**Why**: OSE Platform naming conventions (not syntax tutorial)

### Violation 2: Missing Prerequisite Statement

**FAIL**:

```markdown
# Java

Java is used for...

## Best Practices
```

**Why**: No prerequisite statement

**PASS**:

```markdown
# Java

## Prerequisite Knowledge

**REQUIRED**: Complete [AyoKoding Java learning path](...)

These are OSE Platform-specific style guides, not educational tutorials.
```
