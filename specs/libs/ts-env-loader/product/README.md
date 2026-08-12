# Product — ts-env-loader

C4 Level 1 product framing for `ts-env-loader`. See
[Specs Directory Structure Convention](../../../../repo-governance/conventions/structure/specs-directory-structure.md)
for the canonical layout.

## Overview

`ts-env-loader` is the shared `APP_ENV` tier env-file loader for the open-sharia-enterprise
monorepo. It implements the repo-wide tier convention's five loader rules — tier selection
(default `"local"`), loading exactly one `.env.<tier>` file, process-env-always-wins precedence, a
missing tier file never being an error, and failing loudly when a stray Next.js-auto-loaded env
file (`.env`, `.env.production`, `.env.local`) would silently coexist with an explicit non-local
tier file.

See [overview.md](./overview.md) for the full product overview.
