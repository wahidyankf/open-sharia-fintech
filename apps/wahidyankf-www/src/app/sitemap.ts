import type { MetadataRoute } from "next";

const siteUrl = "https://www.wahidyankf.com";

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: siteUrl, changeFrequency: "monthly", priority: 1 },
    { url: `${siteUrl}/cv`, changeFrequency: "monthly", priority: 0.8 },
    { url: `${siteUrl}/personal-projects`, changeFrequency: "monthly", priority: 0.8 },
  ];
}
