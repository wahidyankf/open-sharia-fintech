---
description: The inline markdown option format a genuinely non-interactive root emits when no native multiple-choice tool is available.
when_to_use: Use when rendering a grilling question on a root or harness with no native interactive multiple-choice tool.
---

# Markdown Fallback Format

Only a genuinely non-interactive root or harness without a native tool falls back to inline
markdown options emitted to its caller in the following format:

```markdown
**Question**: [Decision to resolve]

- **Option 1 — [Label]**: [Trade-off sentence] _(Recommended — [rationale])_
- **Option 2 — [Label]**: [Trade-off sentence]
- **Option 3 — [Label]**: [Trade-off sentence]
- **Other — type your own answer**: Free-form write-in; the answer is whatever you type (blank
  state). Always present.
- **Chat about this**: Talk the decision through before deciding instead of picking now. Always
  present.
```

The markdown fallback MUST still satisfy Rules 2–5 (2-4 options, trade-offs, one Recommended,
one decision per question).
