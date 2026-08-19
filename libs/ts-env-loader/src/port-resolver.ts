/**
 * The repo-wide runtime port contract, shared by every port-binding app in this repository and
 * mirrored one-for-one by `libs/fsharp-env-loader`'s `PortResolver` module so the TypeScript and
 * F# services resolve their listener port by identical rules.
 *
 * Precedence, highest first:
 *   1. CLI flag  — an explicit `--port` passed at start time.
 *   2. Env var   — the app's own prefixed variable (e.g. `OSE_WWW_PORT`), never a bare `PORT`.
 *                  A prefixed name is what lets one shell hold every app's port at once; see
 *                  `repo-governance/conventions/security/secrets-and-env-standards/naming-standard.md`.
 *   3. Fallback  — the app's compiled-in default, which is also the value documented in
 *                  `docs/reference/web-sites.md`.
 *
 * An empty or whitespace-only value at a tier is treated as absent and falls through to the next
 * tier, matching `./index.ts`'s treatment of an empty `APP_ENV`. A PRESENT but malformed value is a
 * hard error rather than a silent fall-through: a typo'd `--port 80800` must not quietly boot the
 * service on its default port, because the operator asked for something specific and did not get
 * it. That is the same "fail loudly on bad config" posture as the loader's rule 5.
 *
 * THIS MODULE MUST STAY DEPENDENCY-FREE — no `dotenv`, no `node:fs`, nothing outside the language.
 * `scripts/next-with-port.mjs` imports it directly by relative path from inside a built container
 * image, where Next's standalone output has pruned `node_modules` down to what the app traced at
 * build time. `./index.ts` pulls `dotenv`, so importing the port resolver through the package
 * entry point would crash the container at boot. Keeping this file free-standing is what makes the
 * same resolver usable in local development and in the image.
 */

/** A `process.env`-shaped record. Structurally identical to `./index.ts`'s `EnvRecord`, redeclared
 * here so this module imports nothing at all. */
type EnvLike = Record<string, string | undefined>;

const MIN_PORT = 1;
const MAX_PORT = 65535;

export interface ResolvePortOptions {
  /** Value of an explicit `--port` flag, if one was passed. Highest precedence. */
  flag?: string | number | undefined;
  /** Name of this app's prefixed port variable, e.g. `"OSE_WWW_PORT"`. */
  envVar: string;
  /** The app's compiled-in default, used when neither flag nor env var supplies a value. */
  fallback: number;
  /** Record to read `envVar` from. Defaults to `process.env`. */
  env?: EnvLike;
}

/** Treats empty/whitespace-only as absent, so a blank env var falls through instead of erroring. */
function presentValue(value: string | number | undefined): string | undefined {
  if (value === undefined || value === null) {
    return undefined;
  }
  const text = String(value).trim();
  return text.length > 0 ? text : undefined;
}

/** Parses one tier's value, throwing with the tier's name so the error says which knob was wrong. */
function parsePort(text: string, source: string): number {
  // Number() is deliberate over parseInt(): parseInt("3100abc") returns 3100, silently accepting a
  // typo'd value, whereas Number("3100abc") is NaN and gets rejected below.
  const parsed = Number(text);

  if (!Number.isInteger(parsed) || parsed < MIN_PORT || parsed > MAX_PORT) {
    throw new Error(
      `env-loader: ${source} supplied an invalid port "${text}". A port must be an integer ` +
        `between ${MIN_PORT} and ${MAX_PORT}.`,
    );
  }

  return parsed;
}

/**
 * Resolves a listener port by the flag > env var > fallback precedence documented above.
 *
 * @throws if a tier is present but does not hold a valid port number.
 */
export function resolvePort(options: ResolvePortOptions): number {
  const env = options.env ?? process.env;

  const flagValue = presentValue(options.flag);
  if (flagValue !== undefined) {
    return parsePort(flagValue, "--port");
  }

  const envValue = presentValue(env[options.envVar]);
  if (envValue !== undefined) {
    return parsePort(envValue, options.envVar);
  }

  return parsePort(String(options.fallback), `fallback for ${options.envVar}`);
}
