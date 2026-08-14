---
title: "Phase 6: Python Ecosystem (Sequential)"
description: "Phase 6 (full scope only): install Python 3.13+ via pyenv or Homebrew, required for the polyglot demo apps in ose-primer."
when_to_use: "Use when setting up Python for the ose-primer polyglot demo apps under full scope."
---

# Phase 6: Python Ecosystem (Sequential)

**Condition**: `{input.scope} == full`

Required for: polyglot demo apps in ose-primer (extracted 2026-04-18)

## 6.1 Install Python 3.13+

```bash
# macOS (via pyenv, recommended)
brew install pyenv
pyenv install 3.13.5
pyenv global 3.13.5

# Or use Homebrew directly
brew install python@3.13

# Linux
sudo apt-get install -y python3 python3-pip python3-venv
```

The required minimum version is in the `ose-primer` repository's `.python-version` file.

**Success criteria**: `python3 --version` shows a version >= the `.python-version` file.
