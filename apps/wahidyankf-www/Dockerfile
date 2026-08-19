# Build context: workspace root (../../.. from infra/dev/wahidyankf-www/)
FROM node:24-alpine AS build
WORKDIR /app

# Copy app package.json and strip workspace dependency before install
COPY apps/wahidyankf-www/package.json ./
RUN node -e " \
  const pkg = JSON.parse(require('fs').readFileSync('package.json','utf8')); \
  delete pkg.dependencies['@open-sharia-enterprise/web-ui']; \
  require('fs').writeFileSync('package.json', JSON.stringify(pkg, null, 2)); \
" && npm install --ignore-scripts

# Install web-ui transitive dependencies not already in wahidyankf-www
RUN npm install --save radix-ui@^1.0.0 cmdk@1.1.1 --ignore-scripts

# Copy workspace libs as resolvable node_modules packages
COPY libs/web-ui/src/ ./node_modules/@open-sharia-enterprise/web-ui/src/
COPY libs/web-ui/package.json ./node_modules/@open-sharia-enterprise/web-ui/
COPY libs/web-ui-token/src/ ./node_modules/@open-sharia-enterprise/web-ui-token/src/
COPY libs/web-ui-token/package.json ./node_modules/@open-sharia-enterprise/web-ui-token/

COPY apps/wahidyankf-www/src/ ./src/
COPY apps/wahidyankf-www/public/ ./public/
COPY apps/wahidyankf-www/package.json apps/wahidyankf-www/tsconfig.json apps/wahidyankf-www/next.config.ts apps/wahidyankf-www/postcss.config.mjs ./

ENV NEXT_TELEMETRY_DISABLED=1
RUN npx next build

FROM node:24-alpine

LABEL org.opencontainers.image.source="https://github.com/wahidyankf/ose-public"
LABEL org.opencontainers.image.description="Wahidyan Kresna Fridayoka personal portfolio site built with Next.js"

RUN addgroup -S app && adduser -S app -G app
WORKDIR /app
COPY --from=build --chown=app:app /app/.next ./.next
COPY --from=build --chown=app:app /app/public ./public
COPY --from=build --chown=app:app /app/node_modules ./node_modules
COPY --from=build --chown=app:app /app/package.json ./package.json
COPY --chown=app:app scripts/next-with-port.mjs scripts/next-with-port.mjs
COPY --chown=app:app libs/ts-env-loader/src/port-resolver.ts libs/ts-env-loader/src/port-resolver.ts
USER app
EXPOSE 3201
ENV WAHIDYANKF_WWW_PORT=3201 HOSTNAME="0.0.0.0" NODE_ENV=production NEXT_TELEMETRY_DISABLED=1
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:${WAHIDYANKF_WWW_PORT}/ || exit 1

CMD ["node", "scripts/next-with-port.mjs", "start", "--env", "WAHIDYANKF_WWW_PORT", "--default", "3201", "-H", "0.0.0.0"]
