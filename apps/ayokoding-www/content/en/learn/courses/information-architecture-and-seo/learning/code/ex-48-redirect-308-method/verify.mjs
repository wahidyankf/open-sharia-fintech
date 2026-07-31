import assert from "node:assert/strict";
import { createServer } from "node:http";

let receivedMethod;
const server = createServer((request, response) => {
  if (request.url === "/source") {
    response.writeHead(308, { location: "/target" });
    response.end();
    return;
  }

  receivedMethod = request.method;
  response.end("ok");
});

await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
const { port } = server.address();

try {
  const response = await fetch(`http://127.0.0.1:${port}/source`, {
    method: "POST",
    body: "order=42",
  });

  assert.equal(response.status, 200);
  assert.equal(receivedMethod, "POST");
  console.log("308 redirect preserved POST method at the target.");
} finally {
  await new Promise((resolve, reject) => server.close((error) => (error ? reject(error) : resolve())));
}
