"use client";

import { useEffect, useState } from "react";
import { trpcClient } from "@/lib/trpc/client";
import type { CoursePathClientData } from "./course-path-nav";

const requestsByLocale = new Map<string, Promise<CoursePathClientData>>();

export interface RuntimeCoursePathData {
  data: CoursePathClientData;
  /** True only after the optional runtime refresh succeeds for the current locale. */
  isReady: boolean;
}

function requestRuntimePathData(locale: string): Promise<CoursePathClientData> | null {
  const coursePaths = trpcClient.coursePaths;
  if (!coursePaths) return null;

  const existing = requestsByLocale.get(locale);
  if (existing) return existing;

  const request = coursePaths.getRouteData.query(locale as "en" | "id").catch((error: unknown) => {
    requestsByLocale.delete(locale);
    throw error;
  });
  requestsByLocale.set(locale, request);
  return request;
}

/**
 * Refresh course-path data only after an active path context or opened drawer
 * needs it. Static generation intentionally captures no deployment-specific
 * manifest state; this opt-in query lets a running deployment supply its
 * current manifest set without making ordinary pages dynamic or chatty.
 */
export function useRuntimeCoursePathData(
  locale: string,
  fallback: CoursePathClientData,
  enabled: boolean,
): RuntimeCoursePathData {
  const [data, setData] = useState(fallback);
  const [loadedLocale, setLoadedLocale] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    if (!enabled) {
      return () => {
        active = false;
      };
    }

    const request = requestRuntimePathData(locale);
    if (!request) {
      return () => {
        active = false;
      };
    }

    void request.then(
      (next) => {
        if (active) {
          setData(next);
          setLoadedLocale(locale);
        }
      },
      () => {
        // Keep the statically generated fallback when the optional runtime
        // endpoint is unavailable (for example, during a transient outage).
      },
    );

    return () => {
      active = false;
    };
  }, [enabled, locale]);

  return { data, isReady: enabled && loadedLocale === locale };
}
