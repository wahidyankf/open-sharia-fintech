// AI BENCHMARK — benchmark-operator provenance (Phase 5, AC-34 / DD-21).
//
// The Sources and Licences section names each benchmark operator whose figures appear in the
// roster, together with that operator's republication terms. This is dataset-level metadata, not
// presentation: a new operator is added as one entry below with no component edit (W-22).
//
// The `termsKey` is an i18n key resolved by `<SHELL>how-to-read.tsx`; the localized terms copy
// itself lives in `features/i18n/core/translations.ts`. Operator *names* (SWE-bench, etc.) are
// proper nouns and are not translated.
//
// Per DD-21: where an operator states no terms, the entry records that explicitly via the shared
// `aiBenchOpTermsNone` key rather than implying permission.

/**
 * One benchmark operator and its republication terms. `termsKey` resolves to localized copy;
 * operators that state no terms share the `aiBenchOpTermsNone` key.
 */
export type BenchmarkOperator = {
  /** Proper-noun operator name (not translated). */
  name: string;
  /** i18n key for the operator's republication-terms copy. */
  termsKey: string;
  /** Optional operator / project home page. */
  url?: string;
};

/**
 * The benchmark operators whose figures appear in this roster (DD-21 table). Order is stable for
 * readable output; add a new operator by appending one entry.
 */
export const OPERATORS: readonly BenchmarkOperator[] = [
  {
    name: "SWE-bench",
    termsKey: "aiBenchOpTermsSwebench",
    url: "https://www.swebench.com",
  },
  {
    name: "Terminal-Bench",
    termsKey: "aiBenchOpTermsTerminalbench",
    url: "https://www.tbench.ai",
  },
  {
    name: "ARC Prize (GPQA)",
    termsKey: "aiBenchOpTermsArcprize",
    url: "https://github.com/idavidrein/gpqa",
  },
];
