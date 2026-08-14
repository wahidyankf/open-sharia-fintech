---
title: "Quick Start: `doctor --fix`"
description: "The fast path: clone, npm install, then npm run doctor -- --fix to auto-install every missing tool for your platform."
when_to_use: "Use when you already have Homebrew/apt and Node.js/npm and want the one-command setup instead of manual phases."
---

# Quick Start: `doctor --fix`

If you already have Homebrew (macOS) or apt (Linux) and Node.js/npm installed:

```bash
git clone https://github.com/wahidyankf/ose-public.git
cd open-sharia-enterprise
npm install
npm run doctor -- --fix          # Auto-install all missing tools
npm run doctor -- --fix --dry-run  # Preview what would be installed (no changes)
```

`doctor --fix` detects your platform (macOS or Linux) and uses the appropriate package
manager for each tool. It is idempotent — running it when all tools are installed is a no-op.

For manual step-by-step installation, follow the phases below.
