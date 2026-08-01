"use client";

import { useEffect, useState } from "react";
import { trpcClient } from "@/lib/trpc/client";
import type { CoursePathClientData } from "./course-path-nav";

/**
 * Refresh course-path data after hydration. Static generation intentionally
 * captures no deployment-specific manifest state; this query lets a running
 * deployment supply its current manifest set without making the page dynamic.
 */
export function useRuntimeCoursePathData(locale: string, fallback: CoursePathClientData): CoursePathClientData {
  const [data, setData] = useState(fallback);

  useEffect(() => {
    let active = true;
    const coursePaths = trpcClient.coursePaths;

    // Unit renderers deliberately provide their own deterministic path data;
    // they neither run an HTTP server nor need a runtime refresh.
    if (process.env.NODE_ENV === "test" || !coursePaths) {
      return () => {
        active = false;
      };
    }

    void coursePaths.getRouteData.query(locale as "en" | "id").then(
      (next) => {
        if (active) setData(next);
      },
      () => {
        // Keep the statically generated fallback when the optional runtime
        // endpoint is unavailable (for example, during a transient outage).
      },
    );

    return () => {
      active = false;
    };
  }, [locale]);

  return data;
}
