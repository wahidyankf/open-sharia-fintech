import type { Metadata } from "next";
import { serverCaller } from "@/lib/trpc/server";
import type { Locale } from "@/features/i18n/core/config";
import type { TreeNode } from "@/features/content/core/types";
import { t } from "@/features/i18n/core/translations";
import { BrowseIndex } from "@/features/content/shell/browse-index";

interface Props {
  params: Promise<{ locale: string }>;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  return {
    title: t(locale as Locale, "browseTitle"),
    description: t(locale as Locale, "browseIntro"),
    alternates: {
      canonical: `/${locale}/browse`,
    },
  };
}

export default async function BrowsePage({ params }: Props) {
  const { locale } = await params;

  const sections = (await serverCaller.content.getTree({
    locale: locale as Locale,
  })) as TreeNode[];

  // The tree root is a synthetic node (slug ""). The browseable content
  // sections are its section-typed children (e.g. "learn", "rants" for `en`).
  // Fall back to the root's direct children when the tree is flat (no root node).
  const rootNode = sections.find((node) => node.slug === "");
  const topLevelSections = (rootNode ? rootNode.children : sections).filter((node) => node.isSection);

  return <BrowseIndex locale={locale as Locale} sections={topLevelSections} />;
}
