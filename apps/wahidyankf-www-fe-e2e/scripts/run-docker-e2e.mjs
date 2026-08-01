import { execFileSync, spawnSync } from "node:child_process";
import { randomUUID } from "node:crypto";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const e2eRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const workspaceRoot = resolve(e2eRoot, "../..");
const externalBaseUrl = process.env.BASE_URL;
const imageTag = `ose-public-wahidyankf-e2e:${process.pid}`;
const containerName = `ose-public-wahidyankf-e2e-${randomUUID().slice(0, 12)}`;

const run = (command, args, options = {}) => {
  const output = execFileSync(command, args, {
    cwd: e2eRoot,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "inherit"],
    ...options,
  });
  return typeof output === "string" ? output.trim() : "";
};

const runPlaywright = (baseUrl) => {
  run("npx", ["bddgen"]);
  const result = spawnSync("npx", ["playwright", "test", ...process.argv.slice(2)], {
    cwd: e2eRoot,
    env: { ...process.env, BASE_URL: baseUrl },
    stdio: "inherit",
  });

  if (result.error) throw result.error;
  if (result.status !== 0) process.exitCode = result.status ?? 1;
};

const waitForHealthyContainer = () => {
  for (let attempt = 1; attempt <= 90; attempt += 1) {
    const health = run("docker", ["inspect", "--format", "{{.State.Health.Status}}", containerName]);
    if (health === "healthy") return;
    if (health === "unhealthy") {
      run("docker", ["logs", containerName], { stdio: ["ignore", "inherit", "inherit"] });
      throw new Error(`Docker container ${containerName} became unhealthy.`);
    }
    Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 1000);
  }

  run("docker", ["logs", containerName], { stdio: ["ignore", "inherit", "inherit"] });
  throw new Error(`Docker container ${containerName} did not become healthy within 90 seconds.`);
};

const resolveContainerUrl = () => {
  const publishedPort = run("docker", ["port", containerName, "3201/tcp"]);
  const match = publishedPort.match(/:(\d+)\s*$/m);
  if (!match) throw new Error(`Could not resolve the published port for ${containerName}: ${publishedPort}`);
  return `http://127.0.0.1:${match[1]}`;
};

if (externalBaseUrl) {
  runPlaywright(externalBaseUrl);
} else {
  try {
    run("docker", ["build", "--tag", imageTag, "--file", "apps/wahidyankf-www/Dockerfile", "."], {
      cwd: workspaceRoot,
      stdio: "inherit",
    });
    run("docker", ["run", "--detach", "--rm", "--name", containerName, "--publish", "127.0.0.1::3201", imageTag]);
    waitForHealthyContainer();
    runPlaywright(resolveContainerUrl());
  } finally {
    try {
      run("docker", ["rm", "--force", containerName]);
    } catch {
      // The container uses --rm, so it may already have been removed after a failed start.
    }
    try {
      run("docker", ["image", "rm", "--force", imageTag]);
    } catch {
      // Preserve the test failure when Docker cleanup is unavailable.
    }
  }
}
