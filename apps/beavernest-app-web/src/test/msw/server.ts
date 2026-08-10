import { setupServer } from "msw/node";
import { readinessHandler } from "./handlers";

export const server = setupServer(readinessHandler);
