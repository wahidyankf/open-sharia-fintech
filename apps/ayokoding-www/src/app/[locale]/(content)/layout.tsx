import { ResizableSidebar } from "@/features/navigation/shell/resizable-sidebar";
import { Sidebar } from "@/features/navigation/shell/sidebar";
import type { Locale } from "@/features/i18n/core/config";

interface Props {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}

export default async function ContentLayout({ children, params }: Props) {
  const { locale } = await params;

  return (
    <div className="mx-auto flex w-full max-w-screen-2xl">
      <ResizableSidebar locale={locale as Locale}>
        <Sidebar locale={locale} />
      </ResizableSidebar>
      <div className="flex min-w-0 flex-1">{children}</div>
    </div>
  );
}
