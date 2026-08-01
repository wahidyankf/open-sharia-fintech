import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const appRoot = resolve(import.meta.dirname, "..");
const prerenderManifest = JSON.parse(readFileSync(resolve(appRoot, ".next/prerender-manifest.json"), "utf8"));
const routesManifest = JSON.parse(readFileSync(resolve(appRoot, ".next/routes-manifest.json"), "utf8"));
const publicRoutes = ["/", "/cv", "/personal-projects", "/robots.txt", "/sitemap.xml"];
const prerenderedRoutes = Object.keys(prerenderManifest.routes);
const staticRoutes = routesManifest.staticRoutes.map(({ page }) => page);
const dynamicRoutes = routesManifest.dynamicRoutes.map(({ page }) => page);

function requireRoutes(routes, manifestName) {
  const missingRoutes = publicRoutes.filter((route) => !routes.includes(route));

  if (missingRoutes.length > 0) {
    throw new Error(`${manifestName} is missing static route(s): ${missingRoutes.join(", ")}`);
  }
}

requireRoutes(prerenderedRoutes, "prerender-manifest.json");
requireRoutes(staticRoutes, "routes-manifest.json");

if (dynamicRoutes.length > 0) {
  throw new Error(`routes-manifest.json contains dynamic route(s): ${dynamicRoutes.join(", ")}`);
}

console.log(`Verified static build output for ${publicRoutes.join(", ")}.`);
