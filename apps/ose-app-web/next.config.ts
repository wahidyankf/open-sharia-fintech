import "./src/env.ts";
import type { NextConfig } from "next";
import path from "node:path";

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
};

export default nextConfig;
