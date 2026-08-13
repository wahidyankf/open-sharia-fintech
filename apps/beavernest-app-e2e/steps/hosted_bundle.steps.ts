import { createServer, type Server } from "node:http";
import type { AddressInfo } from "node:net";

import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";

const { Given, When, Then, After } = createBdd();

type DeploymentVersion = "v1" | "v2";

interface DeploymentProxy {
  readonly root: string;
  close(): Promise<void>;
  bootstrapRequests(version: DeploymentVersion): number;
  applicationBundleRequests(version: DeploymentVersion): number;
  entrypointCacheControls(version: DeploymentVersion): readonly string[];
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
  await expect.poll(() => deploymentProxy?.bootstrapRequests("v1")).toBe(1);
  await expect.poll(() => deploymentProxy?.applicationBundleRequests("v1")).toBeGreaterThan(0);
});

When("version two is deployed and I navigate normally", async ({ page }) => {
  expect(deploymentProxy).toBeDefined();
  deploymentProxy?.deploy("v2");
  await page.goto(deploymentProxy!.root);
});

Then("the browser loads the coherent version two bundle without a service worker", async ({ page }) => {
  await expect.poll(() => deploymentProxy?.bootstrapRequests("v2")).toBe(1);
  await expect.poll(() => deploymentProxy?.applicationBundleRequests("v2")).toBeGreaterThan(0);
  await expect
    .poll(() => page.evaluate(async () => (await navigator.serviceWorker.getRegistration()) ?? null))
    .toBeNull();
});

Then("un-hashed Flutter entrypoints revalidate before reuse", async () => {
  const cacheControls = deploymentProxy?.entrypointCacheControls("v2") ?? [];

  // These are the responses the second, ordinary browser navigation consumed.
  // Do not issue API-request-context fetches here: those would prove only that
  // a test client can obtain the asset, not that the deployed Flutter loader
  // revalidated it after the deployment changed.
  expect(cacheControls.length).toBeGreaterThan(1);
  expect(cacheControls).toEqual(expect.arrayContaining(["no-cache"]));
  expect(cacheControls.every((value) => value === "no-cache")).toBe(true);
});

async function startDeploymentProxy(): Promise<DeploymentProxy> {
  const upstreamRoot = process.env.WEB_BASE_URL || "http://127.0.0.1:19300";
  let deployment: DeploymentVersion = "v1";
  const requests = new Map<DeploymentVersion, EntrypointRequest[]>([
    ["v1", []],
    ["v2", []],
  ]);
  const server = createServer(async (request, response) => {
    const path = request.url || "/";
    const pathname = new URL(path, upstreamRoot).pathname;
    const upstream = await fetch(new URL(path, upstreamRoot));
    const headers: Record<string, string> = {};
    upstream.headers.forEach((value, key) => {
      headers[key] = value;
    });
    delete headers["content-length"];
    delete headers["content-encoding"];
    delete headers.etag;
    let body: Buffer<ArrayBufferLike> = Buffer.from(await upstream.arrayBuffer());

    if (isFlutterEntrypoint(pathname)) {
      requests.get(deployment)?.push({
        path: pathname,
        cacheControl: upstream.headers.get("cache-control"),
      });
      headers.etag = `"beavernest-${deployment}-${pathname}"`;

      // Flutter selects JavaScript or Wasm at runtime. Keep the compiled
      // response bodies distinguishable without changing their byte length,
      // so both renderer paths remain executable while the proxy models a
      // deployment.
      if (deployment === "v1" && isApplicationBundle(pathname)) {
        body = replaceAscii(body, "Build v2", "Build v1");
      }
    }
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
    bootstrapRequests: (version) => requestsFor(requests, version, isBootstrap).length,
    applicationBundleRequests: (version) => requestsFor(requests, version, isApplicationBundle).length,
    entrypointCacheControls: (version) =>
      requestsFor(requests, version, isFlutterEntrypoint).flatMap((request) =>
        request.cacheControl === null ? [] : [request.cacheControl],
      ),
    deploy: (version) => {
      deployment = version;
    },
    close: () => closeServer(server),
  };
}

interface EntrypointRequest {
  readonly path: string;
  readonly cacheControl: string | null;
}

const bootstrapPath = "/flutter_bootstrap.js";
const applicationBundlePaths = new Set(["/main.dart.js", "/main.dart.mjs", "/main.dart.wasm"]);

function isBootstrap(path: string): boolean {
  return path === bootstrapPath;
}

function isApplicationBundle(path: string): boolean {
  return applicationBundlePaths.has(path);
}

function isFlutterEntrypoint(path: string): boolean {
  return isBootstrap(path) || isApplicationBundle(path);
}

function requestsFor(
  requests: ReadonlyMap<DeploymentVersion, readonly EntrypointRequest[]>,
  version: DeploymentVersion,
  predicate: (path: string) => boolean,
): readonly EntrypointRequest[] {
  return (requests.get(version) ?? []).filter((request) => predicate(request.path));
}

function replaceAscii(body: Buffer<ArrayBufferLike>, from: string, to: string): Buffer<ArrayBufferLike> {
  const source = Buffer.from(from, "ascii");
  const replacement = Buffer.from(to, "ascii");

  if (source.length !== replacement.length) {
    throw new Error("Deployment markers must have equal byte lengths");
  }

  const result = Buffer.from(body);

  for (let offset = result.indexOf(source); offset !== -1; offset = result.indexOf(source, offset + source.length)) {
    replacement.copy(result, offset);
  }

  return result;
}

function closeServer(server: Server): Promise<void> {
  return new Promise((resolve, reject) => {
    server.close((error) => (error ? reject(error) : resolve()));
  });
}
