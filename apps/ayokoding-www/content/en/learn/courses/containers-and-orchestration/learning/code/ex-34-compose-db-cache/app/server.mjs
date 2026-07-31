import http from "node:http";
import net from "node:net";

const port = Number(process.env.PORT ?? "8080");
const databaseUrl = process.env.DATABASE_URL;
const cacheUrl = process.env.CACHE_URL;
const hasToken = Boolean(process.env.API_TOKEN);

const canConnect = (value) =>
  new Promise((resolve) => {
    if (!value) return resolve(false);

    let url;
    try {
      url = new URL(value);
    } catch {
      return resolve(false);
    }

    const socket = net.connect(Number(url.port), url.hostname);
    socket.setTimeout(1_000);
    socket.once("connect", () => socket.end(() => resolve(true)));
    socket.once("timeout", () => socket.destroy());
    socket.once("error", () => resolve(false));
    socket.once("close", () => resolve(false));
  });

const server = http.createServer(async (request, response) => {
  if (request.url === "/livez") {
    response.writeHead(200).end("live");
    return;
  }

  if (request.url === "/readyz") {
    const [databaseReachable, cacheReachable] = await Promise.all([databaseUrl, cacheUrl].map(canConnect));
    const ready = hasToken && databaseReachable && cacheReachable;
    response.writeHead(ready ? 200 : 503).end(ready ? "database and cache reachable" : "dependency or token missing");
    return;
  }

  response.writeHead(200, { "content-type": "application/json" });
  response.end(
    JSON.stringify({
      databaseConfigured: Boolean(databaseUrl),
      cacheConfigured: Boolean(cacheUrl),
      tokenConfigured: hasToken,
    }),
  );
});

server.listen(port, "0.0.0.0", () => console.log(`listening on ${port}`));
