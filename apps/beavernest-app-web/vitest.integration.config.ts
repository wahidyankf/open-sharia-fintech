import { mergeConfig } from "vite";
import unitConfig from "./vitest.config";

export default mergeConfig(unitConfig, {
  test: {
    name: "integration",
    include: ["src/**/*.integration.test.{ts,tsx}"],
  },
});
