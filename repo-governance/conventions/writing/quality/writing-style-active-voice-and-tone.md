---
title: "Writing Style: Active Voice and Professional Tone"
description: "When to use active vs passive voice, and how to keep a professional yet approachable tone"
category: explanation
subcategory: conventions
tags:
  - content-quality
  - markdown
  - writing-standards
  - accessibility
  - documentation
created: 2025-12-07
when_to_use: "Read this when reviewing a passage for voice or tone before committing markdown content."
---

# Writing Style: Active Voice and Professional Tone

## Active Voice

**Prefer active voice** over passive voice for clarity and directness.

PASS: **Good (Active Voice)**:

```markdown
The agent validates the content against the convention.
```

FAIL: **Avoid (Passive Voice)**:

```markdown
The content is validated against the convention by the agent.
```

**Exception**: Passive voice is acceptable when:

- The actor is unknown or irrelevant
- Emphasizing the action over the actor
- Scientific or formal contexts require it

**Example of acceptable passive voice**:

```markdown
The configuration file is automatically generated during setup.
```

## Professional Tone

Maintain a **professional yet approachable** tone throughout all content.

**Key Principles**:

- Be respectful and inclusive
- Avoid slang, jargon (unless defined), or colloquialisms
- Use technical terms correctly and consistently
- Assume readers are intelligent but may lack context

PASS: **Good (Professional Tone)**:

```markdown
To configure the authentication system, update the `auth.config.js` file
with your OAuth2 credentials. Refer to the `Authentication Guide`
for detailed instructions.
```

FAIL: **Avoid (Too Casual)**:

```markdown
Just throw your OAuth2 stuff into `auth.config.js` and you're good to go!
```

FAIL: **Avoid (Too Formal/Stuffy)**:

```markdown
It is incumbent upon the developer to ensure proper configuration of the
aforementioned authentication system by means of modifying the designated
configuration file.
```
