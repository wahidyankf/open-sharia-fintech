# Build-only Vite client stage. The combined backend Dockerfile copies its
# `dist/` output into the ASP.NET static-file directory.
# Build context: workspace root.
FROM node:24.16.0-alpine3.23@sha256:2bdb65ed1dab192432bc31c95f94155ca5ad7fc1392fb7eb7526ab682fa5bf14 AS build
WORKDIR /workspace

COPY package.json package-lock.json nx.json tsconfig.base.json ./
COPY apps/beavernest-app-web/package.json apps/beavernest-app-web/package.json
COPY libs/web-ui/package.json libs/web-ui/package.json
COPY libs/web-ui-token/package.json libs/web-ui-token/package.json
RUN npm ci --workspace=beavernest-app-web --include-workspace-root --ignore-scripts

COPY specs/apps/beavernest/containers/contracts/ specs/apps/beavernest/containers/contracts/
COPY apps/beavernest-app-web/ apps/beavernest-app-web/
COPY libs/web-ui/ libs/web-ui/
COPY libs/web-ui-token/ libs/web-ui-token/
RUN npm exec -- nx run beavernest-contracts:bundle \
  && npm exec -- nx run beavernest-app-web:codegen \
  && npm exec -- nx run beavernest-app-web:build
