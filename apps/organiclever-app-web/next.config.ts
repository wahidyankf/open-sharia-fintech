import "./src/contexts/env-loader/infrastructure/env-loader.ts";
import "./src/env.ts";
import type { NextConfig } from "next";
import path from "node:path";
import { APP_REDIRECTS } from "./src/contexts/routing/application/app-routes";

const nextConfig: NextConfig = {
  output: "standalone",
  // Pin the tracing root explicitly — with two lockfiles visible in the ancestor chain (this
  // repo's own package-lock.json plus a sibling git worktree's copy), Next's automatic
  // lockfile-based root detection is ambiguous and can select the wrong root, nesting the
  // standalone server.js under an unexpected worktree-name subpath.
  outputFileTracingRoot: path.join(__dirname, "../../"),
  transpilePackages: [
    "@open-sharia-enterprise/web-ui",
    "@open-sharia-enterprise/web-ui-token",
    "@t3-oss/env-nextjs",
    "@t3-oss/env-core",
  ],
  images: {
    unoptimized: true,
  },
  // Permanent 308 from /app to /app/home. Implemented at the config level so
  // both dev (`nx dev`) and production builds emit the same HTTP status — the
  // server-component `permanentRedirect()` form returns 200 + RSC payload in
  // dev mode and breaks the e2e redirect-status assertion.
  async redirects() {
    return [...APP_REDIRECTS];
  },
};

export default nextConfig;
