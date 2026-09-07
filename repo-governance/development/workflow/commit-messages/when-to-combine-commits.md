---
description: Keep every artifact required to complete one coherent, build-valid, revertible purpose together.
when_to_use: Use when deciding whether related changes across multiple files should land in one commit instead of several.
---

# What Belongs in One Commit

After explicit commit authorization, combine files when they complete one coherent purpose. The
commit must build, make sense in review, and revert safely without a later companion commit.

**Completion artifacts belong together** — include required implementation, tests, documentation,
specifications, references, migrations and rollback, and generated mirrors:

```
PASS: Good:
1. feat(auth): add two-factor authentication
   (includes: auth.js, auth.test.js, auth.md, routes.js)

FAIL: Bad:
1. feat(auth): add auth.js
2. feat(auth): add auth.test.js
3. feat(auth): add auth.md
4. feat(auth): update routes.js
```

**Tightly coupled changes** — changes that do not make sense or would break the build separately:

```
PASS: Good:
1. refactor(api): rename getUserData to fetchUserProfile
   (includes renaming function definition and all call sites)

FAIL: Bad:
1. refactor(api): rename function definition
2. refactor(api): update call sites
   (This would break the build between commits)
```

Do not split merely because files have different extensions, directories, scopes, or Conventional
Commit types. Split only an independently reviewable and revertible concern.
