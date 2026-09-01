# ts-env-loader — Product Overview

`ts-env-loader` provides the shared `.env.<APP_ENV>` tiered env-file loading logic consumed by the
Next.js apps in the workspace, via one exported function (`loadTierEnv`) and its two
pure helpers (`resolveTier`, `tierEnvFilePath`). It was extracted from six near-identical per-app
copies to close an architecture-review finding about code duplication; five of those apps
(`ayokoding-www`, `organiclever-app-web`, `organiclever-www`, `ose-app-web`, `ose-www`) remain in
this repository.

See [README.md](./README.md) for C4 L1 product framing.
