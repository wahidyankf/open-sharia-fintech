import { cleanup, render, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { CoursePathClientData } from "./course-path-nav";

const getRouteDataMock = vi.hoisted(() => vi.fn());

vi.mock("@/lib/trpc/client", () => ({
  trpcClient: {
    coursePaths: {
      getRouteData: { query: getRouteDataMock },
    },
  },
}));

// eslint-disable-next-line import/first
import { useRuntimeCoursePathData } from "./use-runtime-course-path-data";

const fallback: CoursePathClientData = {
  manifests: [],
  prerequisitesByCourse: {},
  libraryCourseIds: [],
  courseLinks: {},
};

function RuntimePathDataHarness({ locale, enabled }: { locale: string; enabled: boolean }) {
  useRuntimeCoursePathData(locale, fallback, enabled);
  return null;
}

afterEach(() => {
  cleanup();
  getRouteDataMock.mockReset();
});

describe("useRuntimeCoursePathData", () => {
  it("does not request runtime path data for an ordinary render with no path context", async () => {
    render(<RuntimePathDataHarness locale="ordinary-render" enabled={false} />);

    await Promise.resolve();

    expect(getRouteDataMock).not.toHaveBeenCalled();
  });

  it("requests runtime data when a fixture path context needs it", async () => {
    getRouteDataMock.mockResolvedValue(fallback);

    render(<RuntimePathDataHarness locale="fixture-path" enabled />);

    await waitFor(() => {
      expect(getRouteDataMock).toHaveBeenCalledWith("fixture-path");
    });
  });

  it("deduplicates the shared fixture-path request when multiple consumers need it", async () => {
    getRouteDataMock.mockResolvedValue(fallback);

    render(
      <>
        <RuntimePathDataHarness locale="fixture-drawer" enabled />
        <RuntimePathDataHarness locale="fixture-drawer" enabled />
      </>,
    );

    await waitFor(() => {
      expect(getRouteDataMock).toHaveBeenCalledTimes(1);
    });
  });
});
