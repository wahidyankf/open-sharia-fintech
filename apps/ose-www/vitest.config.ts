import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";

const sharedPlugins = [react(), tsconfigPaths()];

export default defineConfig({
  plugins: sharedPlugins,
  test: {
    passWithNoTests: true,
    coverage: {
      provider: "v8",
      include: ["src/**/*.{ts,tsx}"],
      exclude: [
        "src/app/**",
        "src/lib/trpc/client.ts",
        "src/lib/trpc/provider.tsx",
        "src/lib/trpc/server.ts",
        "src/features/content/core/types.ts",
        "src/features/content/core/reader.ts",
        "src/features/content/core/repository.ts",
        "src/features/content/shell/repository-fs.ts",
        "src/features/rss-feed/shell/feed-builder.ts",
        "src/features/seo/shell/sitemap-builder.ts",
        "src/features/seo/shell/metadata.ts",
        "src/features/health/shell/status-page.tsx",
        "src/features/landing/shell/*.tsx",
        "src/features/app-shell/shell/*.tsx",
        "src/features/content/shell/*.tsx",
        "src/features/search/shell/service.ts",
        "src/features/search/shell/search-dialog.tsx",
        "src/features/search/shell/search-provider.tsx",
        "src/features/search/shell/use-search.ts",
        "src/scripts/**",
        "src/test/**",
        "**/*.{test,spec}.{ts,tsx}",
      ],
      thresholds: {
        // Only line coverage is a repository-enforced floor (AC-COVERAGE-01);
        // the `test:unit` Nx target's `--coverage.thresholds.lines=99`
        // flag is the source of truth and overrides this value at
        // invocation time. Functions/branches/statements keep their
        // pre-migration bar — raising them isn't part of this contract.
        lines: 99,
        functions: 80,
        branches: 80,
        statements: 80,
      },
      reporter: ["text", "json-summary", "lcov"],
    },
    // This project has no isolated local-resource boundary, so it owns no Integration runtime.
    projects: [
      {
        plugins: sharedPlugins,
        test: {
          name: "unit",
          include: ["tests/unit/be-steps/**/*.steps.ts", "**/*.unit.{test,spec}.{ts,tsx}"],
          exclude: ["node_modules"],
          environment: "node",
        },
      },
      {
        plugins: sharedPlugins,
        test: {
          name: "unit-fe",
          include: ["tests/unit/fe-steps/**/*.steps.{ts,tsx}"],
          exclude: ["node_modules"],
          environment: "jsdom",
          globals: true,
          setupFiles: ["./src/test/setup.ts"],
        },
      },
    ],
  },
});
