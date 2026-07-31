import http from "node:http";
import net from "node:net";

// => Docker and Kubernetes both inject configuration at runtime, not at image-build time.
const port = Number(process.env.PORT ?? "8080");
// => This value comes from Compose/Kubernetes configuration and is safe to return for verification.
const message = process.env.APP_MESSAGE ?? "containers capstone";
// => A secret is only tested for presence; the service never logs or returns its value.
const hasToken = Boolean(process.env.API_TOKEN);
// => Compose service DNS and Kubernetes Service DNS are consumed as actual TCP endpoints.
const databaseUrl = process.env.DATABASE_URL;
const cacheUrl = process.env.CACHE_URL;

const canConnect = (value) =>
  new Promise((resolve) => {
    if (!value) return resolve(false);
    const url = new URL(value);
    const socket = net.connect(Number(url.port), url.hostname);
    socket.setTimeout(1_000);
    socket.once("connect", () => socket.end(() => resolve(true)));
    socket.once("timeout", () => socket.destroy());
    socket.once("error", () => resolve(false));
    socket.once("close", () => resolve(false));
  });

// => One small server keeps the capstone focused on packaging and orchestration rather than framework APIs.
const server = http.createServer(async (request, response) => {
  // => Liveness answers whether the event loop can serve a request at all.
  if (request.url === "/livez") {
    response.writeHead(200).end("live");
    return;
  }

  // => Compose checks injected dependencies; Kubernetes may omit the local-only DB and cache URLs.
  if (request.url === "/readyz") {
    const dependencyReady = await Promise.all([databaseUrl, cacheUrl].filter(Boolean).map(canConnect));
    const ready = hasToken && dependencyReady.every(Boolean);
    response.writeHead(ready ? 200 : 503).end(ready ? message : "dependency or token missing");
    return;
  }

  // => The ordinary route makes the Service and Ingress testable after readiness succeeds.
  response.writeHead(200, { "content-type": "application/json" });
  response.end(
    JSON.stringify({
      message,
      tokenConfigured: hasToken,
      databaseConfigured: Boolean(databaseUrl),
      cacheConfigured: Boolean(cacheUrl),
    }),
  );
});

// => Binding to all interfaces is necessary inside a container network namespace.
server.listen(port, "0.0.0.0", () => console.log(`listening on ${port}`));
