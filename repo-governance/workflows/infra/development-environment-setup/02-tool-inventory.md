---
title: "Tool Inventory"
description: "Table of every tool rhino-cli doctor checks, its required version, version source file, and package manager."
when_to_use: "Use as a quick reference for which tool version a given config file pins, or which manager installs it."
---

# Tool Inventory

All tools checked by `rhino-cli doctor`, in the order it reports them:

| #   | Tool           | Required Version      | Version Source                               | Manager        |
| --- | -------------- | --------------------- | -------------------------------------------- | -------------- |
| 1   | git            | Any                   | (no config file)                             | System/Brew    |
| 2   | volta          | Any                   | (no config file)                             | curl script    |
| 3   | node           | Exact                 | package.json → volta.node                    | Volta          |
| 4   | npm            | Exact                 | package.json → volta.npm                     | Volta          |
| 5   | rust           | Exact                 | apps/rhino-cli/rust-toolchain.toml → channel | rustup         |
| 6   | cargo-llvm-cov | Any                   | (no config file)                             | cargo install  |
| 7   | dotnet         | >= global.json major  | repo-config.yml → doctor.dotnet-global-json  | Brew/Script    |
| 8   | docker         | Any                   | (no config file)                             | Docker Desktop |
| 9   | jq             | Any                   | (no config file)                             | Brew           |
| 10  | shellcheck     | Any                   | (no config file)                             | Brew/apt       |
| 11  | hadolint       | Any                   | (no config file)                             | Brew/binary    |
| 12  | actionlint     | Any                   | (no config file)                             | Brew/binary    |
| 13  | playwright     | (matches npm version) | node_modules (npx playwright)                | npx            |
| 14  | shfmt          | Any                   | (no config file)                             | Brew/apt       |
| 15  | tofu           | >= pinned floor       | rhino-cli constant (`OPENTOFU_VERSION`)      | Brew/binary    |
| 16  | clang-format   | Any                   | (no config file)                             | Brew/apt       |

**Not checked by doctor**: the toolchains that exist only to format the AyoKoding course corpora —
Go (`gofmt`), Lua (`stylua`), Python (`ruff`), and Elixir (`mix format`). They are installed by
hand in Phases 4, 6, and 8, and enforced by their own `format-*` gates in `repo-config.yml`.
`doctor --fix` will not install them.
