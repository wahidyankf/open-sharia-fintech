import { defineConfig } from "vitest/config";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [tsconfigPaths()],
  test: {
    include: ["tests/integration/**/*.integration.{test,spec}.ts", "tests/integration/**/*.steps.ts"],
    environment: "node",
    testTimeout: 60_000,
    coverage: {
      provider: "v8",
      include: ["src/features/content/shell/index-generator.ts"],
      thresholds: {
        lines: 99,
        functions: 99,
        branches: 90,
        statements: 99,
      },
      reporter: ["text", "json-summary", "lcov"],
      reportsDirectory: "coverage/integration",
    },
  },
});
