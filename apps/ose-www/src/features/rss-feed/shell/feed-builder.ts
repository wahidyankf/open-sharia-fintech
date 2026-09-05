import { serverCaller } from "@/lib/trpc/server";
import { buildFeedResponse } from "../core/feed";

export async function buildFeed(): Promise<Response> {
  const updates = await serverCaller.content.listUpdates();
  return buildFeedResponse(updates);
}
