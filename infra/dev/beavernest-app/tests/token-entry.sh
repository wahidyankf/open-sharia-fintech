#!/usr/bin/env bash
set -euo pipefail

rg -Fq '@open-sharia-enterprise/web-ui-token/src/beavernest.css' apps/beavernest-app-web/src/styles.css
rg -Fq 'bootstrapTheme' apps/beavernest-app-web/src/main.tsx
! rg -q 'src/app/globals\.css|next/font|<script[^>]*>.*theme' \
	libs/web-ui-token/README.md repo-governance/development/frontend/design-tokens.md libs/web-ui-token/src/beavernest.css
