"use client";

import { useSearchParams } from "next/navigation";
import { CoursePageContent, type CoursePageContentProps } from "./course-page-content";
import { resolveCoursePathClientRenderData, type CoursePathClientData } from "./course-path-nav";
import { useRuntimeCoursePathData } from "./use-runtime-course-path-data";

interface CoursePagePathContentProps extends Omit<CoursePageContentProps, "renderData" | "courseId"> {
  courseId: string;
  pathData: CoursePathClientData;
  fallbackPrev: CoursePageContentProps["renderData"]["prev"];
  fallbackNext: CoursePageContentProps["renderData"]["next"];
}

/**
 * Hydrated course-page chrome. `useSearchParams()` stays inside the route's
 * narrow Suspense boundary, preserving a static HTML fallback for every
 * generated content URL while retaining `?path=` navigation after hydration.
 */
export function CoursePagePathContent({ courseId, pathData, fallbackPrev, fallbackNext, ...page }: CoursePagePathContentProps) {
  const searchParams = useSearchParams();
  const runtimePathData = useRuntimeCoursePathData(page.locale, pathData);
  const renderData = resolveCoursePathClientRenderData(
    searchParams,
    runtimePathData,
    courseId,
    fallbackPrev,
    fallbackNext,
  );

  return <CoursePageContent {...page} courseId={courseId} renderData={renderData} />;
}
