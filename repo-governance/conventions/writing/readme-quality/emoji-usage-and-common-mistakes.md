---
description: Strategic emoji use guidelines and the five most common README quality mistakes to avoid
when_to_use: Read this when deciding whether to use an emoji, or when reviewing a README draft for recurring quality mistakes.
---

# Emoji Usage and Common Mistakes

## Emoji Usage

**Strategic, Not Excessive**: Use emojis to create visual markers and hierarchy, not decoration.

**Good Uses**:

- Section headers (, ️, , )
- Bullet point categories (, ️, )
- Emphasis on key points (, ️, )

**Avoid**:

- Multiple emojis per line
- Emojis in every sentence
- Decorative-only emojis
- Emojis that don't add meaning

**Accessibility**: Emojis should enhance, not replace, clear text.

## Common Mistakes

### 1. Corporate Speak

**FAIL: Avoid**:

- "leverage synergies"
- "best-in-class solutions"
- "utilize cutting-edge technology"
- "paradigm shift"
- "value proposition"

**PASS: Use Instead**:

- "use" (not "leverage" or "utilize")
- "good/great" (not "best-in-class")
- "new approach" (not "paradigm shift")
- "what you get" (not "value proposition")

### 2. Assumed Knowledge

**FAIL: Bad**:

```markdown
This project uses TBD with CQRS and DDD patterns for maximum scalability.
```

**PASS: Good**:

```markdown
This project follows Trunk Based Development—all development happens on the main branch with small, frequent commits.
```

**Rule**: If you use an acronym, either spell it out or link to explanation on first use.

### 3. Feature Dumping

**FAIL: Bad**:

```markdown
Features:

- Real-time synchronization
- Multi-tenant architecture
- RBAC implementation
- Event sourcing
- CQRS pattern
- Microservices
  [... 20 more features ...]
```

**PASS: Good**:

```markdown
**What You Get**:

- **Real-time collaboration** - Changes sync instantly across your team
- **Multi-organization support** - One installation serves many clients
- **Granular permissions** - Control who can access what

See [Feature Overview](../../features.md) for complete list.
```

**Rule**: Highlight 3-5 key benefits, link to comprehensive feature list.

### 4. Wall of Text

**FAIL: Bad**: Single paragraph with 10+ lines of continuous text

**PASS: Good**: Multiple short paragraphs, each making one point

**Rule**: If a paragraph exceeds 5 lines, break it up or use bullets.

### 5. Missing Context

**FAIL: Bad**:

```markdown
- OJK compliance
- DSN-MUI guidelines
- AAOIFI standards
```

**PASS: Good**:

```markdown
- Indonesian Banking Authority (OJK) - Sharia banking regulations
- National Sharia Board (DSN-MUI) - Islamic finance guidelines
- Accounting standards (AAOIFI) - International Islamic finance
```

**Rule**: Every acronym needs context, not just expansion.
