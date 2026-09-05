import { existsSync } from "node:fs";
import dotenv from "dotenv";
import type { TierEnvPort } from "./index";

/** Production adapter for the Node filesystem and dotenv parser. */
export const nodeTierEnvPort: TierEnvPort = {
  exists: existsSync,
  load(filePath, env) {
    dotenv.config({
      path: filePath,
      override: false,
      processEnv: env as unknown as Record<string, string>,
    });
  },
};
