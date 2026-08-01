"use client";

import { useSearchParams } from "next/navigation";
import { CoursePageContent, type CoursePageContentProps } from "./course-page-content";
import {
  EMPTY_COURSE_PATH_CLIENT_DATA,
  type CoursePathRenderData,
  resolveCoursePathClientRenderData,
  type CoursePathClientData,
} from "./course-path-nav";
import { useRuntimeCoursePathData } from "./use-runtime-course-path-data";

interface CoursePagePathContentProps extends Omit<CoursePageContentProps, "renderData" | "courseId"> {
  courseId: string;
  /**
   * Compact, per-page canonical chrome captured during static generation. It preserves this
   * course's prerequisite links and path badges after hydration without serializing the complete
   * locale catalog into every ordinary page.
   */
  canonicalRenderData: CoursePathRenderData;
  /** Static pages start empty; opted-in path navigation refreshes this after hydration. */
  pathData?: CoursePathClientData;
  fallbackPrev: CoursePageContentProps["renderData"]["prev"];
  fallbackNext: CoursePageContentProps["renderData"]["next"];
}

/**
 * Hydrated course-page chrome. `useSearchParams()` stays inside the route's
 * narrow Suspense boundary, preserving a static HTML fallback for every
 * generated content URL while retaining `?path=` navigation after hydration.
 */
export function CoursePagePathContent({
  courseId,
  canonicalRenderData,
  pathData = EMPTY_COURSE_PATH_CLIENT_DATA,
  fallbackPrev,
  fallbackNext,
  ...page
}: CoursePagePathContentProps) {
  const searchParams = useSearchParams();
  const hasPathContext = searchParams.has("path");
  const runtimePathData = useRuntimeCoursePathData(page.locale, pathData, hasPathContext);
  const renderData = hasPathContext
    ? resolveCoursePathClientRenderData(searchParams, runtimePathData, courseId, fallbackPrev, fallbackNext)
    : canonicalRenderData;

  return <CoursePageContent {...page} courseId={courseId} renderData={renderData} />;
}
