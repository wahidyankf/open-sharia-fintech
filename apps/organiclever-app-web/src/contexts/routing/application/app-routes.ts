export type AppTabId = "home" | "history" | "progress" | "settings";

export interface AppTabRoute {
  readonly id: AppTabId;
  readonly href: `/app/${AppTabId}`;
  readonly label: string;
  readonly icon: string;
}

export const APP_TAB_ROUTES: ReadonlyArray<AppTabRoute> = [
  { id: "home", href: "/app/home", label: "Home", icon: "home" },
  { id: "progress", href: "/app/progress", label: "Progress", icon: "trend" },
  { id: "history", href: "/app/history", label: "History", icon: "history" },
  { id: "settings", href: "/app/settings", label: "Settings", icon: "settings" },
];

export const APP_REDIRECTS = [
  {
    source: "/app",
    destination: "/app/home",
    permanent: true,
  },
] as const;

const DISABLED_ROUTES = new Set(["GET /login", "GET /profile"]);

export interface AppRouteResult {
  readonly status: 200 | 308 | 404;
  readonly path: string;
  readonly screen?: string;
  readonly activeTab?: AppTabId;
  readonly location?: string;
}

/**
 * Application-owned route policy shared by navigation chrome, Next config,
 * and isolated tests. Next remains responsible for turning this policy into
 * browser history and HTTP responses at the public boundary.
 */
export function resolveAppRoute(method: string, path: string): AppRouteResult {
  const redirect = APP_REDIRECTS.find((candidate) => method === "GET" && candidate.source === path);
  if (redirect) return { status: 308, path, location: redirect.destination };

  const tab = APP_TAB_ROUTES.find((candidate) => method === "GET" && candidate.href === path);
  if (tab) return { status: 200, path, screen: tab.label, activeTab: tab.id };

  if (DISABLED_ROUTES.has(`${method} ${path}`) || path.startsWith("/app/")) {
    return { status: 404, path };
  }

  return { status: 404, path };
}

export function refreshAppRoute(path: string): AppRouteResult {
  return resolveAppRoute("GET", path);
}

export function previousAppRoute(history: ReadonlyArray<string>): AppRouteResult {
  return resolveAppRoute("GET", history.at(-2) ?? "/app/home");
}

export function isMainTabPath(path: string | null): boolean {
  return APP_TAB_ROUTES.some((tab) => tab.href === path);
}
