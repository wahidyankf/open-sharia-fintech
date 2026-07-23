import "./src/env.ts";
import type { NextConfig } from "next";
import path from "node:path";
import { learnReorgRedirects } from "./src/redirects/learn-reorg";
import { courseRehomeRedirects } from "./src/redirects/course-rehome";
import { contentNamespaceRedirects } from "./src/redirects/content-namespace";

const securityHeaders = [
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  {
    key: "Content-Security-Policy",
    value:
      "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://*.googletagmanager.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com https://*.googletagmanager.com https://www.google.com;",
  },
];

const nextConfig: NextConfig = {
  output: "standalone",
  poweredByHeader: false,
  transpilePackages: ["@t3-oss/env-nextjs", "@t3-oss/env-core"],
  outputFileTracingRoot: path.join(__dirname, "../../"),
  outputFileTracingIncludes: {
    "/**": ["./content/**/*", "./generated/**/*"],
  },
  serverExternalPackages: ["flexsearch"],
  images: {
    unoptimized: true,
  },
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: securityHeaders,
      },
    ];
  },
  async redirects() {
    // Temporary intermediate order (Phase 2 of ayokoding-learning-path-01-url-restructure):
    // contentNamespaceRedirects is still forward-direction and stays LAST here. Phase 3.0
    // inverts it in place and moves it to the FRONT of this array (DD-48), and Phase 3.1
    // inserts a fourth learn-three-bucket module right after the middle spread below,
    // converging on [namespace, learn-reorg, course-rehome, learn-three-bucket].
    return [...learnReorgRedirects, ...courseRehomeRedirects, ...contentNamespaceRedirects];
  },
};

export default nextConfig;
