import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    passWithNoTests: true,
    coverage: {
      provider: "v8",
      include: ["src/**/*.{ts,tsx}"],
      exclude: [
        // Next.js route infrastructure — covered by e2e, not unit tests
        "src/app/layout.tsx",
        "src/app/**/page.tsx",
        "src/app/api/**",
        "src/proxy.ts",
        "src/test/**",
        "src/generated-contracts/**",
        "**/*.{test,spec}.{ts,tsx}",
        "**/*.stories.{ts,tsx}",
      ],
      thresholds: {
        // Only line coverage is a repository-enforced floor (AC-COVERAGE-01);
        // the `test:coverage` Nx target's `--coverage.thresholds.lines=99`
        // flag is the source of truth and overrides this value at
        // invocation time. Functions/branches/statements keep their
        // pre-migration bar — raising them isn't part of this contract.
        lines: 99,
        functions: 70,
        branches: 70,
        statements: 70,
      },
      reporter: ["text", "json-summary", "lcov"],
    },
    // There is no separate "integration" tier here: the canonical registry
    // (repo-config.yml testing.projects[ose-app-web].behavior.adapters.
    // integration) declares that disposition `inapplicable` — no isolated
    // local-resource boundary — so the former "integration" vitest project
    // matched zero files and `test:integration` is (correctly) a no-op.
    include: ["tests/unit/**/*.test.{ts,tsx}", "tests/unit/**/*.steps.{ts,tsx}"],
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
    testTimeout: 30000,
    hookTimeout: 30000,
  },
});
