---
title: "Testing Reproducibility"
description: A verification script that checks Node.js/npm versions and lockfile presence match expectations, runnable in CI.
category: explanation
subcategory: development
tags:
  - development
  - reproducibility
  - volta
  - docker
  - environment
  - dependencies
created: 2025-12-28
when_to_use: Use when writing or wiring an environment-verification script into local dev or CI.
---

# Testing Reproducibility

## Verification Script

**Verify environment matches expectations**:

```typescript
// scripts/verify-environment.ts
import { execSync } from "child_process";
import { existsSync } from "fs";
import pkg from "../package.json";

function getVersion(command: string): string {
  return execSync(command, { encoding: "utf-8" }).trim();
}

function verify() {
  console.log("Verifying environment...\n");

  // Check Node.js version
  const nodeVersion = getVersion("node --version");
  const expectedNode = `v${pkg.volta.node}`;
  if (nodeVersion === expectedNode) {
    console.log(`PASS: Node.js: ${nodeVersion}`);
  } else {
    console.error(`FAIL: Node.js: Expected ${expectedNode}, got ${nodeVersion}`);
    process.exit(1);
  }

  // Check npm version
  const npmVersion = getVersion("npm --version");
  const expectedNpm = pkg.volta.npm;
  if (npmVersion === expectedNpm) {
    console.log(`PASS: npm: ${npmVersion}`);
  } else {
    console.error(`FAIL: npm: Expected ${expectedNpm}, got ${npmVersion}`);
    process.exit(1);
  }

  // Check lockfile exists
  if (existsSync("package-lock.json")) {
    console.log("PASS: package-lock.json exists");
  } else {
    console.error("FAIL: package-lock.json missing");
    process.exit(1);
  }

  console.log("\nPASS: Environment verification passed!");
}

verify();
```

**Run in CI**:

```yaml
- name: Verify environment
  run: npx ts-node scripts/verify-environment.ts
```
