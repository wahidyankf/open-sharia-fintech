#!/usr/bin/env bash
set -euo pipefail

# beavernest-app-web resolves the workspace package via its own Vite
# `resolve.alias` (see vite.config.ts) rather than a package.json export
# map, so its CSS `@import` uses the resolved relative path instead of the
# bare `@open-sharia-enterprise/web-ui-token` specifier the Next.js apps use.
rg -Fq 'libs/web-ui-token/src/beavernest.css' apps/beavernest-app-web/src/styles.css
rg -Fq 'bootstrapTheme' apps/beavernest-app-web/src/main.tsx
# Scoped to BeaverNest's own sources, not the shared libs/web-ui-token README
# or the general design-tokens governance doc — both legitimately reference
# the Next.js `src/app/globals.css` pattern for the *other*, Next.js-based
# apps (e.g. organiclever-app-web) that also consume this library.
! rg -q 'src/app/globals\.css|next/font|<script[^>]*>.*theme' \
	apps/beavernest-app-web/src libs/web-ui-token/src/beavernest.css
