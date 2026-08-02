import { publicProcedure } from "@/features/app-shell/shell/trpc-init";
import { localeSchema } from "@/features/i18n/core/schemas";
import { toCoursePathClientData } from "./course-path-nav";
import { loadRoutePathData } from "./route-path-data";

/** Runtime course-path data for client navigation on statically generated pages. */
export const coursePathProcedures = {
  getRouteData: publicProcedure.input(localeSchema).query(async ({ input }) => {
    return toCoursePathClientData(await loadRoutePathData(input), input);
  }),
};
