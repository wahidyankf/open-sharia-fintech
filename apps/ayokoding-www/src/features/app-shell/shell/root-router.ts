import { router } from "./trpc-init";
import { contentProcedures } from "@/features/content/shell/router";
import { navigationProcedures } from "@/features/navigation/shell/router";
import { searchProcedures } from "@/features/search/shell/router";
import { healthProcedures } from "@/features/health/shell/router";
import { i18nProcedures } from "@/features/i18n/shell/router";
import { coursePathProcedures } from "@/features/course-paths/shell/router";

export const appRouter = router({
  content: router({ ...contentProcedures, ...navigationProcedures }),
  search: router({ ...searchProcedures }),
  meta: router({ ...healthProcedures, ...i18nProcedures }),
  coursePaths: router(coursePathProcedures),
});

export type AppRouter = typeof appRouter;
