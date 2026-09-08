---
description: Verification process and worked examples for validating code snippets against real APIs, checking external reference URLs, and confirming LaTeX mathematical notation is correctly formatted.
when_to_use: Use when verifying a code example's API usage, checking whether a cited URL is accessible and accurate, or validating LaTeX math syntax in a document.
---

# Core Validation Methodology — Code Examples, External References, and Mathematical Notation

Continues from [Command Syntax, Feature Existence, and Version Verification](./core-methodology-command-feature-version.md).

## 4. Code Example Validation

**What to Verify:**

- Code snippets use correct language syntax
- Imports/requires are accurate
- Function signatures match actual APIs
- API methods exist and are not deprecated
- Parameter order and types are correct

**Verification Process:**

```
1. Extract code snippet from documentation
2. Identify language and libraries used
3. WebSearch: "[library] [method/API] documentation"
4. WebFetch: Official API documentation
5. Verify:
   - Import paths are correct
   - Function signatures match current API
   - Parameters are in correct order
   - Return types are accurate
```

**Example:**

````
Claim:
```typescript
import { createUser } from '@prisma/client';
const user = await createUser({ name: 'John' });
```

Verification:
1. WebFetch: https://www.prisma.io/docs/reference/api-reference
2. Check: Prisma Client doesn't export `createUser` directly
3. Actual API: `prisma.user.create({ data: { name: 'John' } })`
4. Result: FAIL: Incorrect API usage
````

## 5. External Reference Verification

**What to Verify:**

- URLs are accessible (not 404/403)
- Citations support the claims made
- Documentation sources are current
- Attribution is correct

**Verification Process:**

```
1. Extract cited URLs from documentation
2. WebFetch: Check if URL is accessible (not 404/403)
3. If accessible: Read content to verify it supports the claim
4. If broken: WebSearch to find current URL or alternative source
```

**Example:**

```
Claim: "According to NIST guidelines at [broken URL]..."
Verification:
1. WebFetch: Original URL returns 404
2. WebSearch: "NIST [topic] guidelines"
3. Find: New URL for same guideline
4. Result: URL outdated, suggest replacement
```

## 6. Mathematical Notation Validation

**What to Verify:**

- LaTeX syntax is used for mathematical formulas
- Variables use proper subscripts ($r_f$ not r_f in text)
- Greek letters use LaTeX ($\beta$ not β in formulas)
- Display math uses `$$...$$` with proper spacing
- LaTeX is NOT used inside code blocks or Mermaid diagrams
- All variables are defined after formulas

**Verification Process:**

```
1. Search for mathematical content in markdown
2. Check inline math uses `$...$` delimiters
3. Check display math uses `$$...$$` delimiters
4. Verify LaTeX NOT in code blocks, Mermaid, or ASCII art
5. Confirm variables are defined
```

**Common error pattern:**

```markdown
FAIL: BROKEN - Single $ on its own line:
$
WACC = \frac{E}{V} \times r_e
$

PASS: CORRECT - Use $$:

$$
WACC = \frac{E}{V} \times r_e
$$
```
