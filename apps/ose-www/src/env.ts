import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

export const env = createEnv({
  server: {
    OSE_WEB_CONTENT_DIR: z.string().optional(),
    OSE_WEB_SEARCH_DATA_PATH: z.string().optional(),
    OSE_WEB_SHOW_DRAFTS: z.enum(["true", "false"]).optional(),
  },
  experimental__runtimeEnv: {},
});
