import { fileURLToPath, URL } from "node:url";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import { guardStrayEnvFiles } from "./src/vite-env-guard";

// Rule 1 of the repo's APP_ENV loader contract — the tier selector: reads
// APP_ENV (default "local"). Read directly from process.env rather than
// Vite's own resolved `mode`, because the local tier is remapped to Vite's
// "development" mode name by the Nx target commands (see
// src/vite-env-guard.test.ts for why) — the guard needs this app's own tier
// concept, not Vite's post-remap mode string.
const tier = process.env.APP_ENV ?? "local";

guardStrayEnvFiles(tier, process.cwd());

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      "@open-sharia-enterprise/web-ui": fileURLToPath(new URL("../../libs/web-ui/src/index.ts", import.meta.url)),
      "@open-sharia-enterprise/web-ui-token": fileURLToPath(
        new URL("../../libs/web-ui-token/src/index.ts", import.meta.url),
      ),
    },
  },
  server: {
    host: "127.0.0.1",
    port: 19310,
    proxy: {
      "/api": "http://127.0.0.1:19320",
    },
  },
});
