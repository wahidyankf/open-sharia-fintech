import { spawn, type ChildProcessWithoutNullStreams } from "node:child_process";
import { existsSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { createBdd } from "playwright-bdd";

const { AfterAll } = createBdd();

// A dedicated e2e port, deliberately not the service's default 8303: the suite must not fight a
// developer's `nx run ose-lms-be:dev` session, nor the exploratory-testing step in this same
// delivery unit, both of which hold 8303.
const port = process.env.LMS_E2E_PORT ?? "8403";
const baseUrl = `http://127.0.0.1:${port}`;
const libsDirectory = join(__dirname, "..", "..", "ose-lms-be", "build", "libs");

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

// The jar name carries the project version, so it is discovered rather than hard-coded — a version
// bump must not silently break the suite. `-plain.jar` is Gradle's non-executable companion
// artifact and is excluded explicitly.
function resolveJarPath(): string {
  if (!existsSync(libsDirectory)) {
    throw new Error(
      `ose-lms-be has not been built: ${libsDirectory} does not exist. ` + `Run \`nx run ose-lms-be:build\` first.`,
    );
  }
  const candidates = readdirSync(libsDirectory).filter((name) => name.endsWith(".jar") && !name.endsWith("-plain.jar"));
  const [jarName, ...extra] = candidates;
  if (jarName === undefined || extra.length > 0) {
    throw new Error(
      `expected exactly one bootable jar in ${libsDirectory}, found ${candidates.length}: ` +
        `${candidates.join(", ") || "(none)"}`,
    );
  }
  return join(libsDirectory, jarName);
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

  backend = spawn("java", ["-jar", resolveJarPath()], {
    cwd: process.cwd(),
    env: { ...process.env, OSE_LMS_BE_PORT: port },
    stdio: "pipe",
  });
  backend.stdout.on("data", (chunk: Buffer) => (output += chunk.toString()));
  backend.stderr.on("data", (chunk: Buffer) => (output += chunk.toString()));

  for (let attempt = 0; attempt < 120; attempt += 1) {
    if (await endpointResponds()) return;
    if (backend.exitCode !== null) throw new Error(`ose-lms-be exited during startup:\n${output}`);
    await wait(500);
  }

  throw new Error(`ose-lms-be did not become ready on ${baseUrl}:\n${output}`);
}

export async function ensureBackendStarted() {
  if (!(await endpointResponds())) await startBackend();
}

AfterAll(async () => {
  await stopBackend();
});

process.once("exit", () => {
  if (backend?.exitCode === null) backend.kill("SIGKILL");
});
