# => The build stage supplies Node only to validate the application artifact before it is copied onward.
FROM node:24-alpine AS build
# => A dedicated working directory prevents application files leaking into arbitrary image paths.
WORKDIR /app
# => The app has no package dependencies, so the stage copies only the runnable source artifact.
COPY app/server.mjs ./server.mjs
# => Verify the syntax before the final stage receives the artifact.
RUN node --check server.mjs

# => The runtime stage starts fresh and receives only the verified application artifact plus its Node runtime.
FROM node:24-alpine AS runtime
# => Create a stable unprivileged identity before copying application code.
RUN addgroup -S app && adduser -S -G app -u 10001 app
# => Receive exactly the verified artifact from the named build stage.
COPY --from=build --chown=app:app /app/server.mjs /app/server.mjs
# => Runtime configuration is injected by Compose or Kubernetes.
ENV PORT=8080
# => Drop root before the application process starts.
USER app
# => Document the listener for local tooling; publishing remains a runtime decision.
EXPOSE 8080
# => Exec form forwards signals directly to Node for clean shutdown.
CMD ["node", "/app/server.mjs"]
