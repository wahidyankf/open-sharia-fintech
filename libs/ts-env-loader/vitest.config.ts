import { defineConfig } from "vitest/config";
import path from "path";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    include: ["src/**/*.test.{ts,tsx}", "src/**/*.steps.{ts,tsx}"],
  },
  resolve: {
    alias: {
      "@open-sharia-enterprise/ts-env-loader": path.resolve(__dirname, "src"),
    },
  },
});
