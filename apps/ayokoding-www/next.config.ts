import "./src/env.ts";
import type { NextConfig } from "next";
import path from "node:path";
import { learnReorgRedirects } from "./src/redirects/learn-reorg";
import { courseRehomeRedirects } from "./src/redirects/course-rehome";
import { contentNamespaceRedirects } from "./src/redirects/content-namespace";
import { learnThreeBucketRedirects } from "./src/redirects/learn-three-bucket";

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

const localeEntryRedirects = [
  { source: "/", destination: "/en", permanent: true },
  { source: "/EN", destination: "/en", permanent: true },
  { source: "/En", destination: "/en", permanent: true },
  { source: "/eN", destination: "/en", permanent: true },
  { source: "/ID", destination: "/id", permanent: true },
  { source: "/Id", destination: "/id", permanent: true },
  { source: "/iD", destination: "/id", permanent: true },
  { source: "/EN/:path*", destination: "/en/:path*", permanent: true },
  { source: "/En/:path*", destination: "/en/:path*", permanent: true },
  { source: "/eN/:path*", destination: "/en/:path*", permanent: true },
  { source: "/ID/:path*", destination: "/id/:path*", permanent: true },
  { source: "/Id/:path*", destination: "/id/:path*", permanent: true },
  { source: "/iD/:path*", destination: "/id/:path*", permanent: true },
];

const nextConfig: NextConfig = {
  output: "standalone",
  // Legacy markdown pages can exceed Next's 60s default during the full SSG
  // fan-out; retain static generation instead of retrying them as failures.
  staticPageGenerationTimeout: 180,
  poweredByHeader: false,
  transpilePackages: ["@t3-oss/env-nextjs", "@t3-oss/env-core"],
  outputFileTracingRoot: path.join(__dirname, "../../"),
  outputFileTracingIncludes: {
    "/[locale]/[...slug]": ["./content/**/*", "./generated/**/*"],
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
    // resolve to their canonical domain. courseRehomeRedirects before the six-domain legacy-bucket
    // module last, so its more specific per-course rules win over the broader per-domain wildcard.
    return [
      ...localeEntryRedirects,
      ...contentNamespaceRedirects,
      ...learnReorgRedirects,
      ...courseRehomeRedirects,
      ...learnThreeBucketRedirects,
    ];
  },
};

export default nextConfig;
