# ts-env-loader — Product Overview

`ts-env-loader` provides the shared `.env.<APP_ENV>` tiered env-file loading logic consumed by
every Next.js and Vite app in the workspace, via one exported function (`loadTierEnv`) and its two
pure helpers (`resolveTier`, `tierEnvFilePath`). It was extracted from six near-identical per-app
copies (`ayokoding-www`, `organiclever-app-web`, `organiclever-www`, `ose-app-web`, `ose-www`,
`wahidyankf-www`) to close an architecture-review finding about code duplication.

See [README.md](./README.md) for C4 L1 product framing.
