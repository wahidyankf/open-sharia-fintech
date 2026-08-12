# config — platform-web Gherkin Domain

Scenarios for the OSE Platform website's Next.js `APP_ENV` tier env-file loader
(`apps/ose-www/src/env-loader.ts`), wired as the first import in `next.config.ts`.

## Feature Files

- **[env-tier-loading.feature](./env-tier-loading.feature)** — Tier selection, process-env
  precedence, missing-file tolerance, and the stray auto-loaded env-file guard

## Related

- [Parent gherkin README](../README.md)
