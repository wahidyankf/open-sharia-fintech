// Example 73: Locale-Aware Number and Date Formatting via Intl. (co-35)
//
// The Intl API formats numbers and dates per locale -- no custom formatting code, no string
// concatenation. The SAME value renders as "1,234.56" in en-US, "1.234,56" in de-DE, and so on. This
// is the foundation of i18n: never hand-build a locale format; let Intl do it.

// formatNumber formats a number for a locale (grouping separators and the decimal symbol vary).
function formatNumber(value: number, locale: string): string {
  // => co-35: Intl picks the correct grouping and decimal separators per locale
  return new Intl.NumberFormat(locale).format(value); // => e.g. "1,234.56" vs "1.234,56"
}

// formatDate formats a fixed date for a locale (order and separators vary).
function formatDate(date: Date, locale: string): string {
  // => co-35: the locale decides field order (MDY vs DMY) and separators
  return new Intl.DateTimeFormat(locale, { dateStyle: "medium" }).format(date); // => e.g. "Jan 5, 2026"
}

const amount = 1234.56; // => the same value in every locale
const date = new Date("2026-01-05"); // => the same date in every locale

const locales = ["en-US", "de-DE", "id-ID"]; // => three locales to contrast
for (const loc of locales) {
  // => one value, three locale-correct renderings -- zero hand-written formatting
  console.log(`${loc}: ${formatNumber(amount, loc)} | ${formatDate(date, loc)}`); // => Output: one line per locale
}
