/**
 * Runs `dotnet fsi` / `dotnet build` on the Playwright test runner's own
 * machine — never inside the disposable, SDK-less production runtime
 * container (`apps/beavernest-be/Dockerfile`'s `runtime` stage ships only the
 * ASP.NET runtime). The test runner's machine builds and tests the F# app
 * elsewhere in this same Nx pipeline (`nx run beavernest-be:test:unit`,
 * `test:integration`), so the .NET SDK is always present there.
 *
 * Deep SQLite-internals observations (migration journal contents, PRAGMA
 * settings, write contention) talk directly to the host-bind-mounted SQLite
 * files the disposable Compose stack already exposes
 * (`BEAVERNEST_BE_HOST_DATA_DIRECTORY` / `BEAVERNEST_BE_BACKUP_DIRECTORY`),
 * instead of `docker compose exec`-ing a nonexistent SDK inside the running
 * container.
 */
import { execFile } from "node:child_process";
import { cp, mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { promisify } from "node:util";
import { test } from "@playwright/test";

const execFileAsync = promisify(execFile);
const repositoryRoot = resolve(__dirname, "../../..");

const hostDataDirectory = process.env.BEAVERNEST_BE_E2E_DATA_DIRECTORY;
const hostBackupDirectory = process.env.BEAVERNEST_BE_E2E_BACKUP_DIRECTORY;

/** Debug build produced by run-e2e.sh's host-side `dotnet build` step. */
export const hostAssemblyPath = resolve(
  repositoryRoot,
  "apps/beavernest-be/src/BeaverNestBe/bin/Debug/net10.0/BeaverNestBe.dll",
);

export function requireHostRuntimeAccess(): void {
  test.skip(
    hostDataDirectory === undefined ||
      hostDataDirectory === "" ||
      hostBackupDirectory === undefined ||
      hostBackupDirectory === "",
    "requires the host-visible data/backup directories exported by run-e2e.sh",
  );
}

export function hostDataDirectoryPath(): string {
  if (hostDataDirectory === undefined || hostDataDirectory === "") {
    throw new Error("BEAVERNEST_BE_E2E_DATA_DIRECTORY is not set");
  }

  return hostDataDirectory;
}

export function hostDatabasePath(): string {
  return join(hostDataDirectoryPath(), "beavernest.sqlite3");
}

export function hostBackupPath(name: string): string {
  if (hostBackupDirectory === undefined || hostBackupDirectory === "") {
    throw new Error("BEAVERNEST_BE_E2E_BACKUP_DIRECTORY is not set");
  }

  return join(hostBackupDirectory, name);
}

type CommandFailure = Error & {
  code?: number | string;
  stderr?: string;
  stdout?: string;
};

export type HostCommandResult = {
  exitCode: number;
  output: string;
};

/** Executes an F# script with the host machine's own `dotnet fsi`. */
export async function runFsiOnHost(script: string): Promise<string> {
  const workingDirectory = await mkdtemp(join(tmpdir(), "beavernest-e2e-fsi-"));
  const scriptPath = join(workingDirectory, "probe.fsx");
  await writeFile(scriptPath, script, "utf8");

  try {
    const { stdout, stderr } = await execFileAsync("dotnet", ["fsi", "--exec", scriptPath], {
      encoding: "utf8",
    });
    return `${stdout}${stderr}`;
  } catch (error) {
    const failure = error as CommandFailure;
    throw new Error(`dotnet fsi failed:\n${failure.stdout ?? ""}${failure.stderr ?? ""}${failure.message}`);
  } finally {
    await rm(workingDirectory, { recursive: true, force: true });
  }
}

/**
 * Builds an isolated copy of the BeaverNestBe source tree with an
 * intentionally invalid migration script embedded, then runs the resulting
 * binary as a plain host process against a disposable data directory —
 * reproducing the production boot sequence (`Program.prepareApplication`)
 * without ever touching the shared E2E Compose fixture or requiring an SDK
 * inside any container.
 */
export async function bootIsolatedBackendWithBrokenMigration(): Promise<HostCommandResult> {
  const workingDirectory = await mkdtemp(join(tmpdir(), "beavernest-e2e-broken-"));
  const sourceDirectory = join(workingDirectory, "src");
  const dataDirectory = join(workingDirectory, "data");

  try {
    await cp(resolve(repositoryRoot, "apps/beavernest-be/src/BeaverNestBe"), sourceDirectory, {
      recursive: true,
      filter: (source) => !/[/\\](bin|obj)([/\\]|$)/.test(source),
    });
    await writeFile(join(sourceDirectory, "Migrations", "999-e2e-broken.sql"), "not valid SQL\n", "utf8");

    const fsproj = join(sourceDirectory, "BeaverNestBe.fsproj");
    await execFileAsync("dotnet", ["build", fsproj, "--nologo", "-v", "quiet"], { encoding: "utf8" });

    const publishedDll = join(sourceDirectory, "bin", "Debug", "net10.0", "BeaverNestBe.dll");

    try {
      const { stdout, stderr } = await execFileAsync("dotnet", [publishedDll], {
        encoding: "utf8",
        env: {
          ...process.env,
          BEAVERNEST_BE_DATA_DIRECTORY: dataDirectory,
          BEAVERNEST_BE_HTTP_LISTEN_ADDRESS: "127.0.0.1",
          BEAVERNEST_BE_HTTP_LISTEN_PORT: "19398",
          BEAVERNEST_BE_SQLITE_BUSY_TIMEOUT_MILLISECONDS: "1000",
        },
      });
      return { exitCode: 0, output: `${stdout}${stderr}` };
    } catch (error) {
      const failure = error as CommandFailure;
      const exitCode = typeof failure.code === "number" ? failure.code : 1;
      return { exitCode, output: `${failure.stdout ?? ""}${failure.stderr ?? ""}` };
    }
  } finally {
    await rm(workingDirectory, { recursive: true, force: true });
  }
}
