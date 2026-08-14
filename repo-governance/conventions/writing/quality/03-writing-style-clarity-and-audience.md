---
title: "Writing Style: Clarity, Conciseness, and Audience Awareness"
description: "Writing clearly with minimal words and adjusting complexity for beginner vs advanced audiences"
category: explanation
subcategory: conventions
tags:
  - content-quality
  - markdown
  - writing-standards
  - accessibility
  - documentation
created: 2025-12-07
when_to_use: "Read this when a passage reads as wordy or vague, or when unsure how much to explain for the target audience."
---

# Writing Style: Clarity, Conciseness, and Audience Awareness

## Clarity and Conciseness

**Write clearly and concisely** - say what you mean with minimal words.

**Guidelines**:

- **One idea per sentence** - Complex ideas need multiple sentences
- **Short paragraphs** - 3-5 sentences maximum for web readability
- **Remove filler words** - "basically", "actually", "just", "simply"
- **Use concrete examples** - Show, don't just tell
- **Define acronyms** - First use should be spelled out

PASS: **Good (Clear and Concise)**:

````markdown
The API returns a JSON response with status code 200 on success.

```json
{
  "status": "success",
  "data": { ... }
}
```
````

````

FAIL: **Avoid (Wordy and Vague)**:

```markdown
Basically, what happens is that when the API call actually completes
successfully, it will simply return back a JSON-formatted response that
contains the status code of 200, which indicates success.
````

## Audience Awareness

**Know your audience** and write for their experience level.

**For Beginners**:

- Explain concepts before using them
- Provide step-by-step instructions
- Include more examples and visuals
- Define technical terms

**For Intermediate/Advanced**:

- Assume foundational knowledge
- Focus on nuances and edge cases
- Provide links to prerequisites instead of explaining basics
- Use technical terminology appropriately

**Example (Tutorial for Beginners)**:

```markdown
## What is an API?

An API (Application Programming Interface) is a way for two programs to
communicate with each other. Think of it like a waiter in a restaurant:
you (the client) tell the waiter (the API) what you want, and the waiter
brings your order from the kitchen (the server).

In this tutorial, we'll build a simple API that responds to requests...
```

**Example (Reference for Advanced)**:

```markdown
## API Authentication

Endpoint authentication uses OAuth 2.0 authorization code flow with PKCE.
Token lifetime: 3600s (configurable via `TOKEN_EXPIRY` env var).
Refresh tokens supported with sliding expiration.
```
