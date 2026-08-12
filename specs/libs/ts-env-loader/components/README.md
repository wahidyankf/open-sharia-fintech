# Components — ts-env-loader

C4 Level 3 components for `ts-env-loader`.

| Module     | Export            | Purpose                                                                                                                         |
| ---------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `index.ts` | `resolveTier`     | Reads `APP_ENV` from an `EnvRecord`, defaulting to `"local"`                                                                    |
| `index.ts` | `tierEnvFilePath` | Builds the absolute path to a tier's `.env.<tier>` file inside `appDir`                                                         |
| `index.ts` | `loadTierEnv`     | Applies the current tier's file to an `EnvRecord` with process-env-wins semantics, guarding against stray auto-loaded env files |
| `index.ts` | `EnvRecord`       | The `process.env`-shaped record type consumed and populated by the loader                                                       |

See [../behavior/gherkin/env-loader/](../behavior/gherkin/env-loader/) for the behavioral spec.
See [component-ts-env-loader.md](./component-ts-env-loader.md) for the C4 component diagram
placeholder.
