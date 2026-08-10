import { execFile } from "node:child_process";
import { resolve } from "node:path";
import { promisify } from "node:util";
import { expect, test } from "@playwright/test";

const execFileAsync = promisify(execFile);
const repositoryRoot = resolve(__dirname, "../../..");
const backendService = "beavernest-app";
const projectName = process.env.BEAVERNEST_BE_E2E_COMPOSE_PROJECT;
const composeFiles = [
  "-f",
  resolve(repositoryRoot, "infra/dev/beavernest-app/docker-compose.yml"),
  "-f",
  resolve(repositoryRoot, "infra/dev/beavernest-app/docker-compose.ci.yml"),
];
const apiBaseUrl = process.env.API_BASE_URL ?? "http://127.0.0.1:19320";

type CommandResult = {
  exitCode: number;
  output: string;
};

type CommandFailure = Error & {
  code?: number | string;
  stderr?: string;
  stdout?: string;
};

function composeArguments(arguments_: readonly string[]): string[] {
  if (projectName === undefined || projectName === "") {
    throw new Error("the disposable BeaverNest compose runtime is not available");
  }

  return ["compose", "-p", projectName, ...composeFiles, ...arguments_];
}

async function commandResult(command: string, arguments_: readonly string[]): Promise<CommandResult> {
  try {
    const { stdout, stderr } = await execFileAsync(command, arguments_, { encoding: "utf8" });
    return { exitCode: 0, output: `${stdout}${stderr}` };
  } catch (error) {
    const failure = error as CommandFailure;
    const exitCode = typeof failure.code === "number" ? failure.code : 1;
    return { exitCode, output: `${failure.stdout ?? ""}${failure.stderr ?? ""}` };
  }
}

export function requireComposeRuntime(): void {
  test.skip(
    projectName === undefined || projectName === "",
    "requires the disposable backend Compose runtime started by run-e2e.sh",
  );
}

export async function compose(arguments_: readonly string[]): Promise<void> {
  const result = await commandResult("docker", composeArguments(arguments_));
  expect(result.exitCode, result.output).toBe(0);
}

export async function composeResult(arguments_: readonly string[]): Promise<CommandResult> {
  return commandResult("docker", composeArguments(arguments_));
}

export async function runBackendCommand(arguments_: readonly string[]): Promise<void> {
  await compose([
    "exec",
    "-T",
    backendService,
    "dotnet",
    "run",
    "--project",
    "src/BeaverNestBe/BeaverNestBe.fsproj",
    "--",
    ...arguments_,
  ]);
}

export async function runStoppedBackendCommand(arguments_: readonly string[]): Promise<void> {
  await compose([
    "run",
    "--rm",
    "--no-deps",
    backendService,
    "dotnet",
    "run",
    "--project",
    "src/BeaverNestBe/BeaverNestBe.fsproj",
    "--",
    ...arguments_,
  ]);
}

export async function backendShell(script: string): Promise<void> {
  await compose(["exec", "-T", backendService, "sh", "-ceu", script]);
}

export async function stoppedBackendShell(script: string): Promise<void> {
  await compose(["run", "--rm", "--no-deps", backendService, "sh", "-ceu", script]);
}

export async function runFsi(script: string, stopped = false): Promise<string> {
  const encoded = Buffer.from(script, "utf8").toString("base64");
  const command = `printf '%s' '${encoded}' | base64 -d > /tmp/beavernest-e2e-probe.fsx\ndotnet fsi --exec /tmp/beavernest-e2e-probe.fsx\nrm -f /tmp/beavernest-e2e-probe.fsx`;
  const arguments_ = stopped
    ? ["run", "--rm", "--no-deps", backendService, "sh", "-ceu", command]
    : ["exec", "-T", backendService, "sh", "-ceu", command];
  const result = await composeResult(arguments_);
  expect(result.exitCode, result.output).toBe(0);
  return result.output;
}

export async function stopBackend(): Promise<void> {
  await compose(["stop", backendService]);
}

export async function startBackend(): Promise<void> {
  await compose(["up", "-d", backendService]);
  await waitForHealth();
}

export async function waitForHealth(): Promise<void> {
  for (let attempt = 0; attempt < 60; attempt += 1) {
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/health`);
      if (response.status === 200) {
        return;
      }
    } catch {
      // Kestrel is still starting; the bounded retry below is the assertion.
    }

    await new Promise((resolve_) => setTimeout(resolve_, 1_000));
  }

  throw new Error("the restarted disposable backend did not become live");
}

export async function resetBackendData(): Promise<void> {
  await compose(["down", "-v"]);
  await compose(["up", "-d", backendService]);
  await waitForHealth();
}
