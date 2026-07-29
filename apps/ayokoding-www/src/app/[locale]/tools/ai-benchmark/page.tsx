import { Suspense } from "react";
import type { Metadata } from "next";
import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";
import { BenchmarkContent } from "./benchmark-content";

export async function generateMetadata(props: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await props.params;
  return { title: t(locale as Locale, "aiBenchTitle") };
}

export default function AiBenchmarkPage() {
  return (
    <Suspense>
      <BenchmarkContent />
    </Suspense>
  );
}
