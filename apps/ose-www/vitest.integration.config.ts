import path from "node:path";
import { defineConfig } from "vitest/config";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [tsconfigPaths()],
  test: {
    environment: "node",
    include: ["tests/integration/**/*.steps.ts", "tests/integration/**/*.integration.test.ts"],
    coverage: {
      provider: "v8",
      // Numeric Integration coverage measures the local-resource adapter itself. ContentService
      // stays in mandatory Unit coverage; these scenarios still exercise its real filesystem and
      // prebuilt-index paths through the adapter below.
      include: ["src/features/content/shell/repository-fs.ts"],
      reportsDirectory: "coverage/integration",
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
});
