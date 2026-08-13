import { expect, type APIResponse } from "@playwright/test";
import { expectNoStorageDiagnostics } from "./readiness";

type JsonRecord = Record<string, unknown>;

const exactKeys = (value: JsonRecord, expected: readonly string[]): void => {
  expect(Object.keys(value).sort()).toEqual([...expected].sort());
};

const diagnosticsBody = async (response: APIResponse): Promise<JsonRecord> => {
  const body = (await response.json()) as unknown;
  expect(body).not.toBeNull();
  expect(typeof body).toBe("object");
  expect(Array.isArray(body)).toBeFalsy();
  return body as JsonRecord;
};

const diagnosticsComponents = (body: JsonRecord): JsonRecord => {
  const components = body.components;
  expect(components).not.toBeNull();
  expect(typeof components).toBe("object");
  expect(Array.isArray(components)).toBeFalsy();
  return components as JsonRecord;
};

export async function expectReadyDiagnosticsSnapshot(response: APIResponse, status: string): Promise<void> {
  const body = await diagnosticsBody(response);
  exactKeys(body, ["components", "serverTimeUtc", "status", "uptimeSeconds", "version"]);
  expect(body.status).toBe(status);
  expect(body.version).toMatch(/^\d+\.\d+\.\d+(?:\.\d+)?(?:[-+][0-9A-Za-z.-]+)?$/);
  expect(body.uptimeSeconds).toEqual(expect.any(Number));
  expect(Number.isInteger(body.uptimeSeconds)).toBeTruthy();
  expect(body.uptimeSeconds).toBeGreaterThanOrEqual(0);
  expect(body.serverTimeUtc).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]00:00)$/);
}

export async function expectReadyDiagnosticsComponents(response: APIResponse): Promise<void> {
  const components = diagnosticsComponents(await diagnosticsBody(response));
  exactKeys(components, ["database", "schema"]);
  expect(components).toEqual({ database: "ready", schema: "current" });
}

export async function expectUnavailableDiagnostics(response: APIResponse, status: string): Promise<void> {
  const body = await diagnosticsBody(response);
  exactKeys(body, ["components", "status"]);
  expect(body.status).toBe(status);
  expect(diagnosticsComponents(body)).toEqual({ database: "unavailable", schema: "unknown" });
}

export async function expectUnavailableDiagnosticsDisclosure(response: APIResponse): Promise<void> {
  const body = await diagnosticsBody(response);
  exactKeys(body, ["components", "status"]);
  await expectNoStorageDiagnostics(response);
}
