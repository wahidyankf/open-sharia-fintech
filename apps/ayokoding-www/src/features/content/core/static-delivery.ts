export interface PrerenderManifestLike {
  routes?: Readonly<Record<string, unknown>>;
  dynamicRoutes?: Readonly<Record<string, unknown>>;
}

export const MINIMUM_PRERENDERED_ROUTE_COUNT = 2_000;

export const TRPC_RUNTIME_TRACED_ASSETS = [
  "./content/**/*",
  "./generated/**/*",
  "./src/features/course-paths/manifests/**/*",
] as const;

/** Next.js route policy for locale-scoped content responses. */
export function contentCacheRule() {
  return {
    source: "/:locale(en|id)/:path*",
    headers: [{ key: "Cache-Control", value: "public, max-age=0, must-revalidate" }],
  };
}

export function inspectPrerenderManifest(manifest: PrerenderManifestLike, contentRoute: string) {
  const routes = manifest.routes ?? {};
  return {
    routeCount: Object.keys(routes).length,
    contentRouteIsPrerendered: Object.hasOwn(routes, contentRoute),
    contentCatchAllIsDynamic: Object.hasOwn(manifest.dynamicRoutes ?? {}, "/[locale]/[...slug]"),
  };
}
