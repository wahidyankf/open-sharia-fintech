---
title: "Tool Inventory"
description: "Table of all 9 tools checked by rhino-cli doctor, their required versions, version source file, and package manager."
when_to_use: "Use as a quick reference for which tool version a given config file pins, or which manager installs it."
---

# Tool Inventory

All tools checked by `rhino-cli doctor`:

| #   | Tool       | Required Version      | Version Source                                                                                | Manager        |
| --- | ---------- | --------------------- | --------------------------------------------------------------------------------------------- | -------------- |
| 1   | git        | Any                   | (no config file)                                                                              | System/Brew    |
| 2   | volta      | Any                   | (no config file)                                                                              | curl script    |
| 3   | node       | 24.13.1               | package.json > volta.node                                                                     | Volta          |
| 4   | npm        | 11.10.1               | package.json > volta.npm                                                                      | Volta          |
| 5   | golang     | >= go.mod directive   | apps/ayokoding-cli/go.mod                                                                     | Brew/asdf      |
| 6   | dotnet     | >= global.json major  | repo-config.yml > doctor.dotnet-global-json > sdk.version (currently apps/ose-be/global.json) | Brew/Script    |
| 7   | docker     | Any                   | (no config file)                                                                              | Docker Desktop |
| 8   | jq         | Any                   | (no config file)                                                                              | Brew           |
| 9   | playwright | (matches npm version) | node_modules                                                                                  | npx            |
