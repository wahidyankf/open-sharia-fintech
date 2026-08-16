---
title: "Phase 6: Python Ecosystem (Sequential)"
description: "Phase 6 (full scope only): install Python 3.13+ via pyenv or Homebrew, for optional Python tooling."
when_to_use: "Use when setting up Python under full scope."
---

# Phase 6: Python Ecosystem (Sequential)

**Condition**: `{input.scope} == full`

Required for: optional Python tooling only — this repo ships no Python project today

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

Pin the version in a `.python-version` file alongside any Python project you add.

**Success criteria**: `python3 --version` shows a version >= the `.python-version` file.
