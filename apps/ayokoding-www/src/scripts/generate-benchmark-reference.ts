// DD-18 — generates the DATA TABLES of docs/reference/ai-model-benchmarks.md from the single source
// of truth at apps/ayokoding-www/src/features/ai-benchmark/core/data/models.ts. Hand-written prose
// (benchmark definitions, tier rationale, caveats) is preserved verbatim: only the text between
// `<!-- BEGIN GENERATED: <name> -->` / `<!-- END GENERATED: <name> -->` marker pairs is rewritten.
//
// Marker-first guard: the generator locates a BEGIN/END pair BEFORE substituting and throws loudly
// when one is missing. It NEVER falls back to inserting at an anchor — an insert-style substitution
// duplicates content on every re-run.
//
// Nx targets (see apps/ayokoding-www/project.json):
//   generate-benchmark-reference  → writes the reference in place.
//   validate-benchmark-reference  → regenerates in memory and exits non-zero on drift.
//
// The rendering logic is split into PURE functions (`renderTables`, `substituteMarkers`) that take
// their inputs as arguments and do no disk I/O, so they are unit-tested directly; the `main()` shell
// below is the only place that touches the filesystem.

import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  dataset,
  isConflictedFigure,
  type BenchmarkId,
  type Dataset,
  type EvidenceGrade,
  type HarnessId,
  type Model,
} from "../features/ai-benchmark/core/data/models";

/** A generated block's inner content, keyed by marker name. */
export type GeneratedTables = Record<string, string>;

// ─── Evidence-grade presentation ──────────────────────────────────────────────

const GRADE_LABEL: Record<EvidenceGrade, string> = {
  verified: "[Verified]",
  "self-reported": "[Self-reported]",
  secondary: "[Secondary]",
  conflicted: "[Conflicted]",
  unavailable: "[Unavailable]",
};

/** The four composite benchmarks (DD-5), in display order. */
const BENCHMARK_ORDER: BenchmarkId[] = ["swe-bench-verified", "swe-bench-pro", "terminal-bench-2-1", "gpqa-diamond"];

/** Canonical harness display order for the per-harness pricing table. */
const HARNESS_ORDER: HarnessId[] = ["claude-code", "codex-cli", "cursor", "opencode-go", "opencode-zen"];

// ─── Pure table-rendering helpers ─────────────────────────────────────────────

/**
 * Render a single benchmark cell for a model. Returns `—` when the model has no figure for that
 * benchmark; for a conflicted figure, shows the published LOW–HIGH range (the LOW enters the
 * composite, per DD-6); otherwise shows `value% [Grade]`.
 */
function figureCell(model: Model, benchmark: BenchmarkId): string {
  const fig = model.figures.find((f) => f.benchmark === benchmark);
  if (!fig) return "—";
  if (isConflictedFigure(fig)) {
    return `${fig.low}–${fig.high}% ${GRADE_LABEL.conflicted}`;
  }
  return `${fig.value}% ${GRADE_LABEL[fig.grade]}`;
}

/** Format a USD-per-1M-tokens rate with no trailing-zero noise (e.g. 5 → "$5", 0.435 → "$0.435"). */
function money(n: number): string {
  return Number.isInteger(n) ? `$${n}` : `$${n.toString()}`;
}

/**
 * Format a GitHub-flavoured markdown table with column widths padded to the longest cell — the same
 * shape Prettier emits for markdown tables (left-aligned, dashes match column width) — so the
 * generator's output is stable under the repo's Prettier pre-commit pass and does not trip the
 * `validate-benchmark-reference` drift gate.
 */
function formatTable(header: string[], rows: string[][]): string {
  const cols = header.length;
  const all = [header, ...rows];
  const widths = Array.from({ length: cols }, (_, c) => Math.max(...all.map((r) => (r[c] ?? "").length)));
  const padRow = (cells: string[]) => "| " + cells.map((c, i) => c.padEnd(widths[i] ?? 0)).join(" | ") + " |";
  const separator = "| " + widths.map((w) => "-".repeat(w)).join(" | ") + " |";
  return [padRow(header), separator, ...rows.map(padRow)].join("\n");
}

/** Wrap a block body in the standard leading/trailing blank lines that separate it from its markers. */
function block(body: string): string {
  return `\n\n${body}\n\n`;
}

function renderRoster(ds: Dataset): string {
  const goModels = ds.models.filter((m) => m.harnesses.includes("opencode-go"));
  const rows = goModels.map((m) => {
    const others = m.harnesses.filter((h) => h !== "opencode-go").join(", ") || "—";
    return [`opencode-go/${m.id}`, m.name, m.vendor, others, figureCell(m, "swe-bench-pro")];
  });
  const table = formatTable(["Model ID", "Display Name", "Provider", "Other Harnesses", "SWE-bench Pro"], rows);
  const caption =
    `> Snapshot ${ds.snapshotDate} — ${goModels.length} models selectable via the ` +
    "`opencode-go/`" +
    ` flat-rate subscription. Derived from ` +
    "`apps/ayokoding-www/src/features/ai-benchmark/core/data/models.ts`.";
  return block(`${caption}\n\n${table}`);
}

function renderPricing(ds: Dataset): string {
  const rows: string[][] = [];
  for (const m of ds.models) {
    for (const h of HARNESS_ORDER) {
      const price = m.pricing[h];
      if (!price) continue;
      if (price.kind === "metered") {
        rows.push([m.name, h, money(price.input), money(price.output), GRADE_LABEL[price.grade]]);
      } else {
        rows.push([m.name, h, `$${price.planCostUsd}/mo sub`, "—", "—"]);
      }
    }
  }
  const table = formatTable(["Model", "Harness", "Input $/1M", "Output $/1M", "Grade"], rows);
  const caption =
    `> Per-harness standard-tier rates, snapshot ${ds.snapshotDate}. Metered prices are USD per 1M ` +
    "tokens; `opencode-go` rows are the flat-rate subscription. Derived from `models.ts`.";
  return block(`${caption}\n\n${table}`);
}

function renderFrontier(ds: Dataset): string {
  const bigBrands = new Set(["Anthropic", "OpenAI", "Google"]);
  const preferredHarness: Record<string, HarnessId> = {
    Anthropic: "claude-code",
    OpenAI: "codex-cli",
    Google: "cursor",
  };
  const header = [
    "Provider",
    "Model",
    ...BENCHMARK_ORDER.map((b) =>
      b === "swe-bench-verified"
        ? "SWE-bench Verified"
        : b === "swe-bench-pro"
          ? "SWE-bench Pro"
          : b === "terminal-bench-2-1"
            ? "Terminal-Bench 2.1"
            : "GPQA Diamond",
    ),
    "In $/1M",
    "Out $/1M",
  ];
  const rows = ds.models
    .filter((m) => bigBrands.has(m.vendor))
    .map((m) => {
      const harness: HarnessId = preferredHarness[m.vendor] ?? m.harnesses[0] ?? "opencode-zen";
      const price = m.pricing[harness];
      let inCell = "—";
      let outCell = "—";
      if (price && price.kind === "metered") {
        inCell = money(price.input);
        outCell = money(price.output);
      } else if (price && price.kind === "subscription") {
        inCell = `$${price.planCostUsd}/mo sub`;
      }
      return [m.vendor, m.name, ...BENCHMARK_ORDER.map((b) => figureCell(m, b)), inCell, outCell];
    });
  const table = formatTable(header, rows);
  const caption =
    `> Frontier/big-brand models in the dataset, snapshot ${ds.snapshotDate}. Pricing shown is the ` +
    "vendor-native harness rate where one is recorded. Derived from `models.ts`.";
  return block(`${caption}\n\n${table}`);
}

function renderCapabilitySummary(ds: Dataset): string {
  const header = [
    "Model",
    "Provider",
    ...BENCHMARK_ORDER.map((b) =>
      b === "swe-bench-verified"
        ? "SWE-bench Verified"
        : b === "swe-bench-pro"
          ? "SWE-bench Pro"
          : b === "terminal-bench-2-1"
            ? "Terminal-Bench 2.1"
            : "GPQA Diamond",
    ),
  ];
  const rows = ds.models.map((m) => [m.name, m.vendor, ...BENCHMARK_ORDER.map((b) => figureCell(m, b))]);
  const table = formatTable(header, rows);
  const caption =
    `> Composite-benchmark figures for every model in the dataset, snapshot ${ds.snapshotDate}. ` +
    "Conflicted figures show their published LOW–HIGH range; the LOW enters the composite (DD-6). " +
    "Derived from `models.ts`.";
  return block(`${caption}\n\n${table}`);
}

/**
 * Derive every generated block from the dataset. PURE: no disk I/O, deterministic, unit-tested.
 * The keys MUST match the marker names written into the reference document.
 */
export function renderTables(ds: Dataset): GeneratedTables {
  return {
    roster: renderRoster(ds),
    pricing: renderPricing(ds),
    frontier: renderFrontier(ds),
    "capability-summary": renderCapabilitySummary(ds),
  };
}

// ─── Marker-delimited substitution (PURE) ────────────────────────────────────

interface MarkerPair {
  name: string;
  /** Index immediately AFTER the BEGIN tag (start of inner content). */
  innerStart: number;
  /** Index of the END tag's leading `<` (end of inner content). */
  innerEnd: number;
  /** Index immediately AFTER the END tag. */
  afterEnd: number;
}

/**
 * Scan the document for BEGIN/END marker pairs in order. Marker-first guard: throws if any BEGIN has
 * no following END with the SAME name (so substitution can never silently fall back to insertion,
 * which would duplicate content on re-run).
 */
function findMarkerPairs(input: string): MarkerPair[] {
  // Fresh global regex (no shared lastIndex state across invocations). Global (`/g`) SEARCHES from
  // lastIndex onward; sticky (`/y`) would ANCHOR at lastIndex and miss markers not at position 0.
  const beginTag = /<!-- BEGIN GENERATED: (\S+) -->/g;
  const pairs: MarkerPair[] = [];
  let match: RegExpExecArray | null;
  while ((match = beginTag.exec(input)) !== null) {
    const name = match[1];
    if (name === undefined) continue; // unreachable: the regex's (\S+) capture is mandatory
    const innerStart = beginTag.lastIndex; // index just after the matched BEGIN tag
    const endTag = `<!-- END GENERATED: ${name} -->`;
    const innerEnd = input.indexOf(endTag, innerStart);
    if (innerEnd === -1) {
      throw new Error(
        `generate-benchmark-reference: BEGIN GENERATED marker "${name}" has no matching END — ` +
          "refusing to substitute (an insert-style fallback would duplicate content on re-run).",
      );
    }
    const afterEnd = innerEnd + endTag.length;
    pairs.push({ name, innerStart, innerEnd, afterEnd });
    beginTag.lastIndex = afterEnd; // resume scanning after this pair's END tag
  }
  if (pairs.length === 0) {
    throw new Error("generate-benchmark-reference: no BEGIN GENERATED markers found in the reference document.");
  }
  return pairs;
}

/**
 * Replace ONLY the text between each marker pair with the corresponding generated block. Every byte
 * outside the marker pairs (including the marker tags themselves) is preserved. Throws if a marker
 * pair is missing its END, or if the document carries a marker name the generator does not produce.
 */
export function substituteMarkers(input: string, tables: GeneratedTables): string {
  const pairs = findMarkerPairs(input);
  let out = "";
  let cursor = 0;
  for (const p of pairs) {
    if (!(p.name in tables)) {
      throw new Error(
        `generate-benchmark-reference: document has a "${p.name}" generated block, but renderTables ` +
          "produces no such table. Either add the section to renderTables or remove the marker pair.",
      );
    }
    out += input.slice(cursor, p.innerStart); // prose + the BEGIN tag, untouched
    out += tables[p.name]; // canonical generated inner content
    cursor = p.innerEnd; // the END tag (+ following prose) is appended by the next slice / tail
  }
  out += input.slice(cursor); // final END tag + trailing prose, untouched
  return out;
}

// ─── Thin file-I/O shell ─────────────────────────────────────────────────────

// The reference lives at the repository root, not under this app; resolve from this script's
// location so the path is correct regardless of the process cwd.
const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const REF_PATH = path.resolve(SCRIPT_DIR, "../../../../docs/reference/ai-model-benchmarks.md");

async function main(): Promise<void> {
  const mode = process.argv.includes("--validate") ? "validate" : "generate";
  const original = await readFile(REF_PATH, "utf8");
  const tables = renderTables(dataset);
  const regenerated = substituteMarkers(original, tables);

  if (mode === "validate") {
    if (regenerated !== original) {
      console.error(
        "generate-benchmark-reference: docs/reference/ai-model-benchmarks.md is out of date with models.ts (drift inside BEGIN/END GENERATED blocks).",
      );
      console.error("Regenerate with:  npx nx run ayokoding-www:generate-benchmark-reference");
      process.exit(1);
    }
    console.log("generate-benchmark-reference: reference is up to date.");
    return;
  }

  if (regenerated !== original) {
    await writeFile(REF_PATH, regenerated, "utf8");
    console.log("generate-benchmark-reference: updated docs/reference/ai-model-benchmarks.md.");
  } else {
    console.log("generate-benchmark-reference: already up to date.");
  }
}

// Run the I/O shell only when invoked directly as a script, never when imported (e.g. by the unit
// tests, which exercise the pure functions only).
const invokedDirectly =
  process.argv[1] !== undefined && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);

if (invokedDirectly) {
  main().catch((err) => {
    console.error(err);
    process.exit(1);
  });
}
