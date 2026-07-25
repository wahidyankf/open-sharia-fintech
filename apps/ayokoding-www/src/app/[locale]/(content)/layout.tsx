import { ResizableSidebar } from "@/features/navigation/shell/resizable-sidebar";
import { Sidebar } from "@/features/navigation/shell/sidebar";
import { SidebarHost } from "@/features/course-paths/shell/sidebar-host";
import { loadRoutePathData } from "@/features/course-paths/shell/route-path-data";
import { buildCourseTitleIndex } from "@/features/course-paths/shell/course-path-nav";
import type { Locale } from "@/features/i18n/core/config";

interface Props {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}

export default async function ContentLayout({ children, params }: Props) {
  const { locale } = await params;

  // Course-paths plan (Cycle 2.8) — loaded once per render here (not per page), so every course
  // page under this layout shares the same manifest set for its SidebarHost content swap.
  const pathData = await loadRoutePathData(locale);
  const courseTitles = buildCourseTitleIndex(pathData.contentMap, locale, pathData.manifests);

  return (
    <div className="mx-auto flex w-full max-w-screen-2xl">
      <ResizableSidebar locale={locale as Locale}>
        <SidebarHost locale={locale} manifests={pathData.manifests} courseTitles={courseTitles}>
          <Sidebar locale={locale} />
        </SidebarHost>
      </ResizableSidebar>
      <div className="flex min-w-0 flex-1">{children}</div>
    </div>
  );
}
