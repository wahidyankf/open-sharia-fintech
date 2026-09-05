/**
 * Wired as the very first import in `next.config.ts`, before `./env.ts`, so every other config
 * module — including `./env.ts`'s `createEnv()` validation — observes the tier file's values.
 *
 * The actual loader logic (tier resolution, stray-file guard, process-env-wins application) lives
 * in `@open-sharia-enterprise/ts-env-loader`, shared across every Next.js app in this repo — see
 * that package for the full contract. This file's only job is the explicit call: a shared library
 * never loads its own tier file on import, so each app must call `loadTierEnv()` itself.
 */
import { loadOrganicLeverWwwEnvironment } from "./environment-bootstrap";

export { loadTierEnv, resolveTier, tierEnvFilePath } from "@open-sharia-enterprise/ts-env-loader";

loadOrganicLeverWwwEnvironment();
