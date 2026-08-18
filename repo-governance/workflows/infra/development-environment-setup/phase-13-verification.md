---
title: "Phase 13: Verification (Sequential)"
description: "Phase 13: verify the pre-commit hook, pre-push gate set, one backend's integration tests, and one backend's E2E tests all work end to end."
when_to_use: "Use as the final smoke test confirming the whole environment setup actually works."
---

# Phase 13: Verification (Sequential)

**Depends on**: All previous phases

## 13.1 Verify pre-commit hook

```bash
# Create a test change and attempt a commit
echo "# test" >> /tmp/test-precommit.md
cp /tmp/test-precommit.md README.md
git add README.md
git commit -m "test: verify pre-commit hook"
# Pre-commit hook should run Prettier, markdownlint, and lint-staged
# Then abort: git reset HEAD~1 && git checkout README.md
git reset HEAD~1
git checkout README.md
```

**Success criteria**: Pre-commit hook runs without errors (Prettier, markdownlint).

## 13.2 Verify pre-push targets (cache warm)

```bash
# Run the same gate set pre-push would run, exactly as .husky/pre-push invokes it
apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push
```

**Success criteria**: Every declared gate passes. This also warms the Nx cache (via the
`test:quick` affected-projects gate) so subsequent pushes are fast. Discover the live gate set
with `apps/rhino-cli/scripts/rhino-bin.sh gate list --surface=pre-push --format=text`.

## 13.3 Verify integration tests (one backend)

```bash
# Pick any backend to validate Docker + PostgreSQL integration
nx run organiclever-be:test:integration
```

**Success criteria**: Integration tests pass. Docker starts PostgreSQL, runs migrations, and
executes Gherkin scenarios against a real database.

**On failure**: Ensure Docker is running (`docker info`). Check for port conflicts on 5432.

## 13.4 Verify E2E tests (one backend)

```bash
# Start a backend
nx run organiclever-be:dev &

# Wait for it to be ready, then run E2E
sleep 5
nx run organiclever-be-e2e:test:e2e

# Stop the backend
kill %1
```

**Success criteria**: Playwright E2E tests pass against the running backend.
