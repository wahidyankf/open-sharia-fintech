/**
 * Loads exactly one `.env.<tier>` file per the repo-wide `APP_ENV` tier convention, selected by
 * `APP_ENV` (default `"local"`). Wired as the very first import in `next.config.ts`, before
 * `./env.ts`, so every other config module — including `./env.ts`'s `createEnv()` validation —
 * observes the tier file's values.
 *
 * Next.js has no `--mode` flag like Vite; this module is the custom stand-in. It also owns one
 * guard Next.js itself doesn't provide: Next's own env loader (`@next/env`) auto-loads a bare
 * `.env`, and in a production build also `.env.production`, IN ADDITION to whatever tier file is
 * explicit here. Left unchecked, that silent extra file would violate rule 2 below, so this
 * module throws if any stray file exists beside the tier file at a non-local tier (the "local"
 * exemption is explained on `assertNoStrayEnvFile` below).
 *
 * `.env.local` is the sharpest of the three: Next.js auto-loads it in EVERY environment, not just
 * production, and that auto-load runs before `next.config.ts` is even evaluated — so its values
 * are already in `process.env` by the time this module's `override: false` call runs, silently
 * winning over an explicit `.env.stag`/`.env.prod` with no error. A developer testing a non-local
 * tier locally (exactly the scenario this guard protects) always has a `.env.local` on disk.
 *
 * The five loader rules (identical across every app in this repo):
 *   1. Tier selector    — read APP_ENV; unset means "local".
 *   2. One file         — load .env.$APP_ENV and no other tier file.
 *   3. Process env wins — a variable already present in the process environment is never
 *                         replaced by a file value.
 *   4. Missing file is not an error — absence is the normal CI case.
 *   5. Fail loudly on required-but-absent config, not on the missing file itself — that's
 *      `./env.ts`'s job (zod validation via `createEnv()`), unchanged by this module.
 */
import { existsSync } from "node:fs";
import path from "node:path";
import dotenv from "dotenv";

const DEFAULT_TIER = "local";

/** Files Next.js auto-loads that must never coexist with an explicit non-local tier file. */
const STRAY_ENV_FILENAMES = [".env", ".env.production", ".env.local"] as const;

/** A `process.env`-shaped record: every entry is a string or absent. */
type EnvRecord = Record<string, string | undefined>;

/** Reads `APP_ENV` from `env`, defaulting to `"local"` (rule 1). */
export function resolveTier(env: EnvRecord): string {
  const tier = env["APP_ENV"];
  return tier && tier.length > 0 ? tier : DEFAULT_TIER;
}

/** Builds the absolute path to `tier`'s env file inside `appDir` (rule 2 — "one file"). */
export function tierEnvFilePath(tier: string, appDir: string): string {
  return path.join(appDir, `.env.${tier}`);
}

/**
 * Throws if a stray auto-loaded env file sits beside the tier file at a non-local tier. Skipped
 * at "local": Next.js auto-loading a bare `.env` alongside an explicit `.env.local` tier file is
 * the one case this convention treats as safe, since local development is never a deploy target.
 */
function assertNoStrayEnvFile(tier: string, appDir: string): void {
  if (tier === DEFAULT_TIER) {
    return;
  }

  for (const strayFilename of STRAY_ENV_FILENAMES) {
    if (existsSync(path.join(appDir, strayFilename))) {
      throw new Error(
        `env-loader: found stray auto-loaded env file "${strayFilename}" beside the tier file for ` +
          `APP_ENV="${tier}". Next.js auto-loads "${strayFilename}" in addition to the explicit ` +
          `tier file, which breaks the "one file per tier" contract. Move its contents into ` +
          `".env.${tier}" and delete "${strayFilename}".`,
      );
    }
  }
}

export interface LoadTierEnvOptions {
  /** Directory containing the tier files. Defaults to `process.cwd()`. */
  appDir?: string;
  /** The process-env-like record to read `APP_ENV` from and load tier values into. Defaults to `process.env`. */
  env?: EnvRecord;
}

/**
 * Loads the current tier's `.env.<tier>` file into `options.env` (default `process.env`),
 * implementing rules 1-4 above.
 */
export function loadTierEnv(options: LoadTierEnvOptions = {}): void {
  const appDir = options.appDir ?? process.cwd();
  const env = options.env ?? process.env;
  const tier = resolveTier(env);

  assertNoStrayEnvFile(tier, appDir);

  // `override: false` is dotenv's default; it's spelled out here so the choice reads as
  // deliberate. Per node_modules/dotenv/lib/main.js's `populate()`, dotenv only overwrites a key
  // already present on the target record when `override === true` — otherwise it leaves an
  // already-set key untouched and only fills in keys the file defines that the target doesn't
  // already have. That is exactly rule 3 ("process env wins"): every key `env` already carries
  // before this call survives unchanged; only unset keys get the tier file's value.
  //
  // A missing tier file is not treated as an error either (rule 4): dotenv's `configDotenv()`
  // catches the file-read failure internally and reports it only via the returned `.error` field
  // — it never throws — so this function doesn't need to special-case a missing file itself.
  //
  // `env` is typed as `EnvRecord` (`string | undefined` values) to match `process.env`; dotenv's
  // own `DotenvPopulateInput` type requires `string` values, so the cast below is necessary. It's
  // safe: dotenv only ever assigns to keys it read as strings from the parsed file, and reads via
  // `hasOwnProperty` (which doesn't care whether an existing value is `undefined`).
  dotenv.config({
    path: tierEnvFilePath(tier, appDir),
    override: false,
    processEnv: env as unknown as Record<string, string>,
  });
}

loadTierEnv();
