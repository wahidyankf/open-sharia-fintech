export const SUPPORTED_LOCALES = ["en", "id"] as const;
export type Locale = (typeof SUPPORTED_LOCALES)[number];

export const DEFAULT_LOCALE: Locale = "en";
export const DEFAULT_LOCALE_HREF = `/${DEFAULT_LOCALE}` as const;

export function isValidLocale(locale: string): locale is Locale {
  return (SUPPORTED_LOCALES as readonly string[]).includes(locale);
}

/** Maps EN URL segments to ID equivalents */
export const SEGMENT_MAP: Record<string, Record<string, string>> = {
  en: {},
  id: {
    learn: "belajar",
    rants: "celoteh",
    overview: "ikhtisar",
  },
};

export const LOCALE_LABELS: Record<Locale, string> = {
  en: "English",
  id: "Bahasa Indonesia",
};
