import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  timeout: 60000,
  use: { baseURL: "http://127.0.0.1:19310" },
  webServer: {
    command: "npm exec -- vite apps/beavernest-app-web --host 127.0.0.1 --port 19310",
    cwd: "../..",
    reuseExistingServer: !process.env.CI,
    url: "http://127.0.0.1:19310",
  },
});
