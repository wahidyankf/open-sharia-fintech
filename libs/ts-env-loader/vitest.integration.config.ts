import { defineConfig } from "vitest/config";
import path from "node:path";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    include: ["tests/integration/**/*.test.{ts,tsx}", "tests/integration/**/*.steps.{ts,tsx}"],
    coverage: {
      include: ["src/index.ts", "src/node-tier-env-port.ts"],
      reportsDirectory: "coverage/integration",
    },
  },
  resolve: {
    alias: {
      "@open-sharia-enterprise/ts-env-loader": path.resolve(__dirname, "src"),
    },
  },
});
