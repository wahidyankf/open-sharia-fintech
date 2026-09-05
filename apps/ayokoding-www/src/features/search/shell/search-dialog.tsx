"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import {
  CommandDialog,
  CommandInput,
  CommandList,
  CommandEmpty,
  CommandGroup,
  CommandItem,
} from "@open-sharia-enterprise/web-ui";
import { useLocale } from "@/features/i18n/shell/use-locale";
import { useSearchOpen } from "@/features/search/shell/use-search";
import { t } from "@/features/i18n/core/translations";
import { trpcClient } from "@/lib/trpc/client";
import type { SearchResult } from "@/features/content/core/types";
import { contentUrl } from "@/features/content/core/content-url";
import type { Locale } from "@/features/i18n/core/config";

export function formatSectionPath(slug: string): string {
  const parts = slug.split("/");
  if (parts.length <= 1) return "";
  return parts
    .slice(0, -1)
    .map((part) =>
      part
        .split("-")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" "),
    )
    .join(" / ");
}

export function SearchDialog() {
  const { open, setOpen } = useSearchOpen();
  const locale = useLocale();
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);

  // Keyboard shortcut
  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setOpen(true);
      }
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [setOpen]);

  // Debounced search
  useEffect(() => {
    if (!query || query.length < 1) {
      setResults([]);
      return;
    }

    const timer = setTimeout(async () => {
      setLoading(true);
      try {
        const data = await trpcClient.search.query.query({
          query,
          locale,
          limit: 10,
        });
        setResults(data);
      } catch {
        setResults([]);
      } finally {
        setLoading(false);
      }
    }, 200);

    return () => clearTimeout(timer);
  }, [query, locale]);

  const handleSelect = useCallback(
    (slug: string) => {
      setOpen(false);
      setQuery("");
      router.push(contentUrl(locale as Locale, slug));
    },
    [locale, router, setOpen],
  );

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput placeholder={t(locale, "search")} value={query} onValueChange={setQuery} />
      <CommandList>
        {query.length > 0 && results.length === 0 && !loading && <CommandEmpty>{t(locale, "noResults")}</CommandEmpty>}
        {results.length > 0 && (
          <CommandGroup heading="Results">
            {results.map((result) => (
              <CommandItem
                key={result.slug}
                data-result-slug={result.slug}
                // Rule-15 e2e regression fix (surfaced by USS-001): cmdk's own client-side fuzzy
                // filter re-filters items against this `value` string. Results are already
                // server-filtered (ContentService.search), so re-filtering here is redundant AND
                // harmful whenever a query matches the title but not the slug — e.g. "AI Model
                // Benchmark" matches the title but not the slug `tools/ai-benchmark` (no "model"),
                // so cmdk hid an already-correct result. Including the title keeps `value` unique
                // per item (slug is unique) while making cmdk's filter agree with the server's.
                value={`${result.title} ${result.slug}`}
                onSelect={() => handleSelect(result.slug)}
                className="cursor-pointer"
              >
                <div className="flex flex-col gap-1">
                  <span data-testid="search-result-title" className="font-medium">
                    {result.title}
                  </span>
                  <span data-testid="search-result-path" className="line-clamp-1 text-xs text-muted-foreground">
                    {formatSectionPath(result.slug)}
                  </span>
                  <span data-testid="search-result-excerpt" className="line-clamp-1 text-xs text-muted-foreground">
                    {result.excerpt}
                  </span>
                </div>
              </CommandItem>
            ))}
          </CommandGroup>
        )}
      </CommandList>
    </CommandDialog>
  );
}
