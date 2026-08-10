import { fileURLToPath, URL } from "node:url";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      "@open-sharia-enterprise/web-ui": fileURLToPath(new URL("../../libs/web-ui/src/index.ts", import.meta.url)),
      "@open-sharia-enterprise/web-ui-token": fileURLToPath(
        new URL("../../libs/web-ui-token/src/index.ts", import.meta.url),
      ),
    },
  },
  test: {
    name: "unit",
    passWithNoTests: true,
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
    include: ["src/**/*.{test,spec}.{ts,tsx}"],
    testTimeout: 30000,
    hookTimeout: 30000,
    coverage: {
      provider: "v8",
      include: ["src/**/*.{ts,tsx}"],
      exclude: ["src/test/**", "src/main.tsx", "src/generated-contracts/**", "**/*.{test,spec}.{ts,tsx}"],
      thresholds: {
        lines: 90,
        functions: 90,
        branches: 90,
        statements: 90,
      },
      reporter: ["text", "json-summary", "lcov"],
    },
  },
});
