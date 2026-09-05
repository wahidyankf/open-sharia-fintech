---
title: "Anti-Patterns 10-11"
description: "Formatting the entire repo on every commit, mixing test levels."
category: explanation
subcategory: development
tags:
  - anti-patterns
  - quality
  - development
created: 2026-05-12
when_to_use: "Use when reviewing for these two quality anti-patterns."
---

# Anti-Patterns 10-11

## Anti-Pattern 10: Formatting Entire Repo on Every Commit

**Problem**: Pre-commit hook formats all files, not just staged.

**Bad Example:**

```bash
# .husky/pre-commit
prettier --write .  # Formats ALL files (slow!)
git add .           # Stages unintended changes!
```

**Solution:**

```json
// package.json
{
  "lint-staged": {
    "*.md": ["prettier --write"]
  }
}
```

**Rationale:**

- Fast pre-commit (only staged files)
- No unintended changes
- Gradual quality improvement
- Developer-friendly

## Anti-Pattern 11: Mixing Test Levels

**Problem**: Using HTTP dispatch in integration tests, or using a real database in unit tests, conflating what each level is meant to verify.

**Bad Example:**

```rust
// Integration test using HTTP dispatch (wrong for integration level)
#[tokio::test]
async fn create_product() {
    let response = app.oneshot(
        Request::builder().method("POST").uri("/api/products").body(body).unwrap()
    ).await.unwrap();
    assert_eq!(response.status(), StatusCode::CREATED); // HTTP dispatch — belongs in E2E!
}
```

**Solution:**

```rust
// Integration test calling service directly (correct)
#[tokio::test]
async fn create_product() {
    let result = product_service.create(product_data, &real_repo).await;
    assert!(result.is_ok()); // direct call, no HTTP layer
}
```

**Rationale:**

- Integration tests verify persistence and transactions, not HTTP routing
- HTTP contract is verified at E2E level with Playwright
- Mixing levels obscures which concern fails when a test breaks
- Real databases in unit tests make them slow, non-deterministic, and uncacheable

**See**: [Behaviour-Driven Development](../../behaviour-driven-development.md) for the full level definitions and boundaries.
