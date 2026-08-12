import { existsSync } from "node:fs";
import { join } from "node:path";

/**
 * Vite always auto-loads a bare `.env` and `.env.local` file "in all cases",
 * in addition to whatever mode-specific `.env.<mode>` file it was told to
 * load — see https://vite.dev/guide/env-and-mode. That auto-load is the one
 * place Vite's native env mechanism diverges from this repo's `APP_ENV`
 * loader contract (rule 2: load exactly one tier file). At any tier other
 * than `local`, a stray `.env`/`.env.local` sitting beside the real tier
 * file would silently leak local values into a staging or production build
 * with no signal to the operator — this guard turns that leak into a build
 * failure instead.
 */
const STRAY_ENV_FILENAMES = [".env", ".env.local"] as const;

/** Builds the guard's failure message for a stray `filename` found at `tier`. */
function strayEnvFileMessage(filename: string, tier: string, envDir: string): string {
  return (
    `beavernest-app-web: found a stray "${filename}" in ${envDir} while building at tier "${tier}". ` +
    `Vite auto-loads bare .env/.env.local files at every mode, which would leak into this non-local ` +
    `build. Move its values into .env.${tier} (or delete it) before building at tier "${tier}".`
  );
}

/**
 * Throws when a stray `.env` or `.env.local` file exists in `envDir` while
 * `tier` is not `local`. Call once, at the top of `vite.config.ts`, before
 * Vite resolves its own env files.
 *
 * `tier` is this app's own `APP_ENV` tier concept (`local`/`test`/`stag`/
 * `prod`) — not Vite's `--mode` CLI value, which the local tier remaps to
 * `development` (see `vite-env-guard.test.ts` for why: Vite's `loadEnv()`
 * rejects the literal mode name `"local"`).
 */
export function guardStrayEnvFiles(tier: string, envDir: string): void {
  if (tier === "local") {
    return;
  }

  const strayFilename = STRAY_ENV_FILENAMES.find((filename) => existsSync(join(envDir, filename)));

  if (strayFilename === undefined) {
    return;
  }

  throw new Error(strayEnvFileMessage(strayFilename, tier, envDir));
}
