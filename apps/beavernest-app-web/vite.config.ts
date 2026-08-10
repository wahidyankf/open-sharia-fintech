import { fileURLToPath, URL } from "node:url";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

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
