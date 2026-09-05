import type { Locale } from "./config";

const translations: Record<Locale, Record<string, string>> = {
  en: {
    readMore: "Read More",
    lastUpdated: "Last updated",
    publishedOn: "Published on",
    author: "Author",
    tags: "Tags",
    categories: "Categories",
    share: "Share",
    relatedContent: "Related Content",
    openSourceProject: "Open-Source Project",
    search: "Search...",
    onThisPage: "On this page",
    previous: "Previous",
    next: "Next",
    noResults: "No results found",
    toggleTheme: "Toggle theme",
    skipToContent: "Skip to content",
    toolsPageTitle: "Tools",
    toolsPageCalcLink: "Cost of Living Calculator",
    toolsPageCalcDesc: "Compare monthly living costs, savings, and the minimum role needed across cities.",
    toolsPageAiBenchLink: "AI Model Benchmark",
    toolsPageAiBenchDesc:
      "Compare coding-agent models by capability, class, and per-token price, every figure sourced.",
    breadcrumbHome: "Home",
    breadcrumbCalculator: "Calculator",

    // AI benchmark — page shell, data table, honesty surface, and provenance.
    // Every aiBench* key MUST exist in both locales (AC-35): a missing key renders as its
    // raw identifier, and the page test asserts no "aiBench" token leaks into rendered text.
    aiBenchTitle: "AI Model Benchmark",
    // Rule-15 UWT-003 fix (2026-07-30): reworded away from "roster-relative" — that term's own
    // definition ("normalized to the strongest model on this roster") lived several bullets into
    // the collapsed "How to read this benchmark" box, which a reader can skip entirely, so the very
    // first sentence on the page used an undefined term. This wording states the same fact
    // ("scored relative to each other", not against an absolute standard) in plain language.
    // Rule-15 UWT-004 fix (2026-07-30): "harness" is the FIRST technical term on the page (right
    // here, in the subtitle) and was never glossed anywhere — a first-time reader unfamiliar with
    // coding-agent tooling had no way to learn what it means. The parenthetical below glosses it at
    // its first use, rather than only inside the collapsed "How to read" box or the filter label.
    aiBenchSubtitle:
      "An index of coding-agent models scored relative to each other across five harnesses (the CLI or IDE tools used to run them), with every figure sourced.",
    aiBenchSnapshotLabel: "Data snapshot",
    aiBenchTableCaption:
      "Coding-agent model roster: capability figures, composite index, coverage, and per-harness prices.",
    aiBenchColModel: "Model",
    aiBenchColVendor: "Vendor",
    aiBenchColHarnesses: "Harnesses",
    aiBenchColClass: "Class",
    aiBenchBenchSweVerified: "SWE-bench Verified",
    aiBenchBenchSwePro: "SWE-bench Pro",
    aiBenchBenchTerminalBench: "Terminal-Bench 2.1",
    aiBenchBenchGpqa: "GPQA Diamond",
    aiBenchColIndex: "Composite index",
    aiBenchColCoverage: "Coverage",
    aiBenchColInputPrice: "Input price",
    aiBenchColOutputPrice: "Output price",
    aiBenchBandOpus: "Opus",
    aiBenchBandSonnet: "Sonnet",
    // "Haiku" is deliberately untranslated in `id` (see the `id` block below), for the same
    // reason `aiBenchBandOpus`/`aiBenchBandSonnet` already are — it is a model-tier proper noun
    // (DD-35), not the common-noun adjective this now-retired band's own Indonesian value used
    // to be, before the rename.
    aiBenchBandHaiku: "Haiku",
    aiBenchBandUnrated: "Unrated",
    aiBenchNoFigure: "Not reported",
    aiBenchSubscription: "Subscription",
    // Rule-15 UWT-016 fix: the detail-region label for a subscription's usage-cap text (plan
    // ramp/caps), surfaced as its own field so a model's own row/card discloses it directly.
    aiBenchSubscriptionTerms: "Subscription terms",
    aiBenchCoverageLow: "low coverage",
    aiBenchGradeVerified: "verified",
    aiBenchGradeSelfReported: "self-reported",
    aiBenchGradeSecondary: "secondary",
    aiBenchGradeConflicted: "conflicted",
    aiBenchGradeUnavailable: "unavailable",
    aiBenchEvidenceLabel: "Evidence grade",
    aiBenchSourceLabel: "Source",
    aiBenchRangeSeparator: "to",
    aiBenchPriceUnit: "per 1M tokens",
    aiBenchIntegrityLabel: "Integrity note",
    // Rule-15 UWT-010 fix: the `<summary>` for the always-reachable, click-to-reveal claim text.
    aiBenchIntegrityDetailsSummary: "Read the finding",
    // DD-33 item 1 (Phase 6, cycle 6.1) — the roster card's <summary> disclosure label. Genuinely
    // new copy: no existing key names "reveal the rest of this model's figures".
    aiBenchCardAllFigures: "All figures",
    // DD-33 item 3/4 (Phase 6, cycle 6.6) — the two field-group headings DD-34 Treatment 3 adds.
    // Genuinely new copy: no existing key names either heading.
    aiBenchCardGroupModel: "Model",
    aiBenchCardGroupScores: "Scores",
    aiBenchHowToSummary: "How to read this benchmark (please read before comparing models)",
    aiBenchHowToVendorReported:
      "Most frontier benchmark scores are vendor self-reported. On SWE-bench Verified, independent reproduction (METR) confirmed 0 of 104 vendor-claimed tasks — treat unverified scores as upper bounds, not measured facts.",
    aiBenchHowToIndexRelative:
      "The composite index is roster-relative: each score is normalized to the strongest model on this roster, not to an absolute standard. The per-benchmark weights are our judgement, not a property of the benchmarks.",
    aiBenchHowToCoverage:
      "Coverage varies. A model scored on one of the four benchmarks rests on far less evidence than one scored on all four; low-coverage models are marked so the index is not mistaken for equal-confidence.",
    aiBenchHowToBestConfig:
      "Every figure reflects the vendor's best published configuration (effort setting, prompt, and harness). A model's everyday performance may be lower; the figure is a ceiling, not a typical.",
    // Rule-15 UWT-005 fix (2026-07-30): the example named "ARC-AGI-2" alongside GPQA Diamond, but
    // ARC-AGI-2 is not one of the four benchmarks that actually feed the composite index (see
    // `aiBenchLegendCoverageFormula` below: SWE-bench Verified, SWE-bench Pro, Terminal-Bench 2.1,
    // GPQA Diamond) — a reader who checked the claim against the data table found no ARC-AGI-2
    // column anywhere. Swapped in SWE-bench Pro, one of the four benchmarks actually scored.
    aiBenchHowToArcConflict:
      "Why provenance matters: SWE-bench Pro / GPQA Diamond scores for the same model disagree across sources. Where published values conflict we show the full range and the low end enters the index — never an averaged middle value.",
    aiBenchHowToPriceGap:
      "Why prices are per-harness: DeepSeek V4 Pro costs about one quarter as much direct from DeepSeek as through a gateway that marks the rate up. Each price names the harness that charges it; there is no single 'the price'.",
    // Rule-15 UWT-013 fix: no unit basis (per-token/per-1K/per-million) was disclosed anywhere on
    // the page for the ~80 dollar figures shown. Reuses the wording already defined in
    // `aiBenchPriceUnit` (a key that existed but was never rendered anywhere) so the two stay
    // word-for-word consistent.
    aiBenchHowToPriceUnit:
      "Unless marked Subscription, every dollar figure is priced per 1M tokens — a Subscription figure is a flat monthly rate with its own usage caps, not a per-token rate.",
    aiBenchSourcesHeading: "Sources and licences",
    aiBenchSourcesIntro:
      "Every figure links to the leaderboard or vendor page it came from. These are the benchmark operators whose figures appear here, with their republication terms.",
    aiBenchOpTermsSwebench:
      "Benchmark code and dataset are MIT-licensed; the leaderboard page itself is marked all rights reserved.",
    aiBenchOpTermsTerminalbench: "No republication terms stated by the operator.",
    aiBenchOpTermsGpqa: "The GPQA benchmark repository is MIT-licensed.",
    aiBenchOpTermsNone: "No republication terms stated by the operator.",

    // AI benchmark — legend (Rule-15 UWT-002/UWT-003/UWT-005/USS-002 fix): a visible, always
    // -available definition of the class taxonomy and evidence grades, plus the coverage formula.
    aiBenchLegendHeading: "Class and evidence-grade legend",
    aiBenchLegendClassIntro:
      "The four capability classes are anchor-relative composite-index tiers, not vendor brand names — a model of any vendor can land in any class:",
    aiBenchLegendClassOpus: "at or above Claude Opus 5's own composite index (the tier's defining anchor).",
    aiBenchLegendClassSonnet: "at or above Claude Sonnet 5's own composite index, below the Opus anchor.",
    aiBenchLegendClassHaiku: "below the Sonnet anchor.",
    aiBenchLegendClassUnrated: "no figure on any of the four composite benchmarks.",
    aiBenchLegendGradeIntro: "The five evidence grades describe how each figure was sourced:",
    aiBenchLegendGradeVerified: "scored by an independent verifier (e.g. Scale AI SEAL) or an official model card.",
    aiBenchLegendGradeSelfReported: "published by the vendor about its own model.",
    aiBenchLegendGradeSecondary: "quoted by an aggregator; no primary source retrieved.",
    aiBenchLegendGradeConflicted:
      "multiple irreconcilable published values — the cell shows the range, never an average.",
    aiBenchLegendGradeUnavailable: "the vendor publishes no figure for this benchmark.",
    aiBenchLegendCoverageFormula:
      "Coverage is the weighted share of the composite a model's reported benchmarks cover (SWE-bench Verified 25% + SWE-bench Pro 25% + Terminal-Bench 2.1 20% + GPQA Diamond 30% = 100%), not a simple count of benchmarks reported.",

    // AI benchmark — charts (Phase 6/7).
    aiBenchChartAxisMaxLabel: "Axis maximum",
    aiBenchPriceLowestSubtitle: "Showing the lowest available rate across harnesses for each model",

    // AI benchmark — merged chart (Phase 2).
    aiBenchMergedChartTitle: "Capability and price by model",
    aiBenchSortLabel: "Sort",
    aiBenchSortCapability: "Capability (high to low)",
    aiBenchSortPriceAsc: "Price: Low to High",
    aiBenchSortPriceDesc: "Price: High to Low",
    // Rule-15 UWT-008 fix: clarifies this sort's scope, since the roster table below keeps its own,
    // independent row order rather than following a band's chart sort.
    aiBenchSortScopeNote: "(chart order only)",

    // AI benchmark — harness/class filters (Phase 8).
    aiBenchFilterSummary: "Filters",
    aiBenchFilterHarnessLabel: "Harness",
    aiBenchFilterClassLabel: "Class",
    aiBenchFilterAllHarnesses: "All harnesses",
    aiBenchFilterAllClasses: "All classes",
    // Rule-15 UWT-011 fix: the Class values reuse Anthropic's own tier names cross-vendor with no
    // inline hint anywhere the column/filter itself appears — this is that hint, linking to the
    // always-reachable (if collapsed) legend.
    aiBenchClassHint: "What do these mean?",
    aiBenchFilterResultCountLabel: "Models shown",
    aiBenchFilterActiveCountLabel: "active",
    aiBenchEmptyStateTitle: "No models match these filters",
    aiBenchEmptyStateMessage: "Try a different harness or class filter.",
    // Rule-15 UWT-009 fix: a single RATED band (Opus/Sonnet/Haiku) can be emptied by an active
    // Class filter even while other bands still have models — distinct from `aiBenchEmptyStateTitle`
    // above, which covers the whole-roster empty state.
    aiBenchBandEmptyMessage: "No models in this class match the current filter.",

    // Calculator — page
    calcTitle: "Cost of Living Calculator",
    calcSubtitle: "Compare cost of living and salary savings across cities",
    ariaTabsNav: "Calculator tabs",
    tabCostOfLiving: "Cost of living",
    tabCostDesc: "Compare monthly living costs across cities",
    tabSavings: "Savings",
    tabSavingsDesc: "See how much you'd save",
    tabMinRole: "Minimum role",
    tabMinRoleDesc: "Find the min role you need",
    dataLastUpdated: "Data last updated",
    estimatesOnly: "Estimates only",

    // Calculator — disclaimers
    disclaimerPension: "Savings are before voluntary pension / retirement contributions.",
    disclaimerClothing: "Clothing and personal care are folded into lifestyle expenses.",
    disclaimerFx:
      "A positive USD savings figure does not mean equal purchasing power — USD uses a nominal FX snapshot, not PPP.",
    disclaimerSnapshot: "Data is a snapshot — verify current figures before making relocation decisions.",
    disclaimerTax:
      "Tax is a simplified effective rate (federal + sub-national for US/CA/CH only) — not a full bracket calculation; excludes filing status, deductions, benefits-in-kind, and contribution caps.",
    disclaimerHealthcare: "Healthcare models out-of-pocket costs only; the funding scheme is shown per country.",
    disclaimerRelocation:
      "Relocation sunk costs are a one-time estimate kept out of monthly savings math; the cash cushion is a reserve you keep, not a sunk cost.",
    disclaimerRoleSalary:
      "Role salary is modeled at the national (country) level — cities inherit their country's p25/median/p75 distribution.",
    disclaimerNonSalary:
      "Non-salary comp (RSU/equity + bonus) is informational total-comp context only, not part of the savings math.",

    // Calculator — geo filters
    labelRegion: "Region",
    labelCountry: "Country",
    labelCity: "City",
    optAllRegions: "All regions",
    optAllCountries: "All countries",
    optAllCities: "All cities",
    clearRegion: "Clear",
    regionAutoAdvisory: "Region updated automatically to match the selected country.",

    // Calculator — region display names (UWT-004). The serialized region KEY stays English
    // (URL stability); only these display labels are localized. MENA/Nordics are expanded.
    regionAsean: "ASEAN",
    regionJapan: "Japan",
    regionEurope: "Europe",
    regionNordics: "Nordics (Northern Europe)",
    regionAmericas: "Americas",
    regionMena: "MENA (Middle East & North Africa)",
    regionAsia: "Asia",
    regionOceania: "Oceania",
    regionAfrica: "Africa",

    // Calculator — controls
    labelAdults: "Adults",
    labelPreschoolKids: "Preschool children",
    labelSchoolKids: "School-age children",
    labelSchoolType: "School type",
    optPublic: "Public",
    optPrivate: "Private",
    schoolTypeHint: "add school-age children to choose",
    // UWT-015: native hover tooltip (title) on the disabled Public/Private buttons so a
    // first-timer learns the prerequisite without relying on the screen-reader-only hint.
    schoolTypeDisabledTitle: "Add a school-age child to enable this option",
    foreignerPublicSchoolNote:
      "Public school isn't open to foreign residents in every country; where it isn't (e.g. UAE, Singapore), the private-school cost is used instead.",
    publicSchoolForeignerFlag: "public n/a → private",
    publicSchoolForeignerFlagBadge: "Private — public not open to foreigners",
    labelArea: "Area",
    optCenter: "City center",
    optRural: "Rural",

    // Calculator — cost-of-living table
    colCountry: "Country",
    colCity: "City",
    colHealthcareScheme: "Healthcare scheme",
    tooltipHealthcareScheme:
      "How healthcare costs are funded in this country: tax-funded, mandatory payroll insurance, or out-of-pocket.",
    colHousing: "Housing",
    colFood: "Food",
    colTransport: "Transport",
    colUtilities: "Utilities",
    colHealthcareOOP: "Healthcare (OOP)",
    colHealthcareOOPPrefix: "Healthcare",
    colChildcare: "Childcare",
    colSchool: "School",
    colLifestyle: "Lifestyle",
    colEssentials: "Essentials",
    colTotal: "Total",
    previewMonthlyEstimate: "estimated monthly essentials",
    // UWT-006: labels the pre-populated min-role preview panel as illustrative.
    previewExampleLabel: "Example",
    colRelocationSunk: "Relocation (sunk)",
    colLiquidityReserve: "Liquidity reserve",
    tooltipRelocationSunk:
      "One-time sunk costs: rental deposit, key money, moving, and visa fees. Not a monthly expense.",
    tooltipLiquidityReserve:
      "Cash cushion you keep on hand — not a sunk cost. Covers first months before salary starts.",
    oopLegend: "OOP = out-of-pocket — healthcare you pay yourself, on top of any tax-funded or insurance coverage.",

    // Calculator — healthcare scheme badges
    healthcareTaxFunded: "tax-funded",
    healthcareMandatoryPayroll: "mandatory payroll insurance",
    healthcareOutOfPocket: "out-of-pocket",

    // Calculator — city detail
    sectionMonthlyExpenses: "Monthly expenses",
    sectionRelocationCosts: "Relocation costs",
    labelHousing: "Housing",
    labelFood: "Food",
    labelTransport: "Transport",
    labelUtilities: "Utilities",
    labelHealthcareOOP: "Healthcare (OOP)",
    labelChildcare: "Childcare",
    labelSchool: "School",
    labelEssentialsSubtotal: "Essentials subtotal",
    labelMonthlyTotal: "Monthly total",
    labelRelocationSunkCost: "One-time relocation sunk cost",
    labelLiquidityReserve: "Liquidity reserve (cash cushion — kept, not spent)",
    backToAllCities: "← Back to all cities",

    // Calculator — savings table
    savingsEmptyStateMessage: "Enter your gross monthly salary to see how much you could save in each city.",
    grossMonthlySalaryLabel: "Gross monthly salary (before tax)",
    salaryCurrencyIndicator: "Currency: USD",
    salaryCurrencyExplanation: "Salaries are compared in USD across all cities.",
    annualGrossLabel: "Annual gross",
    nonSalaryCompNote: "Non-salary comp (RSU/equity + bonus) is informational only — not in savings math.",
    colNet: "Net (monthly)",
    colSavingsEssential: "Savings after essentials ↕",
    colSavingsLifestyle: "Savings after lifestyle",
    colNonSalaryComp: "Typical non-salary comp (info, annual)",
    colTotalComp: "Total comp (info, annual)",
    sortBySavings: "Sort by savings",
    subNationalIndicator: "(fed+state)",

    // Calculator — min-role table
    labelBaselineSource: "How to set your target",
    optSavingsTarget: "Monthly savings target",
    optReferenceRole: "Match a role",
    optMySalary: "My salary",
    hintSavingsTarget: "Enter a monthly savings goal — the table marks the lowest role whose best city reaches it.",
    hintReferenceRole:
      "Pick a role and city as the yardstick — the table marks the lowest role that saves at least as much, no dollar figure needed.",
    hintMySalary:
      "Enter your current gross salary — the table marks the lowest role that saves at least what you do today.",
    labelMonthlySavingsTarget: "Monthly savings target",
    labelTargetCurrency: "Target currency",
    labelRefCity: "Reference city",
    labelRefRole: "Reference role",
    labelMyGrossMonthly: "My gross monthly",
    labelMySalaryCity: "My salary city",
    labelSalaryInputCurrency: "Salary currency",
    labelDisplayCurrency: "Display currency",
    rankBasisNote:
      "Ranking key: essential savings (housing + food + transport + utilities + healthcare + school). Lifestyle excluded — personal preference variable.",
    nonSalaryRankNote: "Non-salary comp (RSU / equity / bonus) is informational only — not used in ranking.",
    noQualifierMessage: "No role reaches this savings bar in any city.",
    minRoleEmptyStateMessage: "Enter a monthly savings target to see which roles reach it in each city.",
    seRolesCaption: "Roles: software-engineering (IC + management)",
    qualifyingDivider: "— roles below do not reach the savings bar —",
    moreBelowBar: "more (city, role) pairs below your bar (not shown)",
    colRole: "Role",
    colTrack: "Track",
    colBestCity: "Best city",
    colP25: "P25 (monthly)",
    colMedian: "Median",
    colP75: "P75",
    colEssentialSavings: "Essential savings",
    colNonSalaryCompInfo: "Non-salary comp",
    minimumMarker: "← min",
    // UWT-010: percentile gloss tooltips for the salary-distribution headers.
    tooltipP25: "25th-percentile monthly salary — a quarter of people in this role earn less.",
    tooltipMedian: "Median (50th-percentile) monthly salary for this role.",
    tooltipP75: "75th-percentile monthly salary — a quarter of people in this role earn more.",
    // UWT-013: expanded Track labels (the table renders these instead of bare "ic"/"mgmt").
    trackIc: "Individual contributor",
    trackMgmt: "Management",
    // UWT-003: gloss for the shortened "Non-salary comp" header.
    tooltipNonSalaryComp: "RSU/equity + bonus — annual total, informational only, not used in savings math.",

    // IA navigation revamp — landing homepage + global nav
    heroHeading: "Learn to build software, the clear way.",
    heroIntro:
      "AyoKoding is an open, bilingual learning hub for software engineering — practical guides, worked examples, and free tools that grow with you.",
    heroCtaLearn: "Start learning",
    heroCtaTools: "Explore tools",
    navLearn: "Learn",
    navTools: "Tools",
    browseTitle: "Browse",
    browseIntro: "Browse every AyoKoding section in one place.",
    sectionBlurbFallback: "Explore this section.",
    toolsTeaserKicker: "Tools",
    toolsTeaserTitle: "Cost of Living Calculator",
    toolsTeaserDesc: "Compare monthly living costs, savings, and the minimum role you need across cities.",
    toolsTeaserCta: "Open the calculator",
    footerLearn: "Learn",
    footerTools: "Tools",
    footerAbout: "About",
    footerBrowseAll: "Browse all",
    footerCalculator: "Cost of Living Calculator",
    footerAiBenchmark: "AI Model Benchmark",
    footerAboutAyokoding: "About AyoKoding",
    footerTerms: "Terms & Conditions",
    footerProject: "Project",
    sectionExploreHeading: "Explore",

    // Mobile nav drawer — preset width control
    mobileNavWidthLabel: "Drawer width",
    // UWT-005 fix (phase-5 rule-15 retest): ties the control to the real, concrete benefit a
    // first-time reader gets from it, rather than leaving "Drawer width" to speak for itself.
    mobileNavWidthHint: "Widen the drawer to read long path or course titles in full",
    mobileNavWidthDefault: "Default",
    mobileNavWidthWide: "Wide",

    // Course-paths feature chrome (DWT-003 fix, phase-5 rule-15 design-tester retest): these
    // static UI strings previously rendered as hardcoded English literals, never routing through
    // `t()`, so they stayed English even when the surrounding page (masthead, hero H1, section
    // headings) correctly rendered `id`. `brd.md`'s own non-goal only defers translating path/
    // course *data* — the feature's own interface chrome was always meant to localize.
    pathsChooseYourPath: "Choose your path",
    pathsCompareAllPaths: "Compare all paths",
    pathsExploreSkillsPaths: "Explore skills paths",
    pathsBrowseCourseLibrary: "Browse the full course library",
    pathsStart: "Start",
    pathsExploreArc: "Explore arc",
    pathsExploreArcRoles: "Explore this arc's roles",
    pathsSyllabus: "Syllabus",
    pathsPrerequisites: "Prerequisites",
    pathsCourseWordCapital: "Course",
    pathsCourseWordLower: "course",
    pathsOfWord: "of",
    pathsOnPathPrefix: "on path",
    pathsViewPath: "View path",
    pathsViewFullPath: "View full path",
    pathsBrowseAllCourses: "Browse all courses",

    // Resizable docs sidebar — drag/keyboard handle accessible name
    resizableSidebarHandleLabel: "Resize panel",

    // Code-block copy button — CodeBlock's copyLabel/copiedLabel/errorLabel (English default)
    copy: "Copy",
    copied: "Copied",
    copyFailed: "Copy failed",
  },
  id: {
    readMore: "Baca Selengkapnya",
    lastUpdated: "Terakhir diperbarui",
    publishedOn: "Dipublikasikan pada",
    author: "Penulis",
    tags: "Tag",
    categories: "Kategori",
    share: "Bagikan",
    relatedContent: "Konten Terkait",
    openSourceProject: "Proyek Open-Source",
    search: "Cari...",
    onThisPage: "Di halaman ini",
    previous: "Sebelumnya",
    next: "Selanjutnya",
    noResults: "Tidak ada hasil",
    toggleTheme: "Ubah tema",
    skipToContent: "Langsung ke konten",
    toolsPageTitle: "Alat",
    toolsPageCalcLink: "Kalkulator Biaya Hidup",
    toolsPageCalcDesc:
      "Bandingkan biaya hidup bulanan, tabungan, dan jabatan minimum yang dibutuhkan di berbagai kota.",
    toolsPageAiBenchLink: "Tolok Ukur Model AI",
    toolsPageAiBenchDesc:
      "Bandingkan model agen-koding berdasarkan kemampuan, kelas, dan harga per-token, setiap angka bersumber.",
    breadcrumbHome: "Beranda",
    breadcrumbCalculator: "Kalkulator",

    // AI benchmark — page shell, data table, honesty surface, and provenance.
    // Setiap kunci aiBench* HARUS ada di kedua bahasa (AC-35): kunci yang hilang muncul sebagai
    // ID mentahnya, dan tes halaman memastikan tidak ada token "aiBench" yang bocor ke teks.
    aiBenchTitle: "Tolok Ukur Model AI",
    // Rule-15 UWT-003 fix (2026-07-30): mirrors the English rewording — plain-language equivalent
    // of "scored relative to each other", not the undefined "roster-relative" jargon.
    // Rule-15 UWT-004 fix (2026-07-30): mirrors the English gloss for "harness" at its first use.
    aiBenchSubtitle:
      "Indeks model coding-agent yang dinilai secara relatif satu sama lain di lima harness (alat CLI atau IDE yang dipakai menjalankannya), dengan setiap angka disertai sumber.",
    aiBenchSnapshotLabel: "Cuplikan data",
    aiBenchTableCaption:
      "Roster model coding-agent: angka kapabilitas, indeks komposit, cakupan, dan harga per-harness.",
    aiBenchColModel: "Model",
    aiBenchColVendor: "Vendor",
    aiBenchColHarnesses: "Harness",
    aiBenchColClass: "Kelas",
    aiBenchBenchSweVerified: "SWE-bench Verified",
    aiBenchBenchSwePro: "SWE-bench Pro",
    aiBenchBenchTerminalBench: "Terminal-Bench 2.1",
    aiBenchBenchGpqa: "GPQA Diamond",
    aiBenchColIndex: "Indeks komposit",
    aiBenchColCoverage: "Cakupan",
    aiBenchColInputPrice: "Harga input",
    aiBenchColOutputPrice: "Harga output",
    aiBenchBandOpus: "Opus",
    aiBenchBandSonnet: "Sonnet",
    // "Haiku" tetap tidak diterjemahkan (mirip aiBenchBandOpus/aiBenchBandSonnet) — nama tingkatan
    // model (DD-35), bukan kata sifat umum seperti nilai kelas ini sebelum penggantian nama.
    aiBenchBandHaiku: "Haiku",
    aiBenchBandUnrated: "Belum dinilai",
    aiBenchNoFigure: "Tidak dilaporkan",
    aiBenchSubscription: "Langganan",
    aiBenchSubscriptionTerms: "Ketentuan langganan",
    aiBenchCoverageLow: "cakupan rendah",
    aiBenchGradeVerified: "terverifikasi",
    aiBenchGradeSelfReported: "dilaporkan sendiri",
    aiBenchGradeSecondary: "sekunder",
    aiBenchGradeConflicted: "berkonflik",
    aiBenchGradeUnavailable: "tidak tersedia",
    aiBenchEvidenceLabel: "Tingkat bukti",
    aiBenchSourceLabel: "Sumber",
    aiBenchRangeSeparator: "hingga",
    aiBenchPriceUnit: "per 1 juta token",
    aiBenchIntegrityLabel: "Catatan integritas",
    aiBenchIntegrityDetailsSummary: "Baca temuannya",
    aiBenchCardAllFigures: "Semua angka",
    aiBenchCardGroupModel: "Model",
    aiBenchCardGroupScores: "Skor",
    aiBenchHowToSummary: "Cara membaca tolok ukur ini (harap dibaca sebelum membandingkan model)",
    aiBenchHowToVendorReported:
      "Sebagian besar angka tolok ukur frontier dilaporkan sendiri oleh vendor. Pada SWE-bench Verified, reproduksi independen (METR) mengonfirmasi 0 dari 104 tugas yang diklaim vendor — anggap angka yang belum diverifikasi sebagai batas atas, bukan fakta terukur.",
    aiBenchHowToIndexRelative:
      "Indeks komposit bersifat relatif terhadap roster: setiap angka dinormalisasi terhadap model terkuat di roster ini, bukan terhadap standar mutlak. Bobot per-tolok-ukur adalah penilaian kami, bukan sifat dari tolok ukurnya.",
    aiBenchHowToCoverage:
      "Cakupan bervariasi. Model yang dinilai pada satu dari empat tolok ukur bertumpu pada jauh lebih sedikit bukti daripada yang dinilai pada keempatnya; model dengan cakupan rendah ditandai agar indeks tidak disangka setara-kepercayaan.",
    aiBenchHowToBestConfig:
      "Setiap angka mencerminkan konfigurasi publik terbaik vendor (pengaturan effort, prompt, dan harness). Performa harian model bisa lebih rendah; angka tersebut adalah batas langit, bukan kondisi tipikal.",
    // Rule-15 UWT-005 fix (2026-07-30): mirrors the English fix — ARC-AGI-2 is not one of the four
    // benchmarks that feed the composite index; swapped in SWE-bench Pro.
    aiBenchHowToArcConflict:
      "Mengapa provenans penting: angka SWE-bench Pro / GPQA Diamond untuk model yang sama berbeda antar sumber. Saat nilai yang dipublikasikan berkonflik, kami menampilkan rentang lengkapnya dan ujung rendah masuk ke indeks — tidak pernah nilai rata-rata di tengah.",
    aiBenchHowToPriceGap:
      "Mengapa harga per-harness: DeepSeek V4 Pro berharga sekitar seperempat langsung dari DeepSeek dibandingkan melalui gateway yang menaikkan tarifnya. Setiap harga menyebut harness yang menagihnya; tidak ada 'harga tunggal'.",
    aiBenchHowToPriceUnit:
      "Kecuali ditandai Langganan, setiap angka dolar adalah harga per 1 juta token — angka Langganan adalah tarif bulanan tetap dengan batas pemakaiannya sendiri, bukan harga per-token.",
    aiBenchSourcesHeading: "Sumber dan lisensi",
    aiBenchSourcesIntro:
      "Setiap angka menaut ke halaman leaderboard atau vendor asalnya. Berikut operator tolok ukur yang angkanya muncul di sini, beserta ketentuan republikasinya.",
    aiBenchOpTermsSwebench:
      "Kode dan dataset tolok ukur berlisensi MIT; halaman leaderboard itu sendiri bertanda semua hak dilindungi.",
    aiBenchOpTermsTerminalbench: "Tidak ada ketentuan republikasi yang dinyatakan oleh operator.",
    aiBenchOpTermsGpqa: "Repositori tolok ukur GPQA berlisensi MIT.",
    aiBenchOpTermsNone: "Tidak ada ketentuan republikasi yang dinyatakan oleh operator.",

    // AI benchmark — legenda (perbaikan Rule-15 UWT-002/UWT-003/UWT-005/USS-002): definisi yang
    // selalu terlihat untuk taksonomi kelas dan tingkat bukti, plus rumus cakupan.
    aiBenchLegendHeading: "Legenda kelas dan tingkat bukti",
    aiBenchLegendClassIntro:
      "Keempat kelas kemampuan adalah tingkatan indeks komposit relatif terhadap jangkar, bukan nama merek vendor — model dari vendor mana pun dapat masuk ke kelas mana pun:",
    aiBenchLegendClassOpus:
      "setara atau di atas indeks komposit Claude Opus 5 sendiri (jangkar yang menentukan tingkatan ini).",
    aiBenchLegendClassSonnet: "setara atau di atas indeks komposit Claude Sonnet 5 sendiri, di bawah jangkar Opus.",
    aiBenchLegendClassHaiku: "di bawah jangkar Sonnet.",
    aiBenchLegendClassUnrated: "tidak ada angka pada satu pun dari empat tolok ukur komposit.",
    aiBenchLegendGradeIntro: "Kelima tingkat bukti menjelaskan bagaimana setiap angka bersumber:",
    aiBenchLegendGradeVerified: "dinilai oleh verifikator independen (mis. Scale AI SEAL) atau kartu model resmi.",
    aiBenchLegendGradeSelfReported: "dipublikasikan oleh vendor tentang modelnya sendiri.",
    aiBenchLegendGradeSecondary: "dikutip oleh agregator; tidak ada sumber utama yang ditemukan.",
    aiBenchLegendGradeConflicted:
      "beberapa nilai terpublikasi yang tidak dapat direkonsiliasi — sel menampilkan rentang, tidak pernah rata-rata.",
    aiBenchLegendGradeUnavailable: "vendor tidak mempublikasikan angka untuk tolok ukur ini.",
    aiBenchLegendCoverageFormula:
      "Cakupan adalah porsi berbobot dari komposit yang dicakup oleh tolok ukur yang dilaporkan model (SWE-bench Verified 25% + SWE-bench Pro 25% + Terminal-Bench 2.1 20% + GPQA Diamond 30% = 100%), bukan sekadar jumlah tolok ukur yang dilaporkan.",

    // AI benchmark — bagan (Fase 6/7).
    aiBenchChartAxisMaxLabel: "Nilai maksimum sumbu",
    aiBenchPriceLowestSubtitle: "Menampilkan tarif harness terendah yang tersedia untuk setiap model",

    // AI benchmark — bagan gabungan (Fase 2).
    aiBenchMergedChartTitle: "Kemampuan dan harga per model",
    aiBenchSortLabel: "Urutkan",
    aiBenchSortCapability: "Kemampuan (tinggi ke rendah)",
    aiBenchSortPriceAsc: "Harga: Rendah ke Tinggi",
    aiBenchSortPriceDesc: "Harga: Tinggi ke Rendah",
    aiBenchSortScopeNote: "(hanya urutan bagan)",

    // AI benchmark — filter harness/kelas (Fase 8).
    aiBenchFilterSummary: "Filter",
    aiBenchFilterHarnessLabel: "Harness",
    aiBenchFilterClassLabel: "Kelas",
    aiBenchFilterAllHarnesses: "Semua harness",
    aiBenchFilterAllClasses: "Semua kelas",
    aiBenchClassHint: "Apa artinya ini?",
    aiBenchFilterResultCountLabel: "Model ditampilkan",
    aiBenchFilterActiveCountLabel: "aktif",
    aiBenchEmptyStateTitle: "Tidak ada model yang cocok dengan filter ini",
    aiBenchEmptyStateMessage: "Coba filter harness atau kelas yang berbeda.",
    aiBenchBandEmptyMessage: "Tidak ada model di kelas ini yang cocok dengan filter saat ini.",

    // Calculator — page
    calcTitle: "Kalkulator Biaya Hidup",
    calcSubtitle: "Bandingkan biaya hidup dan tabungan gaji di berbagai kota",
    ariaTabsNav: "Tab kalkulator",
    tabCostOfLiving: "Biaya hidup",
    tabCostDesc: "Bandingkan biaya hidup bulanan di berbagai kota",
    tabSavings: "Tabungan",
    tabSavingsDesc: "Lihat seberapa banyak yang bisa Anda hemat",
    tabMinRole: "Jabatan minimum",
    tabMinRoleDesc: "Temukan jabatan minimum yang Anda butuhkan",
    dataLastUpdated: "Data terakhir diperbarui",
    estimatesOnly: "Hanya perkiraan",

    // Calculator — disclaimers
    disclaimerPension: "Tabungan sebelum kontribusi pensiun / dana hari tua sukarela.",
    disclaimerClothing: "Pakaian dan perawatan pribadi termasuk dalam pengeluaran gaya hidup.",
    disclaimerFx:
      "Angka tabungan USD positif tidak berarti daya beli yang sama — USD menggunakan snapshot FX nominal, bukan PPP.",
    disclaimerSnapshot: "Data adalah snapshot — verifikasi angka terkini sebelum membuat keputusan relokasi.",
    disclaimerTax:
      "Pajak menggunakan tarif efektif yang disederhanakan (federal + sub-nasional untuk AS/CA/CH saja) — bukan perhitungan bracket penuh; tidak termasuk status pengisian, potongan, tunjangan natura, dan batas kontribusi.",
    disclaimerHealthcare: "Kesehatan memodelkan biaya out-of-pocket saja; skema pendanaan ditampilkan per negara.",
    disclaimerRelocation:
      "Biaya sunk relokasi adalah perkiraan sekali dan tidak termasuk dalam perhitungan tabungan bulanan; cadangan tunai adalah dana yang Anda simpan, bukan biaya.",
    disclaimerRoleSalary:
      "Gaji jabatan dimodelkan di tingkat nasional (negara) — kota mewarisi distribusi p25/median/p75 negaranya.",
    disclaimerNonSalary:
      "Kompensasi non-gaji (RSU/ekuitas + bonus) hanya sebagai konteks informasi total kompensasi, bukan bagian dari perhitungan tabungan.",

    // Calculator — geo filters
    labelRegion: "Wilayah",
    labelCountry: "Negara",
    labelCity: "Kota",
    optAllRegions: "Semua wilayah",
    optAllCountries: "Semua negara",
    optAllCities: "Semua kota",
    clearRegion: "Hapus",
    regionAutoAdvisory: "Wilayah diperbarui otomatis agar sesuai dengan negara yang dipilih.",

    // Calculator — region display names (UWT-004). The serialized region KEY stays English
    // (URL stability); only these display labels are localized. MENA/Nordics are expanded.
    regionAsean: "ASEAN",
    regionJapan: "Jepang",
    regionEurope: "Eropa",
    regionNordics: "Nordik (Eropa Utara)",
    regionAmericas: "Amerika",
    regionMena: "Timur Tengah & Afrika Utara",
    regionAsia: "Asia",
    regionOceania: "Oseania",
    regionAfrica: "Afrika",

    // Calculator — controls
    labelAdults: "Dewasa",
    labelPreschoolKids: "Anak prasekolah",
    labelSchoolKids: "Anak usia sekolah",
    labelSchoolType: "Jenis sekolah",
    optPublic: "Negeri",
    optPrivate: "Swasta",
    schoolTypeHint: "tambahkan anak usia sekolah untuk memilih",
    // UWT-015: native hover tooltip (title) on the disabled Public/Private buttons.
    schoolTypeDisabledTitle: "Tambahkan anak usia sekolah untuk mengaktifkan opsi ini",
    foreignerPublicSchoolNote:
      "Sekolah negeri nggak terbuka buat warga asing di semua negara; di tempat yang nggak (mis. UEA, Singapura), biaya sekolah swasta yang dipakai.",
    publicSchoolForeignerFlag: "negeri n/a → swasta",
    publicSchoolForeignerFlagBadge: "Swasta — negeri tak terbuka untuk WNA",
    labelArea: "Wilayah",
    optCenter: "Pusat kota",
    optRural: "Pedesaan",

    // Calculator — cost-of-living table
    colCountry: "Negara",
    colCity: "Kota",
    colHealthcareScheme: "Skema kesehatan",
    tooltipHealthcareScheme:
      "Bagaimana biaya kesehatan didanai di negara ini: didanai pajak, asuransi penggajian wajib, atau bayar sendiri.",
    colHousing: "Perumahan",
    colFood: "Makanan",
    colTransport: "Transportasi",
    colUtilities: "Utilitas",
    colHealthcareOOP: "Kesehatan (OOP)",
    colHealthcareOOPPrefix: "Kesehatan",
    colChildcare: "Penitipan anak",
    colSchool: "Sekolah",
    colLifestyle: "Gaya hidup",
    colEssentials: "Kebutuhan pokok",
    colTotal: "Total",
    previewMonthlyEstimate: "perkiraan kebutuhan pokok bulanan",
    // UWT-006: labels the pre-populated min-role preview panel as illustrative.
    previewExampleLabel: "Contoh",
    colRelocationSunk: "Relokasi (biaya hangus)",
    colLiquidityReserve: "Cadangan likuiditas",
    tooltipRelocationSunk:
      "Biaya hangus sekali: deposit sewa, uang kunci, pindahan, dan biaya visa. Bukan pengeluaran bulanan.",
    tooltipLiquidityReserve:
      "Dana cadangan yang Anda simpan — bukan biaya hangus. Menutup bulan-bulan awal sebelum gaji mulai.",
    oopLegend:
      "OOP = out-of-pocket — biaya kesehatan yang Anda bayar sendiri, di luar jaminan dari pajak atau asuransi.",

    // Calculator — healthcare scheme badges
    healthcareTaxFunded: "didanai pajak",
    healthcareMandatoryPayroll: "asuransi penggajian wajib",
    healthcareOutOfPocket: "bayar sendiri",

    // Calculator — city detail
    sectionMonthlyExpenses: "Pengeluaran bulanan",
    sectionRelocationCosts: "Biaya relokasi",
    labelHousing: "Perumahan",
    labelFood: "Makanan",
    labelTransport: "Transportasi",
    labelUtilities: "Utilitas",
    labelHealthcareOOP: "Kesehatan (OOP)",
    labelChildcare: "Penitipan anak",
    labelSchool: "Sekolah",
    labelEssentialsSubtotal: "Subtotal kebutuhan pokok",
    labelMonthlyTotal: "Total bulanan",
    labelRelocationSunkCost: "Biaya sunk relokasi sekali",
    labelLiquidityReserve: "Cadangan likuiditas (dana cadangan — disimpan, tidak dibelanjakan)",
    backToAllCities: "← Kembali ke semua kota",

    // Calculator — savings table
    savingsEmptyStateMessage:
      "Masukkan gaji kotor bulanan Anda untuk melihat berapa banyak yang bisa Anda hemat di setiap kota.",
    grossMonthlySalaryLabel: "Gaji kotor bulanan (sebelum pajak)",
    salaryCurrencyIndicator: "Mata uang: USD",
    salaryCurrencyExplanation: "Gaji dibandingkan dalam USD di semua kota.",
    annualGrossLabel: "Total gaji tahunan",
    nonSalaryCompNote:
      "Kompensasi non-gaji (RSU/ekuitas + bonus) hanya informasi — tidak termasuk dalam perhitungan tabungan.",
    colNet: "Bersih (bulanan)",
    colSavingsEssential: "Tabungan setelah kebutuhan pokok ↕",
    colSavingsLifestyle: "Tabungan setelah gaya hidup",
    colNonSalaryComp: "Kompensasi non-gaji tipikal (info, tahunan)",
    colTotalComp: "Total kompensasi (info, tahunan)",
    sortBySavings: "Urutkan berdasarkan tabungan",
    subNationalIndicator: "(federal+negara bagian)",

    // Calculator — min-role table
    labelBaselineSource: "Cara menetapkan target",
    optSavingsTarget: "Target tabungan bulanan",
    optReferenceRole: "Samakan jabatan",
    optMySalary: "Gaji saya",
    hintSavingsTarget:
      "Masukkan target tabungan bulanan — tabel menandai jabatan terendah yang kota terbaiknya mencapainya.",
    hintReferenceRole:
      "Pilih jabatan dan kota sebagai patokan — tabel menandai jabatan terendah yang menabung setidaknya sebanyak itu, tanpa perlu angka.",
    hintMySalary:
      "Masukkan gaji kotor Anda saat ini — tabel menandai jabatan terendah yang menabung setidaknya sebanyak Anda sekarang.",
    labelMonthlySavingsTarget: "Target tabungan bulanan",
    labelTargetCurrency: "Mata uang target",
    labelRefCity: "Kota referensi",
    labelRefRole: "Jabatan referensi",
    labelMyGrossMonthly: "Gaji kotor bulanan saya",
    labelMySalaryCity: "Kota gaji saya",
    labelSalaryInputCurrency: "Mata uang gaji",
    labelDisplayCurrency: "Mata uang tampilan",
    rankBasisNote:
      "Kunci peringkat: tabungan kebutuhan pokok (perumahan + makanan + transportasi + utilitas + kesehatan + sekolah). Gaya hidup dikecualikan — variabel preferensi pribadi.",
    nonSalaryRankNote: "Kompensasi non-gaji (RSU / ekuitas / bonus) hanya informasi — tidak digunakan dalam peringkat.",
    noQualifierMessage: "Tidak ada jabatan yang mencapai target tabungan ini di kota manapun.",
    minRoleEmptyStateMessage:
      "Masukkan target tabungan bulanan untuk melihat jabatan mana yang mencapainya di setiap kota.",
    seRolesCaption: "Jabatan: rekayasa perangkat lunak (IC + manajemen)",
    qualifyingDivider: "— jabatan di bawah tidak mencapai target tabungan —",
    moreBelowBar: "pasangan (kota, jabatan) lain di bawah ambang Anda (tidak ditampilkan)",
    colRole: "Jabatan",
    colTrack: "Jalur",
    colBestCity: "Kota terbaik",
    colP25: "P25 (bulanan)",
    colMedian: "Median",
    colP75: "P75",
    colEssentialSavings: "Tabungan kebutuhan pokok",
    colNonSalaryCompInfo: "Kompensasi non-gaji",
    minimumMarker: "← min",
    // UWT-010: percentile gloss tooltips for the salary-distribution headers.
    tooltipP25: "Gaji bulanan persentil ke-25 — seperempat orang di jabatan ini berpenghasilan lebih rendah.",
    tooltipMedian: "Gaji bulanan median (persentil ke-50) untuk jabatan ini.",
    tooltipP75: "Gaji bulanan persentil ke-75 — seperempat orang di jabatan ini berpenghasilan lebih tinggi.",
    // UWT-013: expanded Track labels (the table renders these instead of bare "ic"/"mgmt").
    trackIc: "Kontributor individu",
    trackMgmt: "Manajemen",
    // UWT-003: gloss for the shortened "Non-salary comp" header.
    tooltipNonSalaryComp:
      "RSU/ekuitas + bonus — total tahunan, hanya informasi, tidak digunakan dalam perhitungan tabungan.",

    // IA navigation revamp — landing homepage + global nav
    heroHeading: "Belajar membangun perangkat lunak, dengan cara yang jelas.",
    heroIntro:
      "AyoKoding adalah pusat belajar terbuka dwibahasa untuk rekayasa perangkat lunak — panduan praktis, contoh nyata, dan alat gratis yang tumbuh bersama Anda.",
    heroCtaLearn: "Mulai belajar",
    heroCtaTools: "Jelajahi alat",
    navLearn: "Belajar",
    navTools: "Alat",
    browseTitle: "Jelajahi",
    browseIntro: "Jelajahi seluruh bagian AyoKoding dalam satu tempat.",
    sectionBlurbFallback: "Jelajahi bagian ini.",
    toolsTeaserKicker: "Alat",
    toolsTeaserTitle: "Kalkulator Biaya Hidup",
    toolsTeaserDesc: "Bandingkan biaya hidup bulanan, tabungan, dan peran minimum yang Anda butuhkan di berbagai kota.",
    toolsTeaserCta: "Buka kalkulator",
    footerLearn: "Belajar",
    footerTools: "Alat",
    footerAbout: "Tentang",
    footerBrowseAll: "Jelajahi semua",
    footerCalculator: "Kalkulator Biaya Hidup",
    footerAiBenchmark: "Tolok Ukur Model AI",
    footerAboutAyokoding: "Tentang AyoKoding",
    footerTerms: "Syarat & Ketentuan",
    footerProject: "Proyek",
    sectionExploreHeading: "Jelajahi",

    // Mobile nav drawer — preset width control
    mobileNavWidthLabel: "Lebar drawer",
    mobileNavWidthHint: "Perlebar drawer untuk membaca judul jalur atau kursus yang panjang secara utuh",
    mobileNavWidthDefault: "Standar",
    mobileNavWidthWide: "Lebar",

    // Course-paths feature chrome (DWT-003 fix, phase-5 rule-15 design-tester retest)
    pathsChooseYourPath: "Pilih jalur Anda",
    pathsCompareAllPaths: "Bandingkan semua jalur",
    pathsExploreSkillsPaths: "Jelajahi jalur keterampilan",
    pathsBrowseCourseLibrary: "Jelajahi seluruh pustaka kursus",
    pathsStart: "Mulai",
    pathsExploreArc: "Jelajahi arc",
    pathsExploreArcRoles: "Jelajahi peran arc ini",
    pathsSyllabus: "Silabus",
    pathsPrerequisites: "Prasyarat",
    pathsCourseWordCapital: "Kursus",
    pathsCourseWordLower: "kursus",
    pathsOfWord: "dari",
    pathsOnPathPrefix: "pada jalur",
    pathsViewPath: "Lihat jalur",
    pathsViewFullPath: "Lihat jalur lengkap",
    pathsBrowseAllCourses: "Jelajahi semua kursus",

    // Resizable docs sidebar — drag/keyboard handle accessible name
    resizableSidebarHandleLabel: "Ubah ukuran panel",

    // Code-block copy button — CodeBlock's copyLabel/copiedLabel/errorLabel
    copy: "Salin",
    copied: "Tersalin",
    copyFailed: "Gagal menyalin",
  },
};

export function t(locale: Locale, key: string): string {
  return translations[locale]?.[key] ?? key;
}
