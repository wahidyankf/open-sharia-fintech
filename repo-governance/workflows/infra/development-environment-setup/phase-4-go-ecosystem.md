---
description: "Phase 4: install Go and Lua solely so gofmt and stylua can format the AyoKoding course corpora."
when_to_use: "Use when setting up or verifying the Go and Lua toolchains needed by the formatter gates."
---

# Phase 4: Go and Lua Formatter Toolchains (Sequential)

No application or library in `apps/` or `libs/` is written in Go or Lua. Both toolchains exist for
exactly one reason: the `*.go` and `*.lua` course corpora under
`apps/ayokoding-www/content/**` must stay formatted, and the `format-gofmt` /
`format-verify-gofmt` and `format-stylua` / `format-verify-stylua` gates in `repo-config.yml`
enforce that at pre-commit and in CI.

`rhino-cli doctor` does not check either tool — `doctor --fix` will not install them. Skip this
phase entirely if you never touch course code.

## 4.1 Install Go

```bash
# macOS
brew install go

# Linux — download from https://go.dev/dl/
```

No `go.mod` pins a version; any current Go release is fine, because only `gofmt` is invoked.

**Success criteria**: `gofmt --help` runs without error.

## 4.2 Install Lua formatting

```bash
# macOS
brew install stylua

# Linux — download a release binary from https://github.com/JohnnyMorganz/StyLua/releases
```

Lua itself is not required; only the `stylua` formatter is.

**Success criteria**: `stylua --version` returns a version string.
