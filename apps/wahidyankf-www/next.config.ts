import "./src/env-loader.ts";
import "./src/env.ts";
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
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
