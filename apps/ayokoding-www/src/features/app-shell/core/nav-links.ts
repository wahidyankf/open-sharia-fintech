import type { Locale } from "@/features/i18n/core/config";

/**
 * A single primary-navigation entry, shared by the header, the mobile-nav
 * drawer, and the footer so the three surfaces never drift.
 *
 * - `labelKey` is a translation key resolved via {@link t} at render time, so
 *   each surface controls its own JSX/styling while the label + destination
 *   stay centralized here.
 * - `hrefFor` is a pure function from `Locale` to the localized URL.
 */
export interface NavLink {
  readonly labelKey: string;
  readonly hrefFor: (locale: Locale) => string;
}

/**
 * Primary site navigation — Learn and Tools. Pure data (core): no JSX, no IO.
 *
 * Learn points at the browse index (`/{locale}/browse`, relocated from the
 * retired `/{locale}/c` content namespace, DD-48); Tools points at the tools
 * index (`/{locale}/tools`).
 */
export const PRIMARY_NAV_LINKS: readonly NavLink[] = [
  { labelKey: "navLearn", hrefFor: (locale) => `/${locale}/browse` },
  { labelKey: "navTools", hrefFor: (locale) => `/${locale}/tools` },
];
