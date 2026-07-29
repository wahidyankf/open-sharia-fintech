// AI BENCHMARK — benchmark display metadata (Phase 5).
//
// The data table renders one column per composite benchmark, in a fixed order, with a localized
// header label. This is the single place that maps a `BenchmarkId` to its i18n label key and
// column order — the shell reads it verbatim, so reordering or renaming a column is a one-line
// change here, not a table edit. No figures live here (FCIS boundary): only identifiers and the
// i18n key that resolves to localized copy.

import type { BenchmarkId } from "./models";

/** A benchmark column: its id and the i18n key for its localized header label. */
export type BenchmarkColumn = {
  id: BenchmarkId;
  /** i18n key resolving to the localized column header (e.g. "SWE-bench Verified"). */
  labelKey: string;
};

/**
 * The four composite benchmarks in canonical column order, each mapped to its localized label key.
 * The data table renders exactly these columns (AC-20).
 */
export const BENCHMARK_COLUMNS: readonly BenchmarkColumn[] = [
  { id: "swe-bench-verified", labelKey: "aiBenchBenchSweVerified" },
  { id: "swe-bench-pro", labelKey: "aiBenchBenchSwePro" },
  { id: "terminal-bench-2-1", labelKey: "aiBenchBenchTerminalBench" },
  { id: "gpqa-diamond", labelKey: "aiBenchBenchGpqa" },
];

/** Display names for the five harnesses — proper nouns, not translated. */
export const HARNESS_DISPLAY_NAMES: Readonly<Record<string, string>> = {
  "claude-code": "Claude Code",
  "codex-cli": "Codex CLI",
  cursor: "Cursor",
  "opencode-go": "OpenCode Go",
  "opencode-zen": "OpenCode Zen",
};

/** i18n label keys for the four capability bands. */
export const BAND_LABEL_KEYS: Readonly<Record<string, string>> = {
  opus: "aiBenchBandOpus",
  sonnet: "aiBenchBandSonnet",
  light: "aiBenchBandLight",
  unrated: "aiBenchBandUnrated",
};

/** i18n label keys for the five evidence grades. */
export const GRADE_LABEL_KEYS: Readonly<Record<string, string>> = {
  verified: "aiBenchGradeVerified",
  "self-reported": "aiBenchGradeSelfReported",
  secondary: "aiBenchGradeSecondary",
  conflicted: "aiBenchGradeConflicted",
  unavailable: "aiBenchGradeUnavailable",
};
