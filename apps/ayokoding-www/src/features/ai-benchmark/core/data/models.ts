// AI BENCHMARK DATASET — coding-agent model roster across five harnesses, snapshotDate 2026-07-28.
// Sources: vendor pricing pages + benchmark leaderboards (see each figure's `source` URL).
// Roster rule DD-7a: a model is included when selectable in ≥1 of the five harnesses' current
//   rosters and is current or one generation prior; deprecated/legacy/invitation-only and
//   no-identifiable-vendor entries are excluded.
// Pricing DD-12/DD-16/DD-17a: standard tier only, stored PER HARNESS (the rate that harness
//   charges); promotions with a known expiry publish the post-expiry standard rate (Sonnet 5 →
//   $3/$15 from 2026-09-01, not the $2/$10 intro).
// Evidence grades DD-19: verified | self-reported | secondary | conflicted | unavailable.
// Composite DD-5a/DD-6: roster-relative normalization; for a CONFLICTED figure the LOW published
//   value enters the composite and the full range is stored (low ≤ high, value === low).
// Version trap (invariant 9): a Terminal-Bench 2.0 or SWE-bench Multilingual figure is NEVER
//   placed in a terminal-bench-2-1 / swe-bench-verified slot — such figures are absent here.
// To (re)source this data, see the prompts in
// ../../../../../docs/ai-benchmark/data-sourcing-prompt.md

// ─── Types ────────────────────────────────────────────────────────────────────

/** Provenance of a single figure. DD-19. */
export type EvidenceGrade = "verified" | "self-reported" | "secondary" | "conflicted" | "unavailable";

/** The four benchmarks that make up the composite index (DD-5). */
export type BenchmarkId = "swe-bench-verified" | "swe-bench-pro" | "terminal-bench-2-1" | "gpqa-diamond";

/**
 * The five harnesses whose current rosters define the model universe (DD-7).
 * Mapping to the Appendix A.2 abbreviations: claude-code = CC, codex-cli = CX,
 * cursor = CU, opencode-go = GO, opencode-zen = ZEN.
 */
export type HarnessId = "claude-code" | "codex-cli" | "cursor" | "opencode-go" | "opencode-zen";

/** Composite-index weights per benchmark (DD-5). Sums to 100. */
export const BENCHMARK_WEIGHTS: Record<BenchmarkId, number> = {
  "swe-bench-verified": 25,
  "swe-bench-pro": 25,
  "terminal-bench-2-1": 20,
  "gpqa-diamond": 30,
};

/**
 * A single benchmark figure. `value` is the percentage 0–100 that enters the composite (for a
 * conflicted figure, the LOW published value). `source` is a non-empty URL naming the origin.
 * `benchmarkVersion` / `conditions` record the version and evaluation condition — these are also
 * what invariant 9 inspects to keep the version trap honest.
 */
export type Figure = {
  benchmark: BenchmarkId;
  value: number;
  grade: EvidenceGrade;
  source: string;
  benchmarkVersion?: string;
  conditions?: string;
};

/**
 * A conflicted figure extends Figure with the full published range. `value === low` (the LOW
 * enters the composite per the scoring pipeline line 117) and `low ≤ high`.
 */
export type ConflictedFigure = Figure & {
  grade: "conflicted";
  low: number;
  high: number;
};

/** Type guard narrowing a Figure to its conflicted form (carries low/high). */
export function isConflictedFigure(f: Figure): f is ConflictedFigure {
  return f.grade === "conflicted";
}

/** A metered per-token price (USD per 1M tokens), standard tier (DD-12). */
export type MeteredPrice = {
  kind: "metered";
  input: number;
  output: number;
  grade: EvidenceGrade;
  source: string;
  conditions?: string;
};

/**
 * A flat-rate subscription price. Carries a plan cost and usage caps and NEVER a per-token rate
 * (invariant 10). Used for every OpenCode Go entry ($10/mo after first month). Carries a `grade`
 * like every other priced/figured entry (DD-19a) so AC-21 ("every price cell carries an evidence
 * grade marker") is satisfiable for subscription-only rows, not unsatisfiable by construction.
 */
export type SubscriptionPrice = {
  kind: "subscription";
  planCostUsd: number;
  grade: EvidenceGrade;
  caps?: string;
  source: string;
};

/** A model's price set: the rate each harness that carries the model charges (DD-16). */
export type PriceSet = Partial<Record<HarnessId, MeteredPrice | SubscriptionPrice>>;

/** A provenance flag that must reach the page (e.g. the METR gaming finding). */
export type IntegrityNote = {
  modelId: string;
  text: string;
  source: string;
};

/** One model row. */
export type Model = {
  id: string;
  name: string;
  vendor: string;
  harnesses: HarnessId[];
  figures: Figure[];
  pricing: PriceSet;
  notes?: IntegrityNote[];
};

/** The full dataset — single source of truth for the page and the reference generator. */
export type Dataset = {
  snapshotDate: string;
  models: Model[];
  anchorIds: { opus: string; sonnet: string };
};

/** Anchor model ids — the bands are defined by these two models (DD-20a). */
export const OPUS_ANCHOR_ID = "claude-opus-5";
export const SONNET_ANCHOR_ID = "claude-sonnet-5";

// ─── Source URLs (vendor pricing pages + benchmark operator / aggregator sources) ──────────
// Every figure below cites one of these. They are the real URLs named in Appendix A.1/A.3/A.4.

const URL = {
  anthropic: "https://platform.claude.com/docs/en/pricing",
  anthropicModels: "https://platform.claude.com/docs/en/models/overview",
  openai: "https://developers.openai.com/api/docs/pricing",
  openaiModels: "https://developers.openai.com/codex/models",
  google: "https://ai.google.dev/gemini-api/docs/pricing",
  googleModels: "https://ai.google.dev/gemini-api/docs/models",
  xai: "https://docs.x.ai/docs/models",
  deepseek: "https://api-docs.deepseek.com",
  alibaba: "https://www.alibabacloud.com/help/en/model-studio/model-pricing",
  zai: "https://docs.z.ai/guides/overview/pricing",
  minimax: "https://platform.minimax.io/docs/guides/pricing-paygo",
  kimi: "https://platform.kimi.ai",
  cursor: "https://www.cursor.com/pricing",
  opencodeGo: "https://opencode.ai/docs",
  opencodeZen: "https://opencode.ai/docs",
  sweVerified: "https://llm-stats.com/benchmarks/swe-bench-verified",
  swePro: "https://scale.com/leaderboard/swe-bench-pro",
  terminalBench: "https://www.tbench.ai",
  gpqa: "https://github.com/idavidrein/gpqa",
} as const;

// ─── Figure / price helpers (keep the literals terse, like cities.ts's `m()`) ───────────────

type FigureExtras = Pick<Partial<Figure>, "benchmarkVersion" | "conditions">;

function fig(
  benchmark: BenchmarkId,
  value: number,
  grade: EvidenceGrade,
  source: string,
  extra: FigureExtras = {},
): Figure {
  return { benchmark, value, grade, source, ...extra };
}

/** A conflicted figure: `value` is the LOW (composite input); the full [low, high] range is kept. */
function cf(
  benchmark: BenchmarkId,
  low: number,
  high: number,
  source: string,
  extra: FigureExtras = {},
): ConflictedFigure {
  return { benchmark, value: low, grade: "conflicted", low, high, source, ...extra };
}

function met(input: number, output: number, grade: EvidenceGrade, source: string, conditions?: string): MeteredPrice {
  return { kind: "metered", input, output, grade, source, conditions };
}

/**
 * OpenCode Go flat-rate subscription: $5 first month then $10/mo, with usage caps. Graded
 * "verified" — the plan cost and caps are OpenCode's own official published docs, the same grade
 * used elsewhere in this dataset for a harness's own official pricing page (e.g. the OpenCode Zen
 * passthrough rates, `met(..., V, URL...)` below).
 */
function goSubscription(): SubscriptionPrice {
  return {
    kind: "subscription",
    planCostUsd: 10,
    grade: "verified",
    caps: "First month $5, then $10/month. Usage caps: $12/5hr · $30/week · $60/month.",
    source: URL.opencodeGo,
  };
}

const V = "verified";
const XAI_DBL = "xAI doubles all rates once a prompt reaches 200k tokens (applied to the whole request).";
const ZEN_PASS = "OpenCode Zen passthrough at the vendor rate.";

// ─── Models (Appendix A.2 roster, 38 rows) ────────────────────────────────────────────────

export const dataset: Dataset = {
  snapshotDate: "2026-07-28",
  anchorIds: { opus: OPUS_ANCHOR_ID, sonnet: SONNET_ANCHOR_ID },
  models: [
    // ══════════════════════════════════════════
    // Anthropic
    // ══════════════════════════════════════════
    {
      id: "claude-fable-5",
      name: "Claude Fable 5",
      vendor: "Anthropic",
      harnesses: ["claude-code", "cursor", "opencode-zen"],
      figures: [
        fig("swe-bench-verified", 95.0, "self-reported", URL.anthropicModels, { benchmarkVersion: "Verified" }),
        fig("swe-bench-pro", 80.3, "self-reported", URL.anthropicModels, { benchmarkVersion: "Pro" }),
        fig("terminal-bench-2-1", 84.3, "self-reported", URL.anthropicModels, { benchmarkVersion: "2.1" }),
      ],
      pricing: {
        "claude-code": met(10, 50, V, URL.anthropic),
        cursor: met(10, 50, V, URL.anthropic, "Cursor passthrough."),
        "opencode-zen": met(10, 50, V, URL.anthropic, ZEN_PASS),
      },
    },
    {
      id: OPUS_ANCHOR_ID, // claude-opus-5 — OPUS anchor
      name: "Claude Opus 5",
      vendor: "Anthropic",
      harnesses: ["claude-code", "cursor", "opencode-zen"],
      figures: [
        fig("swe-bench-verified", 96.0, "self-reported", URL.anthropicModels, {
          benchmarkVersion: "Verified",
          conditions: "Self-reported 2026-07-24.",
        }),
        // GPQA Diamond is conflicted (K-2): three sources, three numbers, no primary. LOW enters.
        cf("gpqa-diamond", 93.2, 94.3, URL.anthropicModels, {
          benchmarkVersion: "Diamond",
          conditions: "Three secondary sources, three numbers, no primary (K-2).",
        }),
        // Terminal-Bench 2.1: K-1 — not captured. Absent (not zero).
      ],
      pricing: {
        "claude-code": met(5, 25, V, URL.anthropic),
        cursor: met(5, 25, V, URL.anthropic, "Cursor passthrough."),
        "opencode-zen": met(5, 25, V, URL.anthropic, ZEN_PASS),
      },
    },
    {
      id: "claude-opus-4-8",
      name: "Claude Opus 4.8",
      vendor: "Anthropic",
      harnesses: ["claude-code", "cursor", "opencode-zen"],
      figures: [
        fig("swe-bench-verified", 88.6, "verified", URL.anthropicModels, { benchmarkVersion: "Verified" }),
        fig("swe-bench-pro", 69.2, "verified", URL.swePro, { benchmarkVersion: "Pro", conditions: "Scale AI SEAL." }),
      ],
      pricing: {
        "claude-code": met(5, 25, V, URL.anthropic),
        cursor: met(5, 25, V, URL.anthropic, "Cursor passthrough."),
        "opencode-zen": met(5, 25, V, URL.anthropic, ZEN_PASS),
      },
    },
    {
      id: SONNET_ANCHOR_ID, // claude-sonnet-5 — SONNET anchor
      name: "Claude Sonnet 5",
      vendor: "Anthropic",
      harnesses: ["claude-code", "cursor", "opencode-zen"],
      figures: [
        fig("swe-bench-verified", 85.2, "self-reported", URL.anthropicModels, {
          benchmarkVersion: "Verified",
          conditions: "Official launch post.",
        }),
        fig("swe-bench-pro", 63.2, "self-reported", URL.anthropicModels, { benchmarkVersion: "Pro" }),
        fig("terminal-bench-2-1", 80.4, "self-reported", URL.anthropicModels, {
          benchmarkVersion: "2.1",
          conditions: "Official.",
        }),
      ],
      // DD-17a: intro $2/$10 through 2026-08-31; standard $3/$15 from 2026-09-01 is published.
      pricing: {
        "claude-code": met(
          3,
          15,
          V,
          URL.anthropic,
          "Intro $2/$10 through 2026-08-31; standard $3/$15 from 2026-09-01.",
        ),
        cursor: met(
          3,
          15,
          V,
          URL.anthropic,
          "Intro $2/$10 through 2026-08-31; standard $3/$15 from 2026-09-01. Cursor passthrough.",
        ),
        "opencode-zen": met(
          3,
          15,
          V,
          URL.anthropic,
          "Standard $3/$15 (DD-17a); Zen currently displays the $2/$10 promo.",
        ),
      },
    },
    {
      id: "claude-sonnet-4-6",
      name: "Claude Sonnet 4.6",
      vendor: "Anthropic",
      harnesses: ["claude-code", "cursor", "opencode-zen"],
      figures: [
        fig("swe-bench-verified", 79.6, "secondary", URL.sweVerified, { benchmarkVersion: "Verified" }),
        // GPQA conflicted: adaptive (89.9) vs standard (74.1) thinking. LOW (standard) enters.
        cf("gpqa-diamond", 74.1, 89.9, URL.anthropicModels, {
          benchmarkVersion: "Diamond",
          conditions: "Adaptive thinking 89.9% vs standard thinking 74.1% — record the condition.",
        }),
      ],
      pricing: {
        "claude-code": met(3, 15, V, URL.anthropic),
        cursor: met(3, 15, V, URL.anthropic, "Cursor passthrough."),
        "opencode-zen": met(3, 15, V, URL.anthropic, ZEN_PASS),
      },
    },
    {
      id: "claude-haiku-4-5",
      name: "Claude Haiku 4.5",
      vendor: "Anthropic",
      harnesses: ["claude-code", "cursor", "opencode-zen"],
      figures: [
        fig("swe-bench-verified", 73.3, "verified", URL.anthropicModels, { benchmarkVersion: "Verified" }),
        fig("swe-bench-pro", 39.5, "secondary", URL.swePro, { benchmarkVersion: "Pro" }),
        // GPQA conflicted: 74.1% and 67.2% both circulate. LOW (67.2) enters.
        cf("gpqa-diamond", 67.2, 74.1, URL.anthropicModels, {
          benchmarkVersion: "Diamond",
          conditions: "74.1% and 67.2% both circulate.",
        }),
      ],
      pricing: {
        "claude-code": met(1, 5, V, URL.anthropic),
        cursor: met(1, 5, V, URL.anthropic, "Cursor passthrough."),
        "opencode-zen": met(1, 5, V, URL.anthropic, ZEN_PASS),
      },
    },
    // ══════════════════════════════════════════
    // OpenAI
    // ══════════════════════════════════════════
    {
      id: "gpt-5.6-sol",
      name: "GPT-5.6 Sol",
      vendor: "OpenAI",
      harnesses: ["codex-cli", "cursor", "opencode-zen"],
      figures: [
        // SWE-bench Verified: K-3 — vendor moved to SWE-bench Pro; the aggregator's 96.2% is NOT
        // transcribed. No Verified figure.
        fig("terminal-bench-2-1", 91.9, "self-reported", URL.openaiModels, {
          benchmarkVersion: "2.1",
          conditions: '"Ultra" effort setting.',
        }),
        fig("gpqa-diamond", 94.1, "secondary", URL.gpqa, {
          benchmarkVersion: "Diamond",
          conditions: "Max effort; flagged unverified in source.",
        }),
      ],
      pricing: {
        "codex-cli": met(5, 30, V, URL.openai),
        cursor: met(5, 30, V, URL.openai, "Cursor passthrough."),
        "opencode-zen": met(5, 30, V, URL.openai, ZEN_PASS),
      },
      notes: [
        {
          modelId: "gpt-5.6-sol",
          text: 'METR reported GPT-5.6 Sol "gamed its software engineering evaluation at the highest detected rate in the organization\'s history."',
          source: "https://metr.org",
        },
      ],
    },
    {
      id: "gpt-5.6-terra",
      name: "GPT-5.6 Terra",
      vendor: "OpenAI",
      harnesses: ["codex-cli", "cursor", "opencode-zen"],
      figures: [fig("terminal-bench-2-1", 87.4, "self-reported", URL.openaiModels, { benchmarkVersion: "2.1" })],
      pricing: {
        "codex-cli": met(2.5, 15, V, URL.openai),
        cursor: met(2.5, 15, V, URL.openai, "Cursor passthrough."),
        "opencode-zen": met(2.5, 15, V, URL.openai, ZEN_PASS),
      },
    },
    {
      id: "gpt-5.6-luna",
      name: "GPT-5.6 Luna",
      vendor: "OpenAI",
      harnesses: ["codex-cli", "cursor", "opencode-zen"],
      figures: [fig("terminal-bench-2-1", 84.7, "self-reported", URL.openaiModels, { benchmarkVersion: "2.1" })],
      pricing: {
        "codex-cli": met(1, 6, V, URL.openai),
        cursor: met(1, 6, V, URL.openai, "Cursor passthrough."),
        "opencode-zen": met(1, 6, V, URL.openai, ZEN_PASS),
      },
    },
    {
      id: "gpt-5.5",
      name: "GPT-5.5",
      vendor: "OpenAI",
      harnesses: ["codex-cli", "cursor", "opencode-zen"],
      figures: [],
      pricing: {
        "codex-cli": met(5, 30, V, URL.openai),
        cursor: met(5, 30, V, URL.openai, "Cursor passthrough."),
        "opencode-zen": met(5, 30, V, URL.openai, ZEN_PASS),
      },
    },
    {
      id: "gpt-5.5-pro",
      name: "GPT-5.5 Pro",
      vendor: "OpenAI",
      harnesses: ["opencode-zen"],
      figures: [],
      pricing: { "opencode-zen": met(30, 180, V, URL.openai, ZEN_PASS) },
    },
    {
      id: "gpt-5.4",
      name: "GPT-5.4",
      vendor: "OpenAI",
      harnesses: ["codex-cli", "cursor", "opencode-zen"],
      figures: [],
      pricing: {
        "codex-cli": met(2.5, 15, V, URL.openai),
        cursor: met(2.5, 15, V, URL.openai, "Cursor passthrough."),
        "opencode-zen": met(2.5, 15, V, URL.openai, ZEN_PASS),
      },
    },
    {
      id: "gpt-5.4-mini",
      name: "GPT-5.4 Mini",
      vendor: "OpenAI",
      harnesses: ["codex-cli", "cursor", "opencode-zen"],
      figures: [],
      pricing: {
        "codex-cli": met(0.75, 4.5, V, URL.openai),
        cursor: met(0.75, 4.5, V, URL.openai, "Cursor passthrough."),
        "opencode-zen": met(0.75, 4.5, V, URL.openai, ZEN_PASS),
      },
    },
    {
      id: "gpt-5.4-nano",
      name: "GPT-5.4 Nano",
      vendor: "OpenAI",
      harnesses: ["cursor", "opencode-zen"],
      figures: [],
      pricing: {
        cursor: met(0.2, 1.25, V, URL.openai, "Cursor passthrough."),
        "opencode-zen": met(0.2, 1.25, V, URL.openai, ZEN_PASS),
      },
    },
    {
      id: "gpt-5.3-codex-spark",
      name: "GPT-5.3 Codex Spark",
      vendor: "OpenAI",
      harnesses: ["codex-cli", "opencode-zen"],
      figures: [],
      pricing: {
        "codex-cli": met(1.75, 14, V, URL.openai, "ChatGPT Pro only, research preview."),
        "opencode-zen": met(1.75, 14, V, URL.openai, ZEN_PASS),
      },
    },
    // ══════════════════════════════════════════
    // Google
    // ══════════════════════════════════════════
    {
      id: "gemini-3.6-flash",
      name: "Gemini 3.6 Flash",
      vendor: "Google",
      harnesses: ["cursor", "opencode-zen"],
      figures: [fig("terminal-bench-2-1", 78.0, "secondary", URL.terminalBench, { benchmarkVersion: "2.1" })],
      pricing: {
        cursor: met(1.5, 7.5, V, URL.google, "Cursor passthrough."),
        "opencode-zen": met(1.5, 7.5, V, URL.google, ZEN_PASS),
      },
    },
    {
      id: "gemini-3.5-flash",
      name: "Gemini 3.5 Flash",
      vendor: "Google",
      harnesses: ["cursor", "opencode-zen"],
      figures: [],
      pricing: {
        cursor: met(1.5, 9, V, URL.google, "Cursor passthrough."),
        "opencode-zen": met(1.5, 9, V, URL.google, ZEN_PASS),
      },
    },
    {
      id: "gemini-3.5-flash-lite",
      name: "Gemini 3.5 Flash Lite",
      vendor: "Google",
      harnesses: ["opencode-zen"],
      figures: [],
      pricing: { "opencode-zen": met(0.3, 2.5, V, URL.google, ZEN_PASS) },
    },
    {
      id: "gemini-3.1-pro",
      name: "Gemini 3.1 Pro",
      vendor: "Google",
      harnesses: ["cursor", "opencode-zen"],
      figures: [
        fig("swe-bench-verified", 80.6, "self-reported", URL.googleModels, {
          benchmarkVersion: "Verified",
          conditions: "Model card.",
        }),
        // GPQA conflicted: 94.1–94.3 range. LOW enters.
        cf("gpqa-diamond", 94.1, 94.3, URL.googleModels, { benchmarkVersion: "Diamond" }),
      ],
      // No transcribable standard-tier price for 3.1 Pro in Appendix A.4 (only 3.6/3.5 Flash and
      // the 2.5 line are priced). Omitted rather than invented; benchmark data retained.
      pricing: {},
    },
    {
      id: "gemini-3-flash",
      name: "Gemini 3 Flash",
      vendor: "Google",
      harnesses: ["cursor", "opencode-zen"],
      figures: [
        // SWE-bench Verified conflicted: 76.2–78.0 range across sources. LOW (76.2) enters.
        cf("swe-bench-verified", 76.2, 78.0, URL.sweVerified, {
          benchmarkVersion: "Verified",
          conditions: "Range across sources.",
        }),
      ],
      // No standard-tier price for bare "Gemini 3 Flash" in Appendix A.4. Omitted, not invented.
      pricing: {},
    },
    // ══════════════════════════════════════════
    // xAI
    // ══════════════════════════════════════════
    {
      id: "grok-4.5",
      name: "Grok 4.5",
      vendor: "xAI",
      harnesses: ["cursor", "opencode-go", "opencode-zen"],
      figures: [
        // SWE-bench Verified: vendor moved to Pro — no Verified figure (do not transcribe).
        fig("swe-bench-pro", 64.7, "self-reported", URL.xai, { benchmarkVersion: "Pro" }),
        fig("terminal-bench-2-1", 83.3, "self-reported", URL.xai, { benchmarkVersion: "2.1" }),
        // GPQA Diamond: K-4 — vendors omit. Absent.
      ],
      pricing: {
        cursor: met(2, 6, V, URL.cursor, "Base rate; $4/$18 fast. " + XAI_DBL),
        "opencode-go": goSubscription(),
        "opencode-zen": met(2, 6, V, URL.xai, ZEN_PASS + " " + XAI_DBL),
      },
    },
    {
      id: "grok-build-0.1",
      name: "grok-build-0.1",
      vendor: "xAI",
      harnesses: ["opencode-zen"],
      figures: [],
      pricing: { "opencode-zen": met(1, 2, V, URL.xai, ZEN_PASS + " " + XAI_DBL) },
    },
    // ══════════════════════════════════════════
    // Cursor (own models)
    // ══════════════════════════════════════════
    {
      id: "cursor-composer-2.5",
      name: "Cursor Composer 2.5",
      vendor: "Cursor",
      harnesses: ["cursor"],
      // 79.8% is SWE-bench Multilingual (different benchmark) — NOT in swe-bench-verified.
      // 69.3% is Terminal-Bench 2.0 — NOT in terminal-bench-2-1. GPQA not published.
      // All four composite benchmarks absent → coverage 0, unrated band.
      figures: [],
      pricing: {
        cursor: met(0.5, 2.5, V, URL.cursor, "Standard rate; $3.00/$15.00 fast. Released 2026-05-18."),
      },
    },
    {
      id: "cursor-composer-1",
      name: "Cursor Composer 1",
      vendor: "Cursor",
      harnesses: ["cursor"],
      figures: [],
      pricing: { cursor: met(1.25, 10, V, URL.cursor) },
    },
    // ══════════════════════════════════════════
    // Z.ai (GLM)
    // ══════════════════════════════════════════
    {
      id: "glm-5.2",
      name: "GLM 5.2",
      vendor: "Z.ai",
      harnesses: ["cursor", "opencode-go", "opencode-zen"],
      figures: [
        fig("swe-bench-pro", 62.1, "secondary", URL.swePro, { benchmarkVersion: "Pro" }),
        // Terminal-Bench 2.1 conflicted: 82.7 vs ~81.0 circulates. LOW (~81.0) enters.
        cf("terminal-bench-2-1", 81.0, 82.7, URL.terminalBench, {
          benchmarkVersion: "2.1",
          conditions: "82.7% and ≈81.0% both circulate.",
        }),
        fig("gpqa-diamond", 91.2, "secondary", URL.gpqa, { benchmarkVersion: "Diamond" }),
      ],
      pricing: {
        cursor: met(1.4, 4.4, V, URL.zai, "Cursor passthrough."),
        "opencode-go": goSubscription(),
        "opencode-zen": met(1.4, 4.4, V, URL.zai, ZEN_PASS),
      },
    },
    {
      id: "glm-5.1",
      name: "GLM 5.1",
      vendor: "Z.ai",
      harnesses: ["opencode-go", "opencode-zen"],
      // GLM-5.1 Verified not captured (Appendix A.3 note). No benchmark figures.
      figures: [],
      pricing: {
        "opencode-go": goSubscription(),
        "opencode-zen": met(1.4, 4.4, V, URL.zai, ZEN_PASS),
      },
    },
    // ══════════════════════════════════════════
    // Moonshot (Kimi)
    // ══════════════════════════════════════════
    {
      id: "kimi-k3",
      name: "Kimi K3",
      vendor: "Moonshot",
      harnesses: ["cursor", "opencode-go", "opencode-zen"],
      figures: [
        fig("swe-bench-verified", 76.8, "secondary", URL.sweVerified, { benchmarkVersion: "Verified" }),
        fig("terminal-bench-2-1", 88.3, "secondary", URL.terminalBench, { benchmarkVersion: "2.1" }),
        fig("gpqa-diamond", 93.5, "secondary", URL.gpqa, { benchmarkVersion: "Diamond" }),
      ],
      pricing: {
        cursor: met(3, 15, V, URL.kimi, "Cursor passthrough."),
        "opencode-go": goSubscription(),
        "opencode-zen": met(3, 15, V, URL.kimi, ZEN_PASS),
      },
    },
    {
      id: "kimi-k2.7-code",
      name: "Kimi K2.7 Code",
      vendor: "Moonshot",
      harnesses: ["cursor", "opencode-go", "opencode-zen"],
      figures: [],
      // K-6: official Moonshot pricing page did not return content. Zen passthrough ($0.95/$4.00)
      // is recorded as secondary; the official direct rate remains unavailable.
      pricing: {
        cursor: met(
          0.95,
          4,
          "secondary",
          URL.kimi,
          "K-6: official rate not retrievable; Cursor passthrough of Zen rate.",
        ),
        "opencode-go": goSubscription(),
        "opencode-zen": met(
          0.95,
          4,
          "secondary",
          URL.opencodeZen,
          "K-6: official Moonshot rate not retrievable; Zen passthrough.",
        ),
      },
    },
    {
      id: "kimi-k2.6",
      name: "Kimi K2.6",
      vendor: "Moonshot",
      harnesses: ["opencode-go", "opencode-zen"],
      figures: [
        fig("swe-bench-verified", 80.2, "secondary", URL.sweVerified, { benchmarkVersion: "Verified" }),
        fig("swe-bench-pro", 58.6, "secondary", URL.swePro, { benchmarkVersion: "Pro" }),
      ],
      pricing: {
        "opencode-go": goSubscription(),
        "opencode-zen": met(0.95, 4, V, URL.kimi, ZEN_PASS),
      },
    },
    // ══════════════════════════════════════════
    // MiniMax
    // ══════════════════════════════════════════
    {
      id: "minimax-m3",
      name: "MiniMax M3",
      vendor: "MiniMax",
      harnesses: ["opencode-go", "opencode-zen"],
      figures: [
        fig("swe-bench-verified", 80.5, "secondary", URL.sweVerified, { benchmarkVersion: "Verified" }),
        fig("swe-bench-pro", 59.0, "secondary", URL.swePro, { benchmarkVersion: "Pro" }),
        fig("terminal-bench-2-1", 66.0, "secondary", URL.terminalBench, { benchmarkVersion: "2.1" }),
      ],
      // DD-17a: "permanent 50% off" has no stated end date → publish the effective $0.30/$1.20.
      pricing: {
        "opencode-go": goSubscription(),
        "opencode-zen": met(
          0.3,
          1.2,
          V,
          URL.minimax,
          ZEN_PASS + ' "Permanent 50% off" a $0.60/$2.40 list; no stated end date.',
        ),
      },
    },
    {
      id: "minimax-m2.7",
      name: "MiniMax M2.7",
      vendor: "MiniMax",
      harnesses: ["opencode-go", "opencode-zen"],
      figures: [],
      pricing: {
        "opencode-go": goSubscription(),
        "opencode-zen": met(0.3, 1.2, V, URL.minimax, ZEN_PASS),
      },
    },
    // ══════════════════════════════════════════
    // Alibaba (Qwen)
    // ══════════════════════════════════════════
    {
      id: "qwen3.7-max",
      name: "Qwen3.7 Max",
      vendor: "Alibaba",
      harnesses: ["opencode-go", "opencode-zen"],
      figures: [
        fig("swe-bench-verified", 80.4, "secondary", URL.sweVerified, {
          benchmarkVersion: "Verified",
          conditions: "Flagged unverified in source.",
        }),
      ],
      // International (Singapore) endpoint. "Limited-time 50% off" with no stated end date.
      pricing: {
        "opencode-go": goSubscription(),
        "opencode-zen": met(
          2.5,
          7.5,
          V,
          URL.alibaba,
          ZEN_PASS + ' Singapore endpoint; "limited-time 50% off", no end date.',
        ),
      },
    },
    {
      id: "qwen3.7-plus",
      name: "Qwen3.7 Plus",
      vendor: "Alibaba",
      harnesses: ["opencode-go", "opencode-zen"],
      figures: [],
      pricing: {
        "opencode-go": goSubscription(),
        "opencode-zen": met(0.4, 1.6, V, URL.alibaba, ZEN_PASS + " Singapore endpoint, 0–256k band."),
      },
    },
    {
      id: "qwen3.6-plus",
      name: "Qwen3.6 Plus",
      vendor: "Alibaba",
      harnesses: ["opencode-go", "opencode-zen"],
      figures: [],
      pricing: {
        "opencode-go": goSubscription(),
        "opencode-zen": met(0.5, 3, V, URL.alibaba, ZEN_PASS),
      },
    },
    // ══════════════════════════════════════════
    // DeepSeek
    // ══════════════════════════════════════════
    {
      id: "deepseek-v4-pro",
      name: "DeepSeek V4 Pro",
      vendor: "DeepSeek",
      harnesses: ["opencode-go", "opencode-zen"],
      figures: [
        fig("swe-bench-verified", 80.6, "secondary", URL.sweVerified, { benchmarkVersion: "Verified" }),
        fig("gpqa-diamond", 90.1, "secondary", URL.gpqa, { benchmarkVersion: "Diamond" }),
      ],
      pricing: {
        "opencode-go": goSubscription(),
        // Zen marks this up ~4x vs DeepSeek's direct rate — DD-16 worked example. Both numbers
        // are recorded: the Zen rate as the metered value, the direct rate in `conditions`.
        "opencode-zen": met(
          1.74,
          3.48,
          V,
          URL.opencodeZen,
          "Direct from DeepSeek: $0.435 input / $0.87 output per 1M tokens.",
        ),
      },
    },
    {
      id: "deepseek-v4-flash",
      name: "DeepSeek V4 Flash",
      vendor: "DeepSeek",
      harnesses: ["opencode-go", "opencode-zen"],
      figures: [fig("swe-bench-verified", 79.0, "secondary", URL.sweVerified, { benchmarkVersion: "Verified" })],
      pricing: {
        "opencode-go": goSubscription(),
        "opencode-zen": met(0.14, 0.28, V, URL.deepseek, ZEN_PASS),
      },
    },
    // ══════════════════════════════════════════
    // Xiaomi (MiMo)
    // ══════════════════════════════════════════
    {
      id: "mimo-v2.5",
      name: "MiMo v2.5",
      vendor: "Xiaomi",
      harnesses: ["opencode-go", "opencode-zen"],
      figures: [],
      // No Xiaomi per-token pricing in Appendix A.4; OpenCode Go carries it on subscription.
      // Zen rate not transcribable → only the GO subscription entry is recorded.
      pricing: { "opencode-go": goSubscription() },
    },
    {
      id: "mimo-v2.5-pro",
      name: "MiMo v2.5 Pro",
      vendor: "Xiaomi",
      harnesses: ["opencode-go"],
      figures: [],
      pricing: { "opencode-go": goSubscription() },
    },
  ],
};
