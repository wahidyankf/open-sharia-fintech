import type { MetadataRoute } from "next";
import { serverCaller } from "@/lib/trpc/server";
import { buildSitemapEntries } from "../core/sitemap";

export async function buildSitemap(): Promise<MetadataRoute.Sitemap> {
  const updates = await serverCaller.content.listUpdates();
  return buildSitemapEntries(updates);
}
