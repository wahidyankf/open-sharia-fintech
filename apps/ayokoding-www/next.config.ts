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
    // Order is load-bearing (DD-48, re-derived from first principles): contentNamespaceRedirects
    // FIRST so any stale /c/-prefixed request is stripped to its bare form before any other rule
    // evaluates — a rule positioned after it would never see a /c/-prefixed URL, since bare-only
    // rules can't match one. learnReorgRedirects next so historical within-/en/learn/ renames
    // resolve to their canonical domain. courseRehomeRedirects before learnThreeBucketRedirects so
    // the more specific per-course rules win over the six-domain bucket rules.
    return [...contentNamespaceRedirects, ...learnReorgRedirects, ...courseRehomeRedirects];
  },
};

export default nextConfig;
