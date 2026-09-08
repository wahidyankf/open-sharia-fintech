---
description: How Rust backends (dotenvy + envy) and TypeScript webs (@t3-oss/env-nextjs + zod) validate required env vars at startup or build time.
when_to_use: Use when wiring up or debugging typed env-var validation for a new Rust backend or Next.js web app.
---

# Startup Validation

## Rust backends — `dotenvy` + `envy`

```rust
#[derive(serde::Deserialize)]
pub struct Config {
    pub database_url: String,               // required; no default
    #[serde(default = "default_port")]
    pub organiclever_be_port: u16,          // optional; typed default
}

impl Config {
    pub fn load() -> Result<Self, envy::Error> {
        dotenvy::dotenv().ok();             // no-op in CI; loads .env.local locally
        envy::from_env::<Config>()
    }
}
```

- `envy` maps struct field `organiclever_be_port` ↔ env var `ORGANICLEVER_BE_PORT` automatically.
- Required fields are non-`Option`, no `#[serde(default)]` — a missing value is a typed error at
  startup naming the field.
- Deps: `dotenvy = "0.15.7"` (exact pin, successor to the unmaintained `dotenv` RUSTSEC-2021-0141),
  `envy = "0.4.2"` (exact pin; last release Jan 2021; advisory-clean; narrow scope).

## TypeScript webs — `@t3-oss/env-nextjs` + `zod`

```typescript
// apps/<app>/src/env.ts
import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";
export const env = createEnv({
  server: {
    OSE_WEB_CONTENT_DIR: z.string().optional(),
    OSE_WEB_SHOW_DRAFTS: z.string().optional(),
  },
  experimental__runtimeEnv: {},
});
```

```typescript
// apps/<app>/next.config.ts — import triggers build-time validation
import "./src/env";
```

- `t3-env` validates at **build time** — a missing required var fails `nx build`, not at runtime.
- `NEXT_PUBLIC_*` client vars are enforced by t3-env's TypeScript types — a client var without the
  prefix is a compile error.
- Deps: `@t3-oss/env-nextjs` (exact pin, `0.12.0`), `zod` (exact pin, `4.0.5`).
