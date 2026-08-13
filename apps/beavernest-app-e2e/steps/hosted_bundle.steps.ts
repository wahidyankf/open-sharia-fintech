import { createServer, type Server } from "node:http";
import type { AddressInfo } from "node:net";

import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";

const { Given, When, Then, After } = createBdd();

type DeploymentVersion = "v1" | "v2";

interface DeploymentProxy {
  readonly root: string;
  close(): Promise<void>;
  mainRequests(): number;
  deploy(version: DeploymentVersion): void;
}

let deploymentProxy: DeploymentProxy | undefined;

After(async () => {
  await deploymentProxy?.close();
  deploymentProxy = undefined;
});

Given("version one of the F# hosted Flutter bundle has been loaded", async ({ page }) => {
  deploymentProxy = await startDeploymentProxy();
  await page.goto(deploymentProxy.root);
  await expect.poll(() => deploymentProxy?.mainRequests()).toBe(1);
});

When("version two is deployed and I navigate normally", async ({ page }) => {
  expect(deploymentProxy).toBeDefined();
  deploymentProxy?.deploy("v2");
  await page.goto(deploymentProxy!.root);
});

Then("the browser loads the coherent version two bundle without a service worker", async ({ page }) => {
  expect(deploymentProxy?.mainRequests()).toBe(2);
  const bundle = await page.request.get(`${deploymentProxy!.root}main.dart.js`);
  expect(bundle.ok()).toBe(true);
  expect(await bundle.text()).toContain("Build v2");
  await expect
    .poll(() => page.evaluate(async () => (await navigator.serviceWorker.getRegistration()) ?? null))
    .toBeNull();
});

Then("un-hashed Flutter entrypoints revalidate before reuse", async ({ page }) => {
  const bootstrap = await page.request.get(`${deploymentProxy!.root}flutter_bootstrap.js`);
  const entrypoint = await page.request.get(`${deploymentProxy!.root}main.dart.js`);

  expect(bootstrap.headers()["cache-control"]).toBe("no-cache");
  expect(entrypoint.headers()["cache-control"]).toBe("no-cache");
});

async function startDeploymentProxy(): Promise<DeploymentProxy> {
  const upstreamRoot = process.env.WEB_BASE_URL || "http://127.0.0.1:19300";
  let deployment: DeploymentVersion = "v1";
  let requestedMainBundle = 0;
  const server = createServer(async (request, response) => {
    const path = request.url || "/";
    const upstream = await fetch(new URL(path, upstreamRoot));
    const headers: Record<string, string> = {};
    upstream.headers.forEach((value, key) => {
      headers[key] = value;
    });
    delete headers["content-length"];
    delete headers["content-encoding"];
    delete headers.etag;
    let body = Buffer.from(await upstream.arrayBuffer());

    if (new URL(path, upstreamRoot).pathname === "/main.dart.js") {
      requestedMainBundle += 1;
      if (deployment === "v1") {
        body = Buffer.from(body.toString().replaceAll("Build v2", "Build v1"));
      }
      headers.etag = `"beavernest-${deployment}"`;
    }
    headers["cache-control"] = "no-cache";
    response.writeHead(upstream.status, headers);
    response.end(body);
  });

  await new Promise<void>((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolve);
  });
  const address = server.address() as AddressInfo;
  return {
    root: `http://127.0.0.1:${address.port}/`,
    mainRequests: () => requestedMainBundle,
    deploy: (version) => {
      deployment = version;
    },
    close: () => closeServer(server),
  };
}

function closeServer(server: Server): Promise<void> {
  return new Promise((resolve, reject) => {
    server.close((error) => (error ? reject(error) : resolve()));
  });
}
