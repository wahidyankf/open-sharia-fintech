export interface ContentMeta {
  title: string;
  slug: string;
  locale: string;
  weight: number;
  date?: Date;
  description?: string;
  tags: string[];
  draft: boolean;
  isSection: boolean;
  filePath: string;
  /**
   * Declared course prerequisites (course-paths plan, cycle 2.4) — course IDs this page names as
   * "take first". Optional (not every `ContentMeta` producer sets it, and every pre-existing
   * caller omits it) so the field is additive-only; consumers that resolve prerequisites treat an
   * absent field identically to an empty array.
   */
  prerequisites?: string[];
}

export interface ContentPage extends ContentMeta {
  html: string;
  headings: Heading[];
  prev: PageLink | null;
  next: PageLink | null;
}

export interface Heading {
  id: string;
  text: string;
  level: number;
}

export interface PageLink {
  title: string;
  slug: string;
}

export interface TreeNode {
  title: string;
  slug: string;
  weight: number;
  isSection: boolean;
  children: TreeNode[];
}

export interface SearchResult {
  title: string;
  slug: string;
  excerpt: string;
  locale: string;
}

export interface ContentIndex {
  contentMap: Map<string, ContentMeta>;
  trees: Record<string, TreeNode[]>;
  prevNext: Map<string, { prev: PageLink | null; next: PageLink | null }>;
}
