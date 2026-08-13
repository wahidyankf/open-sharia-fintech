# Production multi-stage Dockerfile for the combined BeaverNest runtime.
# Build context: repo root (e.g. `docker build -f apps/beavernest-be/Dockerfile .`).

FROM node:24.16.0-alpine3.23@sha256:2bdb65ed1dab192432bc31c95f94155ca5ad7fc1392fb7eb7526ab682fa5bf14 AS frontend-build
WORKDIR /workspace

# The F# OpenAPI generator is a Java CLI. This remains confined to the build
# stage; neither the production runtime nor the Vite client depends on Java.
RUN apk add --no-cache openjdk17-jre-headless

# Keep dependency installation cacheable while retaining the local workspace
# packages required by the Vite client.
COPY package.json package-lock.json nx.json openapitools.json tsconfig.base.json ./
COPY apps/beavernest-app-web/package.json apps/beavernest-app-web/package.json
COPY libs/web-ui/package.json libs/web-ui/package.json
COPY libs/web-ui-token/package.json libs/web-ui-token/package.json
RUN npm ci --workspace=beavernest-app-web --include-workspace-root --ignore-scripts

# Build the contract bundle and generated frontend client from source; the
# final image never relies on a host-generated client or frontend artifact.
COPY specs/apps/beavernest/containers/contracts/ specs/apps/beavernest/containers/contracts/
COPY apps/beavernest-app-web/ apps/beavernest-app-web/
COPY libs/web-ui/ libs/web-ui/
COPY libs/web-ui-token/ libs/web-ui-token/
RUN npx @redocly/cli bundle specs/apps/beavernest/containers/contracts/openapi.yaml \
    -o specs/apps/beavernest/containers/contracts/generated/openapi-bundled.yaml \
  && npx openapi-generator-cli generate \
    -i specs/apps/beavernest/containers/contracts/generated/openapi-bundled.yaml \
    -g fsharp-giraffe-server \
    -o apps/beavernest-be/generated-contracts \
    --model-package BeaverNestBe.Contracts \
    --global-property=models,modelDocs=false,apiDocs=false \
  && npx @hey-api/openapi-ts \
    -i specs/apps/beavernest/containers/contracts/generated/openapi-bundled.yaml \
    -o apps/beavernest-app-web/src/generated-contracts \
    -s
WORKDIR /workspace/apps/beavernest-app-web
RUN VITE_MODE=$([ "${APP_ENV:-local}" = local ] && echo development || echo "${APP_ENV:-local}") \
  && npx vite build --mode "$VITE_MODE"

FROM mcr.microsoft.com/dotnet/sdk:10.0.302-noble@sha256:72dd743782f2ae7e5476fd64f6a460045e3998dc862218b80e6944cba79a01b0 AS backend-build
WORKDIR /src

# Copy the project file first for restore-layer caching.
COPY apps/beavernest-be/global.json apps/beavernest-be/dotnet-tools.json apps/beavernest-be/.editorconfig ./
COPY apps/beavernest-be/src/BeaverNestBe/BeaverNestBe.fsproj apps/beavernest-be/src/BeaverNestBe/
COPY libs/fsharp-env-loader/fsharp-env-loader.fsproj libs/fsharp-env-loader/
RUN dotnet restore apps/beavernest-be/src/BeaverNestBe/BeaverNestBe.fsproj

COPY apps/beavernest-be/src/ apps/beavernest-be/src/
COPY libs/fsharp-env-loader/src/ libs/fsharp-env-loader/src/
COPY --from=frontend-build /workspace/apps/beavernest-be/generated-contracts/OpenAPI/src/BeaverNestBe.Contracts/Health.fs apps/beavernest-be/generated-contracts/OpenAPI/src/BeaverNestBe.Contracts/Health.fs
RUN dotnet publish apps/beavernest-be/src/BeaverNestBe/BeaverNestBe.fsproj \
  --configuration Release \
  --output /app/publish \
  --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:10.0.10-noble@sha256:f1126d438ccc359f51cc6d4701a8deae513856cf10f5fe645d29ea6403dcac6b AS runtime
WORKDIR /app

# curl is required by the compose healthcheck (the aspnet runtime image does not ship it).
RUN apt-get update \
  && apt-get install --no-install-recommends --yes curl \
  && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 10001 beavernest \
  && useradd --uid 10001 --gid 10001 --create-home --shell /usr/sbin/nologin beavernest \
  && install --directory --owner=10001 --group=10001 --mode=0700 /var/lib/beavernest

COPY --from=backend-build --chown=10001:10001 /app/publish/ ./
COPY --from=frontend-build --chown=10001:10001 /workspace/apps/beavernest-app-web/dist/ ./wwwroot/
COPY --chown=10001:10001 --chmod=0755 apps/beavernest-be/scripts/container-entrypoint.sh ./container-entrypoint.sh

ENV DOTNET_RUNNING_IN_CONTAINER=true \
  BEAVERNEST_BE_DATA_DIRECTORY=/var/lib/beavernest \
  BEAVERNEST_BE_HTTP_LISTEN_ADDRESS=0.0.0.0 \
  BEAVERNEST_BE_HTTP_LISTEN_PORT=19300
EXPOSE 19300
USER 10001:10001
ENTRYPOINT ["/app/container-entrypoint.sh"]
CMD ["dotnet", "BeaverNestBe.dll"]
