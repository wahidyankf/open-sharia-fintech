/**
 * Step definitions for the BE Status Page feature.
 *
 * Covers: specs/apps/organiclever/app-web/behaviors/health/system-status-be.feature
 *
 * Tests BeStatusPage directly as an async server component rendered in jsdom.
 * Mocks fetch via vi.stubGlobal and env vars via vi.stubEnv.
 */
import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, cleanup } from "@testing-library/react";
import { vi, expect } from "vitest";

// createEnv snapshots process.env at module load time; mock it with a live Proxy
// so that per-scenario vi.stubEnv mutations are visible to the page component.
vi.mock("@/env", () => ({
  env: new Proxy({} as Record<string, string | undefined>, {
    get: (_, key: string) => process.env[key],
  }),
}));

import BeStatusPage, { metadata } from "@/app/system/status/be/page";

const feature = await loadFeature(
  path.resolve(
    __dirname,
    "../../../../../../specs/apps/organiclever/app-web/behaviors/health/system-status-be.feature",
  ),
);

describeFeature(feature, ({ Scenario, AfterEachScenario }) => {
  AfterEachScenario(() => {
    cleanup();
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
  });

  Scenario("BE status page shows Not Configured when env unset", ({ Given, When, Then, And }) => {
    Given("ORGANICLEVER_BE_URL is unset", () => {
      vi.stubEnv("ORGANICLEVER_BE_URL", "");
    });

    When("a visitor requests GET /system/status/be", async () => {
      const jsx = await BeStatusPage();
      render(jsx);
    });

    Then("the response status is 200", () => {
      // Rendered without throwing — component returned JSX successfully
      expect(document.body).toBeTruthy();
    });

    // @covers specs/apps/organiclever/app-web/behaviors/health/system-status-be.feature:BE status page shows Not Configured when env unset
    And('the body contains "Not configured"', () => {
      expect(screen.getByText(/Not configured/i)).toBeInTheDocument();
    });
  });

  Scenario("Backend health-check page is excluded from search indexes", ({ When, Then }) => {
    When("a crawler requests GET /system/status/be", () => {
      // Metadata is emitted server-side by Next.js for this route.
    });

    // @covers specs/apps/organiclever/app-web/behaviors/health/system-status-be.feature:Backend health-check page is excluded from search indexes
    Then("the response declares the page non-indexable", () => {
      expect(metadata.robots).toMatchObject({ index: false });
    });
  });

  Scenario("BE status page shows UP when backend healthy", ({ Given, When, Then, And }) => {
    Given('ORGANICLEVER_BE_URL is "http://be.example.test"', () => {
      vi.stubEnv("ORGANICLEVER_BE_URL", "http://be.example.test");
    });

    And('the backend health endpoint returns 200 with body {"status":"UP"}', () => {
      vi.stubGlobal(
        "fetch",
        vi.fn().mockResolvedValue({
          ok: true,
          json: () => Promise.resolve({ status: "UP" }),
        }),
      );
    });

    When("a visitor requests GET /system/status/be", async () => {
      const jsx = await BeStatusPage();
      render(jsx);
    });

    Then("the response status is 200", () => {
      expect(document.body).toBeTruthy();
    });

    And('the body contains "UP"', () => {
      expect(screen.getByText(/UP\s*—/)).toBeInTheDocument();
    });

    // @covers specs/apps/organiclever/app-web/behaviors/health/system-status-be.feature:BE status page shows UP when backend healthy
    And("the body contains the backend URL", () => {
      expect(screen.getByText(/http:\/\/be\.example\.test/)).toBeInTheDocument();
    });
  });

  Scenario("BE status page shows DOWN when backend unreachable", ({ Given, When, Then, And }) => {
    Given('ORGANICLEVER_BE_URL is "http://be.example.test"', () => {
      vi.stubEnv("ORGANICLEVER_BE_URL", "http://be.example.test");
    });

    And("the backend health endpoint fails with connection refused", () => {
      vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("fetch failed")));
    });

    When("a visitor requests GET /system/status/be", async () => {
      const jsx = await BeStatusPage();
      render(jsx);
    });

    Then("the response status is 200", () => {
      expect(document.body).toBeTruthy();
    });

    And('the body contains "DOWN"', () => {
      expect(screen.getByText(/DOWN/)).toBeInTheDocument();
    });

    And("the body contains the failure reason", () => {
      expect(screen.getByText(/fetch failed/i)).toBeInTheDocument();
    });

    // @covers specs/apps/organiclever/app-web/behaviors/health/system-status-be.feature:BE status page shows DOWN when backend unreachable
    And("no uncaught exception reaches the Next.js error boundary", () => {
      // Component rendered without throwing — no error boundary triggered
      expect(screen.getByRole("main")).toBeInTheDocument();
    });
  });

  Scenario("BE status page shows DOWN when backend times out", ({ Given, When, Then, And }) => {
    Given('ORGANICLEVER_BE_URL is "http://be.example.test"', () => {
      vi.stubEnv("ORGANICLEVER_BE_URL", "http://be.example.test");
    });

    And("the backend health endpoint does not respond within 3 seconds", () => {
      const timeoutError = Object.assign(new Error("TimeoutError: timeout exceeded"), {
        name: "TimeoutError",
      });
      vi.stubGlobal("fetch", vi.fn().mockRejectedValue(timeoutError));
    });

    When("a visitor requests GET /system/status/be", async () => {
      const jsx = await BeStatusPage();
      render(jsx);
    });

    Then("the response status is 200", () => {
      expect(document.body).toBeTruthy();
    });

    And('the body contains "DOWN"', () => {
      expect(screen.getByText(/DOWN/)).toBeInTheDocument();
    });

    // @covers specs/apps/organiclever/app-web/behaviors/health/system-status-be.feature:BE status page shows DOWN when backend times out
    And('the body contains "timeout"', () => {
      expect(screen.getByText(/timeout/i)).toBeInTheDocument();
    });
  });
});
