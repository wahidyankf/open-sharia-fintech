import path from "node:path";
import { createCallerFactory } from "@/features/app-shell/shell/trpc-init";
import type { TRPCContext } from "@/features/app-shell/shell/trpc-init";
import { appRouter } from "@/features/app-shell/shell/root-router";
import { FileSystemContentRepository } from "@/features/content/shell/repository-fs";
import { ContentService } from "@/features/content/shell/service";

const contentDirectory = path.resolve(process.cwd(), "content");
const contentService = new ContentService(new FileSystemContentRepository(contentDirectory));
const context: TRPCContext = { contentService };

export const integrationCaller = createCallerFactory(appRouter)(context);
