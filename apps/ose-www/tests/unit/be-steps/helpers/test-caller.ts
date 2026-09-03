import { createCallerFactory } from "@/lib/trpc/init";
import type { TRPCContext } from "@/lib/trpc/init";
import { appRouter } from "@/features/app-shell/shell/root-router";
import { testContentService } from "./test-service";

const context: TRPCContext = { contentService: testContentService };

const createCaller = createCallerFactory(appRouter);
export const testCaller = createCaller(context);
