import type { MetadataRoute } from "next";
import { buildRobots } from "@/features/seo/core/robots";

export default function robots(): MetadataRoute.Robots {
  return buildRobots();
}
