import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

export const env = createEnv({
  server: {
    AYOKODING_WEB_CONTENT_DIR: z.string().optional(),
    AYOKODING_WEB_SHOW_DRAFTS: z.enum(["true", "false"]).optional(),
    // course-paths plan (cycle 2.2) — overrides the manifests directory manifest-repository.ts
    // globs, mirroring AYOKODING_WEB_CONTENT_DIR above. Lets the e2e suite point at a fixture
    // manifest set (Phase 3) without touching the real, still-unpopulated manifests/ directory.
    AYOKODING_WEB_MANIFESTS_DIR: z.string().optional(),
  },
  experimental__runtimeEnv: {},
});
