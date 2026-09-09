import { spawn, type ChildProcessWithoutNullStreams } from "node:child_process";
import { createBdd } from "playwright-bdd";

const { AfterAll } = createBdd();

const port = "8402";
const baseUrl = `http://127.0.0.1:${port}`;
const binary = "../roots-be/dist/roots-be";
let backend: ChildProcessWithoutNullStreams | undefined;
let output = "";

const wait = (milliseconds: number) => new Promise((resolve) => setTimeout(resolve, milliseconds));

async function endpointResponds(path = "/api/v1/health") {
  try {
    const response = await fetch(`${baseUrl}${path}`);
    return response.ok;
  } catch {
    return false;
  }
}

export async function stopBackend() {
  if (!backend) return;

  const processToStop = backend;
  backend = undefined;

  if (processToStop.exitCode === null) {
    processToStop.kill("SIGTERM");
    await Promise.race([
      new Promise<void>((resolve) => processToStop.once("exit", () => resolve())),
      wait(5_000).then(() => {
        if (processToStop.exitCode === null) processToStop.kill("SIGKILL");
      }),
    ]);
  }

  for (let attempt = 0; attempt < 20 && (await endpointResponds()); attempt += 1) {
    await wait(100);
  }
}

export async function startBackend() {
  await stopBackend();
  output = "";

  // The compiled binary, not `go run`: `go run` forks a child and reports the wrapper's exit code,
  // so a service that dies on startup would look alive to the harness. run-e2e.sh builds it first.
  backend = spawn(binary, [], {
    cwd: process.cwd(),
    env: { ...process.env, ROOTS_BE_PORT: port },
    stdio: "pipe",
  });
  backend.stdout.on("data", (chunk: Buffer) => (output += chunk.toString()));
  backend.stderr.on("data", (chunk: Buffer) => (output += chunk.toString()));

  for (let attempt = 0; attempt < 120; attempt += 1) {
    if (await endpointResponds()) return;
    if (backend.exitCode !== null) throw new Error(`roots-be exited during startup:\n${output}`);
    await wait(250);
  }

  throw new Error(`roots-be did not become ready:\n${output}`);
}

export async function ensureBackendStarted() {
  // Reuse only a process this harness started and is still running. Reusing *whatever* answers on
  // the port -- the shape apps/ose-be-e2e uses -- means a stale binary left over from an earlier
  // `nx run roots-be:dev` silently satisfies every scenario, and the suite passes without ever
  // executing the code under test. That is not a hypothetical: it happened while this suite was
  // being written, and a deliberately broken health handler still reported three green scenarios.
  if (backend && backend.exitCode === null) return;

  if (await endpointResponds()) {
    throw new Error(
      `something is already listening on ${baseUrl} that this suite did not start. ` +
        `E2E must observe the process it launched, so refusing to run against it. ` +
        `Stop the stray process and re-run.`,
    );
  }

  await startBackend();
}

AfterAll(async () => {
  await stopBackend();
});

process.once("exit", () => {
  if (backend?.exitCode === null) backend.kill("SIGKILL");
});
