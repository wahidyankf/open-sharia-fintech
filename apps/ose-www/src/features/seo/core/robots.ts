import type { MetadataRoute } from "next";

export function buildRobots(): MetadataRoute.Robots {
  return {
    rules: [{ userAgent: "*", allow: "/" }],
    sitemap: "https://oseplatform.com/sitemap.xml",
  };
}
