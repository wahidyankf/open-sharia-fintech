---
title: "Phase 8: Elixir/Erlang Ecosystem (Sequential)"
description: "Phase 8 (full scope only): install asdf, then Erlang and Elixir at the versions pinned in .tool-versions."
when_to_use: "Use when setting up Elixir/Erlang for the ose-primer polyglot demo apps under full scope."
---

# Phase 8: Elixir/Erlang Ecosystem (Sequential)

**Condition**: `{input.scope} == full`

Required for: polyglot demo apps in ose-primer (extracted 2026-04-18)

## 8.1 Install asdf version manager

```bash
# macOS
brew install asdf

# Linux
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.15.0
echo '. "$HOME/.asdf/asdf.sh"' >> ~/.bashrc
source ~/.bashrc
```

**Success criteria**: `asdf --version` returns a version string.

## 8.2 Install Erlang

```bash
asdf plugin add erlang
asdf install erlang 27.3

# Set global default
asdf global erlang 27.3
```

The required version is pinned in `.tool-versions` (currently `erlang 27.3`).

**Note**: Erlang compilation requires build dependencies. On macOS: `brew install autoconf
openssl wxwidgets`. On Linux: `sudo apt-get install -y build-essential autoconf libncurses-dev
libssl-dev`.

**Success criteria**: `erl -noshell -eval 'io:format("~s",[erlang:system_info(otp_release)]),halt().'`
shows `27`.

## 8.3 Install Elixir

```bash
asdf plugin add elixir
asdf install elixir 1.19.5-otp-27

# Set global default
asdf global elixir 1.19.5-otp-27
```

The required version is pinned in `.tool-versions` (currently `elixir 1.19.5-otp-27`).

**Success criteria**: `elixir --version` shows Elixir 1.19.5.
