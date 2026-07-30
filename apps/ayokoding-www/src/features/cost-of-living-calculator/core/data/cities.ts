// CITY + COUNTRY DATASET — tech-hub cities worldwide (excl. Israel), snapshotDate 2026-07-30.
// Sources: Numbeo (Jun-Jul 2026), PwC Worldwide Tax Summaries, national tax/social-security
//          authorities, official government/education sources — cited inline per field.
// Sources: Numbeo Jun 2026, PwC Worldwide Tax Summaries 2025, OECD 2025, ECB/Xe.com 2026-06-17.
// FX rates NOT stored here — all USD conversion via fx.ts (city.currency → fxToUsd(fx, currency)).
// Confidence tiers: high = primary source, moderate = secondary / corroborated, proxy = derived.
// To (re)source this data, see the prompts in
// ../../../../../docs/cost-of-living-calculator/data-sourcing-prompt.md

import type { FxTable } from "./fx";
import { fx } from "./fx";

// ─── Types ──────────────────────────────────────────────────────────────────

type Confidence = "high" | "moderate" | "proxy";

type Money = {
  amount: number;
  confidence: Confidence;
  note?: string;
};

type ExpenseCategories = {
  housing: Money;
  food: Money;
  transport: Money;
  utilities: Money;
  healthcare: Money;
  childcare: Money;
  lifestyle: Money;
};

type Relocation = {
  sunkCosts: {
    deposit: Money;
    keyMoney: Money;
    moving: Money;
    visaAdmin: Money;
  };
  liquidityReserve: {
    cashCushion: Money;
  };
};

type IncomeBand = "low" | "mid" | "high";
type Area = "center" | "rural";

export type Household = {
  adults: 1 | 2;
  preschoolKids: 0 | 1 | 2 | 3;
  schoolKids: 0 | 1 | 2 | 3;
};

export type Country = {
  id: string;
  name: { en: string; id: string };
  bandThresholdsUsd: { lowToMid: number; midToHigh: number };
  effectiveRate: Record<IncomeBand, Money>;
  healthcareModelType: "oop" | "tax-funded" | "mixed";
  compulsoryInsurance: {
    health: boolean;
    socialSecurity: boolean;
    note?: string;
  };
  // Whether a FOREIGN resident worker (work-visa holder, not a citizen/PR) can enrol children in
  // PUBLIC primary school. "open" = on similar terms to locals; "limited" = legally allowed but
  // with heavy barriers (non-resident fees, local-language-only, quotas) so most expat families
  // use private/international; "nationals-only" = effectively unavailable to foreign residents.
  // When access is NOT "open" (i.e. "limited" or "nationals-only"), the calculator charges the
  // PRIVATE school figure for a foreigner even if "public" is selected — the realistic relocation
  // budget where public schooling carries non-resident fees/barriers or is barred is private.
  foreignerPublicSchool: {
    access: "open" | "limited" | "nationals-only";
    confidence: Confidence;
    note?: string;
  };
};

export type City = {
  id: string;
  name: { en: string; id: string };
  countryId: string;
  currency: string;
  region: "asean" | "japan" | "europe" | "nordics" | "americas" | "mena" | "asia" | "oceania" | "africa";
  expenses: ExpenseCategories;
  childcareMedianLocal: Money;
  schoolMedianLocal: { public: Money; private: Money };
  relocation: Relocation;
  subNational?: {
    name: { en: string; id: string };
    effectiveRate: Record<IncomeBand, Money>;
  };
};

export type Dataset = {
  snapshotDate: string;
  fx: FxTable;
  countries: Country[];
  cities: City[];
};

// ─── OECD Multiplier Helpers ─────────────────────────────────────────────────

// OECD modified equivalence scale: first adult=1.0, additional adult=+0.5, each child=+0.3.
export function equivalisedSize(h: Household): number {
  return 1.0 + 0.5 * (h.adults - 1) + 0.3 * (h.preschoolKids + h.schoolKids);
}

// Damping factor for sub-linear household categories (housing, utilities share economies of scale).
export const SUBLINEAR_DAMPING = 0.5;

// Sub-linear multiplier: housing + utilities grow slower than household size.
export const subLinear = (h: Household): number => 1 + SUBLINEAR_DAMPING * (equivalisedSize(h) - 1);

// Per-capita multiplier: food, healthcare scale with equivalised size.
export const perCapita = (h: Household): number => equivalisedSize(h);

// Area discount for housing outside city center.
export const AREA_MULTIPLIERS: Record<Area, number> = {
  center: 1.0,
  rural: 0.75,
};

// ─── Helper ─────────────────────────────────────────────────────────────────

function m(amount: number, confidence: Confidence, note?: string): Money {
  return { amount, confidence, note };
}

// ─── Countries ──────────────────────────────────────────────────────────────

export const countries: Country[] = [
  // ── ASEAN ──
  {
    id: "sg",
    foreignerPublicSchool: {
      access: "limited",
      confidence: "high",
      note: "Non-citizens apply in Phase 3 after SC/PR (not guaranteed); intl-student fee ~S$985/mo non-ASEAN. MOE 2023 (unchanged 2026)",
    },
    name: { en: "Singapore", id: "Singapura" },
    bandThresholdsUsd: { lowToMid: 3500, midToHigh: 8000 },
    effectiveRate: {
      low: m(
        0.04,
        "high",
        "PwC Worldwide Tax Summaries 2026: resident PIT brackets unchanged (0% to SGD 20K); CPF employee 20% up to SGD 8,000/mo wage ceiling (CPF Board 2026, raised from S$7,400); effective ~4% at low band",
      ),
      mid: m(
        0.1,
        "high",
        "PwC 2026: resident PIT brackets confirmed unchanged; effective ~10% at mid band incl. CPF relief treatment",
      ),
      high: m(0.17, "high", "PwC 2026: resident PIT brackets confirmed unchanged; effective ~17% at high band"),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: true,
      socialSecurity: true,
      note: "CPF employee 20% (wage ceiling raised to S$8,000/mo, Jan 2026, CPF Board) covers retirement/housing/Medisave; MediShield Life mandatory health insurance",
    },
  },
  {
    id: "th",
    foreignerPublicSchool: {
      access: "limited",
      confidence: "high",
      note: "Foreigners may enrol but pay fees unlike Thais; all-Thai instruction; most expats use bilingual/intl schools. Allianz Care 2024 (unchanged 2026)",
    },
    name: { en: "Thailand", id: "Thailand" },
    bandThresholdsUsd: { lowToMid: 2000, midToHigh: 6000 },
    effectiveRate: {
      low: m(
        0.08,
        "moderate",
        "PwC 2026: PIT brackets unchanged (0-150K exempt, 5%-35% progressive); SSF employee 5% at low band",
      ),
      mid: m(0.18, "moderate", "PwC 2026: PIT brackets unchanged; ~18% at mid band incl. SSF"),
      high: m(0.31, "moderate", "PwC 2026: PIT brackets unchanged (top 35% marginal); ~31% at high band incl. SSF"),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: true,
      socialSecurity: true,
      note: "SSF (Social Security Fund) 5% employee, wage ceiling raised to THB 17,500/mo (cap THB 875/mo, phased 2026-2028, up from THB 750 unchanged since 1995); Universal Coverage Scheme (UCS) public coverage. SSO/Acclime/Baker McKenzie 2026",
    },
  },
  {
    id: "id",
    foreignerPublicSchool: {
      access: "nationals-only",
      confidence: "high",
      note: "Foreign nationals legally barred from Sekolah Nasional; must use SPK/international schools. ISJ expat guide 2024 (unchanged 2026)",
    },
    name: { en: "Indonesia", id: "Indonesia" },
    bandThresholdsUsd: { lowToMid: 1500, midToHigh: 5000 },
    effectiveRate: {
      low: m(
        0.07,
        "moderate",
        "PwC 2026: PPh21 brackets unchanged under HPP Law (5/15/25/30/35%); BPJS Kesehatan 1% (capped Rp12M wage) + BPJS Ketenagakerjaan JHT 2%+JP 1% employee; ~7% at low band",
      ),
      mid: m(0.17, "moderate", "PwC 2026: PPh21 brackets unchanged; ~17% at mid band incl. BPJS"),
      high: m(0.3, "moderate", "PwC 2026: PPh21 brackets unchanged (top 35% marginal >Rp5B); ~30% at high band"),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: true,
      socialSecurity: true,
      note: "BPJS Kesehatan 1% employee (capped Rp12,000,000 wage, 2026) + BPJS Ketenagakerjaan (JHT 2% + JP 1% employee, JP wage ceiling raised to Rp11,086,300 Mar 2026); JKK/JKM employer-paid. DataOn/Acclime 2026",
    },
  },
  {
    id: "my",
    foreignerPublicSchool: {
      access: "limited",
      confidence: "high",
      note: "Legal with a student pass (~MYR 250/yr) but Bahasa-medium + admin burden; most expats use intl schools. Expat Exchange 2025 (unchanged 2026)",
    },
    name: { en: "Malaysia", id: "Malaysia" },
    bandThresholdsUsd: { lowToMid: 1800, midToHigh: 5500 },
    effectiveRate: {
      low: m(0.05, "high", "PwC 2026: PIT brackets unchanged; EPF employee 11% unchanged; ~5% effective at low band"),
      mid: m(0.17, "high", "PwC 2026: PIT brackets unchanged; ~17% at mid band incl. EPF"),
      high: m(0.29, "high", "PwC 2026: PIT brackets unchanged (top marginal 30%); ~29% at high band"),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: false,
      socialSecurity: true,
      note: "EPF 11% employee (unchanged) + SOCSO/EIS (combined wage ceiling raised to RM6,000, since Oct 2024) mandatory; public health (MOH) not insurance-based. Swingvy/ajobthing 2026",
    },
  },
  {
    id: "vn",
    foreignerPublicSchool: {
      access: "limited",
      confidence: "moderate",
      note: "Permitted with a valid visa, tuition-free from 2025, but Vietnamese-only + ho khau priority; 2-3yr language prep. VTJ/Allianz 2025 (unchanged 2026)",
    },
    name: { en: "Vietnam", id: "Vietnam" },
    bandThresholdsUsd: { lowToMid: 1000, midToHigh: 3500 },
    effectiveRate: {
      low: m(
        0.08,
        "moderate",
        "PwC 2026: PIT brackets unchanged (5/10/15/20/25/30/35%); VSS 10.5% employee at low band",
      ),
      mid: m(0.18, "moderate", "PwC 2026: PIT brackets unchanged; ~18% at mid band incl. VSS (wage-capped)"),
      high: m(
        0.3,
        "moderate",
        "PwC 2026: PIT brackets unchanged (top 35% marginal >100M VND/mo); ~30% at high band; VSS contribution capped so its % share shrinks at high income",
      ),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: true,
      socialSecurity: true,
      note: "Vietnamese Social Insurance 10.5% employee (8% pension + 1.5% health + 1% unemployment), wage-capped at ~20× base statutory rate; foreign employees exempt from unemployment ins. (9.5%). Omni HR/netviet 2026",
    },
  },
  {
    id: "ph",
    foreignerPublicSchool: {
      access: "open",
      confidence: "moderate",
      note: "Free public basic education for legal residents; work-permit kids exempt from study permit; Filipino-medium. DepEd 2024 (unchanged 2026)",
    },
    name: { en: "Philippines", id: "Filipina" },
    bandThresholdsUsd: { lowToMid: 1000, midToHigh: 3500 },
    effectiveRate: {
      low: m(
        0.07,
        "moderate",
        "PwC 2026: TRAIN law PIT brackets unchanged since 2023 (0/15/20/25/30/35%); SSS 5% (MSC cap ₱35,000) + PhilHealth 2.5% (base cap ₱100,000) + Pag-IBIG 2% employee; ~7% at low band",
      ),
      mid: m(0.19, "moderate", "PwC 2026: TRAIN brackets unchanged; ~19% at mid band"),
      high: m(
        0.3,
        "moderate",
        "PwC 2026: TRAIN brackets confirmed unchanged; bracket-by-bracket calc at representative high-band income + capped SSS/PhilHealth/Pag-IBIG gives ~30% at high band (revised down from prior 33% now that caps are confirmed)",
      ),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: true,
      socialSecurity: true,
      note: "SSS 5% employee (of Monthly Salary Credit, MSC ceiling ₱35,000) + PhilHealth 2.5% employee (base cap ₱100,000, max ₱2,500/mo) + Pag-IBIG 2% employee (cap fund salary ₱10,000, max ₱200/mo) mandatory. Taxify.ph/GreatDay HR 2026",
    },
  },
  // ── Japan ──
  {
    id: "jp",
    foreignerPublicSchool: {
      access: "open",
      confidence: "high",
      note: "Same right as nationals, tuition-free; Japanese-only forms/instruction need language support. MEXT / Japan Living Guide 2024",
    },
    name: { en: "Japan", id: "Jepang" },
    bandThresholdsUsd: { lowToMid: 3000, midToHigh: 8000 },
    effectiveRate: {
      low: m(
        0.14,
        "high",
        "PwC 2026: national income tax 5-45% + local inhabitant tax 10% flat + 2.1% surtax on national tax ~14% at low",
      ),
      mid: m(0.29, "high", "PwC 2026: ~29% at mid band"),
      high: m(
        0.44,
        "high",
        "PwC 2026: ~44% at high band (top marginal combined ~55.95% incl. 10% local + 2.1% surtax)",
      ),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: true,
      socialSecurity: true,
      note: "Shakai hoken (health ~5% employee) + NPS pension mandatory; unemployment insurance 0.5% employee from Apr 2026; 70% coverage",
    },
  },
  {
    id: "gb",
    foreignerPublicSchool: {
      access: "open",
      confidence: "high",
      note: "Free state schools; admissions must not demand passport/visa; residency-based catchment applies equally. GOV.UK 2024",
    },
    name: { en: "United Kingdom", id: "Inggris" },
    bandThresholdsUsd: { lowToMid: 3500, midToHigh: 8500 },
    effectiveRate: {
      low: m(
        0.12,
        "high",
        "HMRC 2026/27: personal allowance frozen at GBP 12,570 (to Apr 2031); income tax + NI ~12% at lower band",
      ),
      mid: m(0.28, "high", "HMRC 2026/27: ~28% at mid band"),
      high: m(0.42, "high", "HMRC 2026/27: ~42% at high band; allowance tapers to zero above GBP 125,140"),
    },
    healthcareModelType: "tax-funded",
    compulsoryInsurance: {
      health: false,
      socialSecurity: true,
      note: "NI contributions fund NHS + state pension; NHS free at point of use",
    },
  },
  {
    id: "de",
    foreignerPublicSchool: {
      access: "open",
      confidence: "high",
      note: "Schulpflicht applies to every resident child regardless of nationality; public schools free. Handbook Germany 2024",
    },
    name: { en: "Germany", id: "Jerman" },
    bandThresholdsUsd: { lowToMid: 4000, midToHigh: 9000 },
    effectiveRate: {
      low: m(
        0.2,
        "high",
        "PwC 2026: income tax (Grundfreibetrag EUR 12,348) + GKV 14.6%+2.9% avg addl + pension 18.6% + care 3.6% (ee halves) ~20%",
      ),
      mid: m(0.36, "high", "PwC 2026: ~36% at mid band"),
      high: m(0.48, "high", "PwC 2026: ~48% at high band; top marginal income tax 45%"),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: true,
      socialSecurity: true,
      note: "GKV statutory health (7.3%+1.45% avg addl employee) + pension 9.3% ee + care 1.8-2.1% ee + unemployment 1.3% ee mandatory. PwC 2026",
    },
  },
  {
    id: "nl",
    foreignerPublicSchool: {
      access: "open",
      confidence: "high",
      note: "Free basisschool for all residents; non-Dutch speakers get a ~1yr newcomers class. Government.nl",
    },
    name: { en: "Netherlands", id: "Belanda" },
    bandThresholdsUsd: { lowToMid: 4000, midToHigh: 9000 },
    effectiveRate: {
      low: m(
        0.18,
        "high",
        "PwC 2026: Box 1 3-bracket system, bracket 1 combines income tax + national insurance (~35.82% incl. 27.65% NI) but low earners net ~18% after credits",
      ),
      mid: m(0.36, "high", "PwC 2026: ~36% at mid band"),
      high: m(0.48, "high", "PwC 2026: ~48% at high band; Box 1 top rate 49.5% (bracket 3)"),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: true,
      socialSecurity: true,
      note: "ZVW mandatory health insurance (~1,700-1,900 EUR/yr deductible) + AOW pension via employer",
    },
  },
  {
    id: "pt",
    foreignerPublicSchool: {
      access: "open",
      confidence: "high",
      note: "Free compulsory schooling ages 6-18 for residents; PLNM language support. gov.pt",
    },
    name: { en: "Portugal", id: "Portugal" },
    bandThresholdsUsd: { lowToMid: 2500, midToHigh: 6500 },
    effectiveRate: {
      low: m(
        0.14,
        "high",
        "PwC Portugal 2026 Tax Guide: IRS 12.5-48% progressive + Segurança Social 11% ee ~14% at low",
      ),
      mid: m(0.28, "high", "PwC Portugal 2026: ~28% at mid band"),
      high: m(0.43, "high", "PwC Portugal 2026: ~43% at high band; top IRS bracket 48%"),
    },
    healthcareModelType: "tax-funded",
    compulsoryInsurance: {
      health: false,
      socialSecurity: true,
      note: "Segurança Social 11% employee; SNS (Serviço Nacional de Saúde) tax-funded",
    },
  },
  {
    id: "ch",
    foreignerPublicSchool: {
      access: "open",
      confidence: "high",
      note: "Free public schooling for all legal residents; cantonal-language-only instruction; many expats still pick private. Expatica 2024",
    },
    name: { en: "Switzerland", id: "Swiss" },
    bandThresholdsUsd: { lowToMid: 5000, midToHigh: 12000 },
    effectiveRate: {
      low: m(
        0.12,
        "high",
        "PwC / EFD 2026: federal tax 0.77-11.5% (single) + AHV/IV/EO ~5.3% ee + cantonal avg ~12% at low",
      ),
      mid: m(0.23, "high", "PwC / EFD 2026: ~23% at mid band"),
      high: m(
        0.36,
        "high",
        "PwC / EFD 2026: ~36% at high band (national canton-weighted average; Zurich combined top ~41%, Geneva ~46%, Zug ~23%)",
      ),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: true,
      socialSecurity: true,
      note: "LAMal individual health insurance mandatory (~400-500 CHF/mo); AHV/AVS pension mandatory",
    },
  },
  {
    id: "pl",
    foreignerPublicSchool: {
      access: "open",
      confidence: "high",
      note: "Compulsory ages 6-18 regardless of status; catchment school must admit; free Polish classes. migrant.info.pl 2024",
    },
    name: { en: "Poland", id: "Polandia" },
    bandThresholdsUsd: { lowToMid: 2000, midToHigh: 6000 },
    effectiveRate: {
      low: m(
        0.1,
        "high",
        "PwC 2026: PIT 12% (bracket to PLN 120,000, tax-free amount PLN 30,000) + ZUS 13.71% + health 9% (partially PIT-deductible) ~10% at low",
      ),
      mid: m(0.21, "high", "PwC 2026: ~21% at mid band"),
      high: m(0.33, "high", "PwC 2026: ~33% at high band; PIT top bracket 32% above PLN 120,000"),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: true,
      socialSecurity: true,
      note: "ZUS: pension 9.76%+disability 1.5%+sick 2.45% ee (13.71% total, capped PLN 282,600/yr 2026) + NFZ health 9% (uncapped) mandatory",
    },
  },
  {
    id: "cz",
    foreignerPublicSchool: {
      access: "open",
      confidence: "high",
      note: "All foreigners resident 90+ days get free basic education regardless of residence type/language. portal.gov.cz",
    },
    name: { en: "Czech Republic", id: "Ceko" },
    bandThresholdsUsd: { lowToMid: 2000, midToHigh: 5500 },
    effectiveRate: {
      low: m(
        0.11,
        "high",
        "PwC 2026: PIT 15% (up to CZK 1,762,812/yr, 36x avg monthly wage) + health 4.5% ee + social security 7.1% ee ~11% at low",
      ),
      mid: m(0.22, "high", "PwC 2026: ~22% at mid band"),
      high: m(0.34, "high", "PwC 2026: ~34% at high band; PIT top rate 23% above threshold"),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: true,
      socialSecurity: true,
      note: "Health insurance 4.5% + social security 7.1% employee mandatory (SS capped at 48x avg monthly wage = CZK 2,350,416/yr 2026)",
    },
  },
  {
    id: "fr",
    foreignerPublicSchool: {
      access: "open",
      confidence: "high",
      note: "Compulsory ages 3-16 for all residents (Code educ. L.131-1); free; UPE2A French support. education.gouv.fr 2024",
    },
    name: { en: "France", id: "Prancis" },
    bandThresholdsUsd: { lowToMid: 3500, midToHigh: 9000 },
    effectiveRate: {
      low: m(
        0.22,
        "high",
        "PwC 2026: employee social contributions ~22-25% of remuneration + CSG/CRDS ~9.7% (largely non-deductible) offsetting income-tax-free low band ~22%",
      ),
      mid: m(0.39, "high", "PwC 2026: ~39% at mid band"),
      high: m(0.53, "high", "PwC 2026: ~53% at high band; income tax top marginal 45% + social/CSG stack"),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: true,
      socialSecurity: true,
      note: "URSSAF: CSG/CRDS ~9.7% + health + pension mandatory (employee share ~22-25% total); Assurance maladie covers 70-80%",
    },
  },
  // ── Nordics ──
  {
    id: "se",
    foreignerPublicSchool: {
      access: "open",
      confidence: "high",
      note: "Free compulsory schooling ages 6-16 for residence-permit holders' kids; Forberedelseklass support. sweden.se 2024",
    },
    name: { en: "Sweden", id: "Swedia" },
    bandThresholdsUsd: { lowToMid: 3500, midToHigh: 8000 },
    effectiveRate: {
      low: m(
        0.29,
        "high",
        "PwC (reviewed 2026-02-09): kommunalskatt avg 32% minus jobbskatteavdrag credit ~29% net at low band",
      ),
      mid: m(
        0.39,
        "high",
        "PwC (reviewed 2026-02-09): 32% municipal + partial 20% national above SEK 643,000 (2026 threshold) blended ~39%",
      ),
      high: m(
        0.53,
        "high",
        "PwC (reviewed 2026-02-09): 32% municipal + 20% national above SEK 643,000 threshold ≈ 52-53% at high band",
      ),
    },
    healthcareModelType: "tax-funded",
    compulsoryInsurance: {
      health: false,
      socialSecurity: true,
      note: "Employer pays social contributions; allmän pensionsavgift 7% employee largely offset by tax credit; health tax-funded",
    },
  },
  {
    id: "dk",
    foreignerPublicSchool: {
      access: "open",
      confidence: "high",
      note: "Free Folkeskole ages 6-16 for legal residents; reception class / language support. City of Copenhagen",
    },
    name: { en: "Denmark", id: "Denmark" },
    bandThresholdsUsd: { lowToMid: 4000, midToHigh: 9000 },
    effectiveRate: {
      low: m(
        0.3,
        "high",
        "PwC (reviewed 2026-06-25): AM-bidrag 8% + bottom tax 12.01% + avg municipal 25.049% net of personfradrag ~30% at low band",
      ),
      mid: m(0.41, "high", "PwC (reviewed 2026-06-25): + middle tax 7.5% above DKK 696,956 blended ~41% at mid band"),
      high: m(
        0.56,
        "high",
        "PwC (reviewed 2026-06-25): + top tax 7.5% above DKK 845,543; marginal cap 60.5% (2026) ~56% effective at high band",
      ),
    },
    healthcareModelType: "tax-funded",
    compulsoryInsurance: {
      health: false,
      socialSecurity: false,
      note: "Entirely tax-funded (ATP pension minimal); no separate mandatory employee health contribution",
    },
  },
  {
    id: "no",
    foreignerPublicSchool: {
      access: "open",
      confidence: "high",
      note: "Free compulsory schooling ages 6-16 for residence-permit holders; place within a month of arrival. nyinorge.no",
    },
    name: { en: "Norway", id: "Norwegia" },
    bandThresholdsUsd: { lowToMid: 4000, midToHigh: 9000 },
    effectiveRate: {
      low: m(
        0.22,
        "high",
        "PwC (reviewed 2026-01-20): 22% general income tax + trinnskatt 1.7-4.0% + trygdeavgift 7.6% (2026, down from 7.9%) blended ~22% at low band",
      ),
      mid: m(
        0.34,
        "high",
        "PwC (reviewed 2026-01-20): trinnskatt step 13.7% above NOK 725,050 (2026) raises blended rate to ~34% at mid band",
      ),
      high: m(
        0.46,
        "high",
        "PwC (reviewed 2026-01-20): trinnskatt top steps 16.8-17.8% above NOK 980,100/1,467,200 (2026) ~46% at high band",
      ),
    },
    healthcareModelType: "tax-funded",
    compulsoryInsurance: {
      health: false,
      socialSecurity: true,
      note: "Trygdeavgift (national insurance) 7.6% employee (2026); Helseforetak health tax-funded via general taxes",
    },
  },
  {
    id: "fi",
    foreignerPublicSchool: {
      access: "open",
      confidence: "high",
      note: "Free basic education for permanently resident kids 6-17; valmistava preparatory class. City of Helsinki",
    },
    name: { en: "Finland", id: "Finlandia" },
    bandThresholdsUsd: { lowToMid: 3500, midToHigh: 8000 },
    effectiveRate: {
      low: m(
        0.18,
        "high",
        "PwC (reviewed 2026-06-24): state tax 12.64% on first EUR 21,200 bracket + municipal ~7.5% avg + TyEL/unemployment ~-8% deductions net ~18% at low band",
      ),
      mid: m(
        0.31,
        "high",
        "PwC (reviewed 2026-06-24): state tax steps to 19-30.25% (EUR 21.2K-40.1K brackets) + municipal + soc. contrib. blended ~31% at mid band",
      ),
      high: m(
        0.48,
        "high",
        "PwC (reviewed 2026-06-24): state tax 33.25-37.5% above EUR 40,100/52,100 + municipal + soc. contrib. blended ~48% at high band",
      ),
    },
    healthcareModelType: "tax-funded",
    compulsoryInsurance: {
      health: false,
      socialSecurity: true,
      note: "TyEL pension ~7.15% + unemployment insurance employee mandatory; health primarily tax-funded, Kela refunds partial",
    },
  },
  {
    id: "us",
    foreignerPublicSchool: {
      access: "open",
      confidence: "high",
      note: "Work-visa kids attend free; Plyler v. Doe bars status discrimination; no quota or fee. US State Dept",
    },
    name: { en: "United States", id: "Amerika Serikat" },
    bandThresholdsUsd: { lowToMid: 3500, midToHigh: 9000 },
    effectiveRate: {
      low: m(
        0.15,
        "high",
        "PwC (US, current 2025-26 filing year): federal income tax + FICA 7.65% (6.2% SS capped at $184,500 wage base 2026 + 1.45% Medicare) ~15% at low band",
      ),
      mid: m(
        0.26,
        "high",
        "PwC: federal brackets + FICA ~26% at mid band; blended composite across CA/NY/TX — no separate state layer at country level",
      ),
      high: m(
        0.36,
        "high",
        "PwC: top federal marginal 37% (2025-26); effective ~36% at high band before additional Medicare surtax 0.9%",
      ),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: false,
      socialSecurity: true,
      note: "FICA: 6.2% SS (capped $184,500 2026 wage base) + 1.45% Medicare mandatory; employer health near-universal for tech",
    },
  },
  {
    id: "ca",
    foreignerPublicSchool: {
      access: "open",
      confidence: "high",
      note: "Free K-12 for valid work-permit holders' kids in most provinces; Quebec may add conditions. WorkPermitCheck 2024",
    },
    name: { en: "Canada", id: "Kanada" },
    bandThresholdsUsd: { lowToMid: 3500, midToHigh: 8000 },
    effectiveRate: {
      low: m(
        0.18,
        "high",
        "PwC Canada (2025): federal lowest PIT bracket cut 15%→14.5% (2025)/14% (2026) + CPP 5.95% + EI 1.66% ~18% at low band",
      ),
      mid: m(0.29, "high", "PwC Canada (2025): federal + provincial blended + CPP/EI ~29% at mid band"),
      high: m(0.4, "high", "PwC Canada (2025): federal top 33% + provincial blended ~40% at high band"),
    },
    healthcareModelType: "tax-funded",
    compulsoryInsurance: {
      health: false,
      socialSecurity: true,
      note: "CPP 5.95% + EI 1.66% employee mandatory; provincial health (OHIP/MSP) tax-funded",
    },
  },
  {
    id: "br",
    foreignerPublicSchool: {
      access: "open",
      confidence: "high",
      note: "Constitution + Lei 13.445/2017 bar nationality-based exclusion; free public schools for all residents. Library of Congress 2017",
    },
    name: { en: "Brazil", id: "Brasil" },
    bandThresholdsUsd: { lowToMid: 1500, midToHigh: 4500 },
    effectiveRate: {
      low: m(0.1, "moderate", "PwC Brazil: IRPF progressive + INSS employee ceiling contribution ~10% at low band"),
      mid: m(0.23, "moderate", "PwC Brazil: IRPF ~23% at mid band"),
      high: m(
        0.35,
        "moderate",
        "PwC Brazil: IRPF 27.5% top marginal + new IRPFM minimum tax (Law 15.270/2025) up to 10% surtax above BRL 600K/yr for very high earners ~35% effective",
      ),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: false,
      socialSecurity: true,
      note: "INSS 7.5-14% employee (progressive, capped); SUS public health exists; private plano dominates middle class",
    },
  },
  {
    id: "mx",
    foreignerPublicSchool: {
      access: "open",
      confidence: "high",
      note: "Constitution Art.3 universal free basic education; no nationality bar; revalidacion for transcripts. SEP guides 2024",
    },
    name: { en: "Mexico", id: "Meksiko" },
    bandThresholdsUsd: { lowToMid: 1500, midToHigh: 4000 },
    effectiveRate: {
      low: m(
        0.08,
        "moderate",
        "PwC Mexico: ISR 11-bracket progressive (1.92-35%) + IMSS/AFORE employee ~4.1% ~8% at low band, offset by subsidy below MXN 10,171/mo",
      ),
      mid: m(
        0.21,
        "moderate",
        "PwC Mexico: ISR ~17.92-23.52% typical mid bracket + IMSS/AFORE ~21% blended at mid band",
      ),
      high: m(
        0.33,
        "moderate",
        "PwC Mexico: ISR top 35% above MXN 3,898,140/yr (2026) + IMSS/AFORE ~33% effective at high band",
      ),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: true,
      socialSecurity: true,
      note: "IMSS health + AFORE pension contributions ~4.1% employee mandatory for formal employment",
    },
  },
  // ── Middle East, South Asia, East Asia, Oceania, Africa ──
  {
    id: "ae",
    foreignerPublicSchool: {
      access: "limited",
      confidence: "high",
      note: "Expats pay AED 6,000/yr, Arabic-medium, 85% grade + 20% quota + govt-employer condition; ~75% use private. UAE Gov 2024 (unchanged 2026)",
    },
    name: { en: "United Arab Emirates", id: "Uni Emirat Arab" },
    bandThresholdsUsd: { lowToMid: 5000, midToHigh: 15000 },
    effectiveRate: {
      low: m(
        0.0,
        "high",
        "PwC Worldwide Tax Summaries, accessed 2026-07-30: UAE levies no personal income tax on individuals",
      ),
      mid: m(
        0.0,
        "high",
        "PwC Worldwide Tax Summaries, accessed 2026-07-30: UAE levies no personal income tax on individuals",
      ),
      high: m(
        0.0,
        "high",
        "PwC Worldwide Tax Summaries, accessed 2026-07-30: no personal income tax; natural-person business turnover >AED 1M subject to 9% UAE corporate tax, not applicable to salaried employees",
      ),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: true,
      socialSecurity: false,
      note: "Employer mandatory health insurance (DHA/HAAD regulation); no public pension for expats",
    },
  },
  {
    id: "in",
    foreignerPublicSchool: {
      access: "limited",
      confidence: "moderate",
      note: "RTE Act is age-based (not citizenship); Hindi/regional-medium; virtually all expats use intl schools. Expat Arrivals 2024 (unchanged 2026)",
    },
    name: { en: "India", id: "India" },
    bandThresholdsUsd: { lowToMid: 1000, midToHigh: 3500 },
    effectiveRate: {
      low: m(
        0.0,
        "moderate",
        "PwC India new-regime FY2025-26 slabs (rev. 2026-05-12) + ₹75,000 std deduction + Sec 87A rebate (full rebate to tax ≤₹60,000 when taxable ≤₹12L): at representative ~$1,000/mo gross (~₹10.6L/yr, USD/INR≈88) net tax ≈0 — a material 2025 Union Budget change vs. prior ~5% estimate",
      ),
      mid: m(
        0.12,
        "moderate",
        "PwC India new-regime FY2025-26 slabs + 4% cess, no rebate above ₹12L taxable: at representative ~$2,250/mo gross (~₹23.8L/yr) effective ≈12%",
      ),
      high: m(
        0.25,
        "moderate",
        "PwC India new-regime FY2025-26 slabs + 10% surcharge (>₹50L) + 4% cess: at representative ~$5,250/mo gross (~₹55.4L/yr) effective ≈25%, down from prior ~33% estimate",
      ),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: false,
      socialSecurity: true,
      note: "EPF 12% employee; ESI for lower income; tech workers typically above ESI threshold",
    },
  },
  {
    id: "kr",
    foreignerPublicSchool: {
      access: "open",
      confidence: "high",
      note: "Free public elementary; enrolment cannot be refused; Korean-only instruction is a practical, not legal, barrier. Seoul Gov 2024 (unchanged 2026)",
    },
    name: { en: "South Korea", id: "Korea Selatan" },
    bandThresholdsUsd: { lowToMid: 2500, midToHigh: 7000 },
    effectiveRate: {
      low: m(
        0.1,
        "high",
        "PwC Worldwide Tax Summaries (rev. 2026-07-02): national PIT brackets unchanged since 2023 (6%-45%) + 10% local income-tax surtax + NHI 3.545% + NPS 4.5%; ~10% effective at low band after earned-income deduction (deduction schedule not independently recomputed this cycle)",
      ),
      mid: m(
        0.23,
        "high",
        "PwC Worldwide Tax Summaries (rev. 2026-07-02): brackets unchanged; ~23% effective at mid band",
      ),
      high: m(
        0.38,
        "high",
        "PwC Worldwide Tax Summaries (rev. 2026-07-02): brackets unchanged; ~38% effective at high band",
      ),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: true,
      socialSecurity: true,
      note: "NHI (NHIS) 3.545% employee + NPS 4.5% mandatory; 60-70% coverage",
    },
  },
  {
    id: "au",
    foreignerPublicSchool: {
      access: "limited",
      confidence: "high",
      note: "482-visa kids enrol in all states but fees vary; NSW/WA charge temp-visa families (WA ~A$4,000/yr). State edu depts 2024 (unchanged 2026)",
    },
    name: { en: "Australia", id: "Australia" },
    bandThresholdsUsd: { lowToMid: 3500, midToHigh: 8500 },
    effectiveRate: {
      low: m(
        0.18,
        "moderate",
        "Own calc from PwC/ATO 2025-26 resident brackets (0/16/30/37/45%) + 2% Medicare levy at representative ~$3,500/mo gross (~AUD 63,000/yr, USD/AUD≈1.50): effective ≈18%",
      ),
      mid: m(
        0.24,
        "moderate",
        "Own calc, representative ~$6,000/mo gross (~AUD 108,000/yr): effective ≈24% — down from prior 33% estimate",
      ),
      high: m(
        0.36,
        "moderate",
        "Own calc, representative ~$17,000/mo gross (~AUD 306,000/yr): effective ≈36%; NOTE prior 47% figure equals the top marginal rate (45%+2% Medicare), not an average effective rate",
      ),
    },
    healthcareModelType: "tax-funded",
    compulsoryInsurance: {
      health: false,
      socialSecurity: true,
      note: "Superannuation 11.5% employer-paid; Medicare Levy 2% employee; Medicare tax-funded",
    },
  },
  {
    id: "ke",
    foreignerPublicSchool: {
      access: "open",
      confidence: "moderate",
      note: "Basic Education Act 2013 covers residents; fees may apply to non-citizens but no exclusion; free primary in practice. Kenya Law 2022 (unchanged 2026)",
    },
    name: { en: "Kenya", id: "Kenya" },
    bandThresholdsUsd: { lowToMid: 800, midToHigh: 2500 },
    effectiveRate: {
      low: m(
        0.27,
        "moderate",
        "Own calc from KRA Finance Act 2025 PAYE bands (10/25/30/32.5/35%) + personal relief KES 2,400/mo + SHIF 2.75% + NSSF 6% + Housing Levy 1.5%, at representative ~$400/mo gross (~KES 58,000/mo, USD/KES≈145): effective ≈27% — up from prior 10%",
      ),
      mid: m(0.34, "moderate", "Own calc, representative ~$1,650/mo gross (~KES 239,000/mo): effective ≈34%"),
      high: m(
        0.34,
        "moderate",
        "Own calc, representative ~$3,750/mo gross (~KES 544,000/mo): effective ≈34% (NSSF caps ~KES 108,000/mo pensionable pay under Feb-2026 phased schedule, flattening the curve)",
      ),
    },
    healthcareModelType: "mixed",
    compulsoryInsurance: {
      health: true,
      socialSecurity: true,
      note: "SHIF 2.75% + NSSF 6% + Affordable Housing Levy 1.5% mandatory; private insurance common in formal sector",
    },
  },
];

// ─── Cities ──────────────────────────────────────────────────────────────────

export const cities: City[] = [
  // ══════════════════════════════════════════
  // ASEAN
  // ══════════════════════════════════════════
  {
    id: "singapore",
    name: { en: "Singapore", id: "Singapura" },
    countryId: "sg",
    currency: "SGD",
    region: "asean",
    expenses: {
      housing: m(3830, "high", "Numbeo Jul 2026: 1BR city centre avg S$3,830.43 (range S$2,500–6,000)"),
      food: m(
        420,
        "moderate",
        "Numbeo Jul 2026: meal-for-2 mid-range avg S$80 (3-course) + groceries composite ~420 SGD/mo",
      ),
      transport: m(128, "high", "Numbeo Jul 2026: monthly public transport pass avg S$128.00 (range S$122–200)"),
      utilities: m(210, "high", "Numbeo Jul 2026: basic utilities 85m² avg S$209.40 (range S$134.21–323.81)"),
      healthcare: m(
        130,
        "moderate",
        "OOP only: GP copay + dental estimate; MediShield Life premiums captured in effectiveRate",
      ),
      childcare: m(
        1830,
        "high",
        "Numbeo Jul 2026: private full-day preschool avg S$1,829.79/mo (range S$1,200–2,686.42)",
      ),
      lifestyle: m(
        260,
        "moderate",
        "Numbeo Jul 2026: fitness club avg S$136.74 (range S$90–240) + entertainment/clothing composite",
      ),
    },
    childcareMedianLocal: m(1830, "high", "Numbeo Jul 2026 median private full-day preschool"),
    schoolMedianLocal: {
      public: m(160, "high", "MOE 2026: primary school miscellaneous fees ~S$160/mo"),
      private: m(
        2930,
        "moderate",
        "Numbeo Jul 2026: international primary school avg S$35,184.67/yr (range S$25,000–50,000) = ~S$2,932/mo",
      ),
    },
    relocation: {
      sunkCosts: {
        deposit: m(7660, "moderate", "2× updated month rent (S$3,830); standard for Singapore private rental"),
        keyMoney: m(0, "high", "N/A: no key money custom in Singapore"),
        moving: m(3600, "moderate", "International shipping + local transport estimate"),
        visaAdmin: m(
          700,
          "moderate",
          "MOM 2026: EP application S$105 + issuance S$225 + dependant pass ~S$330 = ~S$700 total",
        ),
      },
      liquidityReserve: {
        cashCushion: m(15500, "moderate", "3× monthly essentials incl. housing (~5,170 SGD/mo updated); rounded"),
      },
    },
  },
  {
    id: "bangkok",
    name: { en: "Bangkok", id: "Bangkok" },
    countryId: "th",
    currency: "THB",
    region: "asean",
    expenses: {
      housing: m(23000, "high", "Numbeo Jul 2026: 1BR city centre avg ฿22,775 (range ฿15,000–35,000)"),
      food: m(8200, "moderate", "Numbeo Jul 2026: meal-for-2 mid-range avg ฿1,200 + groceries composite ~8,200 THB/mo"),
      transport: m(1200, "high", "Numbeo Jul 2026: monthly public transport pass avg ฿1,155 (range ฿900–2,000)"),
      utilities: m(3300, "high", "Numbeo Jul 2026: basic utilities 85m² avg ฿3,304 (range ฿2,125–5,100)"),
      healthcare: m(2100, "moderate", "OOP: clinic visit + meds estimate; SSF covers formal employed"),
      childcare: m(17500, "high", "Numbeo Jul 2026: private full-day preschool avg ฿17,470/mo (range ฿10,000–28,000)"),
      lifestyle: m(
        4200,
        "moderate",
        "Numbeo Jul 2026: fitness club avg ฿1,994 (range ฿900–3,000) + social/clothing composite",
      ),
    },
    childcareMedianLocal: m(17500, "high", "Numbeo Jul 2026 median private preschool Bangkok"),
    schoolMedianLocal: {
      public: m(1100, "moderate", "Thai public school misc fees ~1,100 THB/mo (non-citizens pay more)"),
      private: m(
        43750,
        "moderate",
        "Numbeo Jul 2026: international primary school avg ฿524,967/yr (range ฿300,000–810,000) = ~฿43,747/mo",
      ),
    },
    relocation: {
      sunkCosts: {
        deposit: m(46000, "moderate", "2× updated month rent (฿23,000)"),
        keyMoney: m(0, "high", "N/A: no key money in Thailand"),
        moving: m(31000, "moderate", "International shipping estimate in THB"),
        visaAdmin: m(8000, "moderate", "Siam Legal 2026: Non-Immigrant B visa ฿2,000–5,000 + work permit ฿3,000/yr"),
      },
      liquidityReserve: {
        cashCushion: m(105000, "moderate", "3× monthly essentials incl. housing (~฿34,500/mo updated)"),
      },
    },
  },
  {
    id: "jakarta",
    name: { en: "Jakarta", id: "Jakarta" },
    countryId: "id",
    currency: "IDR",
    region: "asean",
    expenses: {
      housing: m(6300000, "high", "Numbeo Jul 2026: 1BR city centre avg Rp6,315,385 (range Rp5,000,000–9,360,000)"),
      food: m(
        3100000,
        "moderate",
        "Numbeo Jul 2026: meal-for-2 mid-range avg Rp300,000 + warung/groceries composite ~3.1M IDR/mo",
      ),
      transport: m(
        500000,
        "moderate",
        "Numbeo Jul 2026 transit pass avg Rp210,000; MRT + TransJakarta + last-mile car-free estimate",
      ),
      utilities: m(
        1750000,
        "high",
        "Numbeo Jul 2026: basic utilities 85m² avg Rp1,766,452 (range Rp850,000–4,000,000)",
      ),
      healthcare: m(550000, "moderate", "OOP: clinic estimate; BPJS Kesehatan covers formal employed"),
      childcare: m(
        3500000,
        "moderate",
        "Numbeo Jul 2026 avg Rp2,740,227 (range Rp1,500,000–7,500,000); expat/bilingual preschool skews higher",
      ),
      lifestyle: m(
        2200000,
        "moderate",
        "Numbeo Jul 2026: fitness avg Rp487,500 (range Rp250,000–1,500,000) + social composite",
      ),
    },
    childcareMedianLocal: m(3500000, "moderate", "Jakarta bilingual preschool median, blended with Numbeo Jul 2026"),
    schoolMedianLocal: {
      public: m(210000, "moderate", "Indonesian public school misc fees ~210K IDR/mo"),
      private: m(
        12200000,
        "moderate",
        "Numbeo Jul 2026: international primary school avg Rp146,900,000/yr (range Rp84,000,000–400,000,000) = ~Rp12.2M/mo",
      ),
    },
    relocation: {
      sunkCosts: {
        deposit: m(12600000, "moderate", "2× updated month rent (Rp6.3M)"),
        keyMoney: m(0, "high", "N/A: no key money in Indonesia"),
        moving: m(10500000, "moderate", "International shipping estimate in IDR"),
        visaAdmin: m(5200000, "moderate", "KITAS work visa processing ~Rp5.2M"),
      },
      liquidityReserve: {
        cashCushion: m(33000000, "moderate", "3× monthly essentials incl. housing (~Rp11M/mo updated)"),
      },
    },
  },
  {
    id: "kuala-lumpur",
    name: { en: "Kuala Lumpur", id: "Kuala Lumpur" },
    countryId: "my",
    currency: "MYR",
    region: "asean",
    expenses: {
      housing: m(2590, "high", "Numbeo Jul 2026: 1BR city centre avg RM2,587.50 (range RM1,700–4,000)"),
      food: m(
        820,
        "moderate",
        "Numbeo Jul 2026: meal-for-2 mid-range avg RM100 + hawker/groceries composite ~820 MYR/mo",
      ),
      transport: m(
        100,
        "moderate",
        "Numbeo Jul 2026: Rapid KL monthly pass avg RM50; blended with typical mixed-mode commute",
      ),
      utilities: m(260, "high", "Numbeo Jul 2026: basic utilities 85m² avg RM258.65 (range RM160–350)"),
      healthcare: m(210, "moderate", "OOP: private clinic estimate; public subsidized but queues"),
      childcare: m(1150, "high", "Numbeo Jul 2026: private full-day preschool avg RM1,129/mo (range RM700–3,333)"),
      lifestyle: m(420, "moderate", "Numbeo Jul 2026: fitness avg RM196.10 (range RM100–280) + social composite"),
    },
    childcareMedianLocal: m(1150, "high", "Numbeo Jul 2026 median private preschool KL"),
    schoolMedianLocal: {
      public: m(110, "moderate", "Malaysian public school misc fees ~110 MYR/mo"),
      private: m(
        4100,
        "moderate",
        "Numbeo Jul 2026: international primary school avg RM49,329/yr (range RM24,000–97,599) = ~RM4,111/mo",
      ),
    },
    relocation: {
      sunkCosts: {
        deposit: m(5180, "moderate", "2× updated month rent (RM2,590)"),
        keyMoney: m(0, "high", "N/A"),
        moving: m(3100, "moderate", "International shipping estimate MYR"),
        visaAdmin: m(2500, "moderate", "AYP Group 2026: 5-yr Category I Employment Pass gov fees RM1,500–3,500"),
      },
      liquidityReserve: {
        cashCushion: m(11000, "moderate", "3× monthly essentials incl. housing (~RM3,650/mo updated)"),
      },
    },
  },
  {
    id: "ho-chi-minh-city",
    name: { en: "Ho Chi Minh City", id: "Ho Chi Minh City" },
    countryId: "vn",
    currency: "VND",
    region: "asean",
    expenses: {
      housing: m(15000000, "high", "Numbeo Jul 2026: 1BR city centre avg ₫14,977,589 (range ₫12,000,000–25,000,000)"),
      food: m(
        5100000,
        "moderate",
        "Numbeo Jul 2026: meal-for-2 mid-range avg ₫550,000 + pho/groceries composite ~5.1M VND/mo",
      ),
      transport: m(400000, "moderate", "Numbeo Jul 2026 transit pass avg ₫300,000; Grab top-up blended estimate"),
      utilities: m(
        2500000,
        "high",
        "Numbeo Jul 2026: basic utilities 85m² avg ₫2,537,087 (range ₫1,500,000–5,312,500)",
      ),
      healthcare: m(520000, "moderate", "OOP: private clinic visit estimate; VSS covers formal employed"),
      childcare: m(
        12400000,
        "high",
        "Numbeo Jul 2026: private full-day preschool avg ₫12,420,939/mo (range ₫7,500,000–25,000,000)",
      ),
      lifestyle: m(
        2200000,
        "moderate",
        "Numbeo Jul 2026: fitness avg ₫600,000 (range ₫300,000–1,600,000) + social composite",
      ),
    },
    childcareMedianLocal: m(12400000, "high", "Numbeo Jul 2026 median private preschool HCMC"),
    schoolMedianLocal: {
      public: m(520000, "moderate", "Vietnamese public school misc fees"),
      private: m(
        35000000,
        "moderate",
        "Numbeo Jul 2026 mean skews to premium tier (₫592.8M/yr); mid-tier intl school blended estimate ~₫35M/mo (₫420M/yr)",
      ),
    },
    relocation: {
      sunkCosts: {
        deposit: m(30000000, "moderate", "2× updated month rent (₫15M)"),
        keyMoney: m(0, "high", "N/A"),
        moving: m(15500000, "moderate", "International shipping estimate VND"),
        visaAdmin: m(5200000, "moderate", "Work permit + TRC fees ~5.2M VND"),
      },
      liquidityReserve: {
        cashCushion: m(68000000, "moderate", "3× monthly essentials incl. housing (~₫22.5M/mo updated)"),
      },
    },
  },
  {
    id: "manila",
    name: { en: "Manila", id: "Manila" },
    countryId: "ph",
    currency: "PHP",
    region: "asean",
    expenses: {
      housing: m(33250, "high", "Numbeo Jul 2026: 1BR city centre avg ₱33,243 (range ₱24,000–49,134)"),
      food: m(
        12300,
        "moderate",
        "Numbeo Jul 2026: meal-for-2 mid-range avg ₱1,600 + tindahan/groceries composite ~12.3K PHP/mo",
      ),
      transport: m(1000, "moderate", "Numbeo Jul 2026 transit pass avg ₱800; MRT + jeepney blended estimate"),
      utilities: m(7500, "high", "Numbeo Jul 2026: basic utilities 85m² avg ₱7,544 (range ₱5,000–12,000)"),
      healthcare: m(3200, "moderate", "OOP: private clinic estimate; PhilHealth covers some"),
      childcare: m(
        20000,
        "moderate",
        "Numbeo Jul 2026 mean skews to premium tier (₱35,987/mo); mainstream preschool estimate ~₱20K/mo",
      ),
      lifestyle: m(6500, "moderate", "Numbeo Jul 2026: fitness avg ₱2,710 (range ₱1,099–5,000) + social composite"),
    },
    childcareMedianLocal: m(20000, "moderate", "Manila private preschool median, blended with Numbeo Jul 2026"),
    schoolMedianLocal: {
      public: m(520, "moderate", "Philippine public school misc fees ~520 PHP/mo"),
      private: m(
        40000,
        "moderate",
        "Numbeo Jul 2026 mean ₱560,391/yr (range ₱250,000–900,000); mid-tier intl school blended estimate ~₱40K/mo",
      ),
    },
    relocation: {
      sunkCosts: {
        deposit: m(66500, "moderate", "2× updated month rent (₱33,250)"),
        keyMoney: m(0, "high", "N/A"),
        moving: m(41000, "moderate", "International shipping estimate PHP"),
        visaAdmin: m(10500, "moderate", "9(g) work visa fees ~₱10,500"),
      },
      liquidityReserve: {
        cashCushion: m(155000, "moderate", "3× monthly essentials incl. housing (~₱52,000/mo updated)"),
      },
    },
  },
  // ══════════════════════════════════════════
  // Japan
  // ══════════════════════════════════════════
  {
    id: "tokyo",
    name: { en: "Tokyo", id: "Tokyo" },
    countryId: "jp",
    currency: "JPY",
    region: "japan",
    expenses: {
      housing: m(197000, "high", "Numbeo Jul 2026: 1BR city centre 196,917 JPY/mo"),
      food: m(
        55000,
        "moderate",
        "Numbeo Jul 2026: meal-for-two mid-range 7,000 JPY + estimated groceries; combined ~55K JPY/mo",
      ),
      transport: m(12000, "high", "Numbeo Jul 2026: monthly public transport pass 12,000 JPY"),
      utilities: m(25000, "high", "Numbeo Jul 2026: elec+gas+water 85m² ~25,234 JPY/mo"),
      healthcare: m(10000, "moderate", "OOP copay only (30%); JHI premiums inside effectiveRate"),
      childcare: m(
        55000,
        "moderate",
        "Numbeo Jul 2026 raw 215,055 JPY skewed by international-preschool entries; using typical hoikuen range 40K-60K JPY/mo per municipal fee schedules",
      ),
      lifestyle: m(30000, "moderate", "Numbeo Jun 2026: gym+izakaya+clothing ~30K JPY/mo"),
    },
    childcareMedianLocal: m(55000, "moderate", "Tokyo private hoikuen/preschool median"),
    schoolMedianLocal: {
      public: m(3000, "high", "MEXT 2026: public school misc fees ~3,000 JPY/mo"),
      private: m(
        230000,
        "high",
        "Numbeo Jul 2026: international primary school annual tuition 2,760,000 JPY/yr = 230,000 JPY/mo",
      ),
    },
    relocation: {
      sunkCosts: {
        deposit: m(394000, "high", "2× rent shikikin on updated Tokyo rent"),
        keyMoney: m(197000, "high", "1× rent reikin (non-refundable) — still common in central Tokyo"),
        moving: m(100000, "moderate", "International + local move estimate JPY"),
        visaAdmin: m(50000, "moderate", "Engineer/Specialist Humanities visa COE + agent fees"),
      },
      liquidityReserve: {
        cashCushion: m(690000, "moderate", "3× monthly essentials (~230K JPY/mo on updated figures)"),
      },
    },
  },
  {
    id: "osaka",
    name: { en: "Osaka", id: "Osaka" },
    countryId: "jp",
    currency: "JPY",
    region: "japan",
    expenses: {
      housing: m(112000, "high", "Numbeo Jun 2026: 1BR city centre 112,000 JPY/mo"),
      food: m(
        45000,
        "moderate",
        "Numbeo Jun 2026: meal-for-two mid-range 5,000 JPY + estimated groceries; combined ~45K JPY/mo",
      ),
      transport: m(
        8000,
        "moderate",
        "Numbeo Jun 2026 single-zone pass 5,150 JPY; typical cross-line Osaka Metro commuter pass runs 8K-10K JPY/mo",
      ),
      utilities: m(20700, "high", "Numbeo Jun 2026: elec+gas+water 85m² ~20,652 JPY/mo"),
      healthcare: m(8000, "moderate", "OOP copay 30%; JHI premiums in effectiveRate"),
      childcare: m(
        60000,
        "moderate",
        "Numbeo Jun 2026 raw 81,614 JPY; blended with typical Osaka hoikuen range 40K-50K JPY/mo per city fee schedules",
      ),
      lifestyle: m(25000, "moderate", "Numbeo Jun 2026: gym+social ~25K JPY/mo"),
    },
    childcareMedianLocal: m(60000, "moderate", "Osaka private hoikuen median"),
    schoolMedianLocal: {
      public: m(3000, "high", "MEXT 2026: public school misc fees ~3,000 JPY/mo"),
      private: m(70000, "moderate", "Private school Osaka ~60K-80K JPY/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(224000, "high", "2× rent shikikin Osaka on updated rent"),
        keyMoney: m(112000, "high", "1× rent reikin — still encountered in central Osaka"),
        moving: m(80000, "moderate", "International + local move estimate JPY"),
        visaAdmin: m(50000, "moderate", "Engineer visa COE + agent fees"),
      },
      liquidityReserve: {
        cashCushion: m(510000, "moderate", "3× monthly essentials (~170K JPY/mo on updated figures)"),
      },
    },
  },
  {
    id: "london",
    name: { en: "London", id: "London" },
    countryId: "gb",
    currency: "GBP",
    region: "europe",
    expenses: {
      housing: m(2290, "high", "Numbeo Jul 2026: 1BR city centre 2,289.29 GBP/mo"),
      food: m(520, "moderate", "Numbeo Jul 2026: meal-for-two mid-range 80 GBP + groceries; combined ~520 GBP/mo"),
      transport: m(200, "high", "Numbeo Jul 2026: monthly public transport pass 200 GBP; TfL zones 1-2 Travelcard"),
      utilities: m(291, "high", "Numbeo Jul 2026: elec+gas+water 85m² 291.03 GBP/mo"),
      healthcare: m(55, "high", "OOP: prescriptions ~GBP 9.90 each + dental; NHS free at point of use"),
      childcare: m(2000, "high", "Numbeo Jul 2026: private nursery 2,013.95 GBP/mo"),
      lifestyle: m(310, "moderate", "Numbeo Jun 2026: gym+pub+clothing ~310 GBP/mo"),
    },
    childcareMedianLocal: m(2000, "high", "London private nursery median, Numbeo Jul 2026"),
    schoolMedianLocal: {
      public: m(50, "high", "State school misc extras ~50 GBP/mo; tuition free"),
      private: m(2100, "moderate", "Independent day school London ~1,900-2,300 GBP/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(4580, "moderate", "2× month rent deposit (tenancy deposit scheme) on updated rent"),
        keyMoney: m(0, "high", "N/A: banned under Tenant Fees Act 2019"),
        moving: m(1500, "moderate", "International shipping + van hire estimate"),
        visaAdmin: m(1200, "moderate", "Skilled Worker visa + IHS surcharge (year 1) ~1,200 GBP"),
      },
      liquidityReserve: {
        cashCushion: m(9700, "moderate", "3× monthly essentials (~3,230 GBP/mo on updated figures)"),
      },
    },
  },
  {
    id: "berlin",
    name: { en: "Berlin", id: "Berlin" },
    countryId: "de",
    currency: "EUR",
    region: "europe",
    expenses: {
      housing: m(1315, "high", "Numbeo Jul 2026: 1BR city centre 1,314.48 EUR/mo (Mitte/Prenzlauer Berg)"),
      food: m(390, "moderate", "Numbeo Jul 2026: meal-for-two mid-range 74.25 EUR + groceries; combined ~390 EUR/mo"),
      transport: m(
        63,
        "high",
        "Deutschlandticket cut to 63 EUR/mo effective Jan 2026 (iamexpat.de / bahn.de); matches Numbeo Jul 2026",
      ),
      utilities: m(355, "high", "Numbeo Jul 2026: elec+heating+water+garbage 85m² 354.96 EUR/mo"),
      healthcare: m(30, "high", "OOP: copay minimal; GKV covers most; prescription copay 5-10 EUR"),
      childcare: m(
        136,
        "high",
        "Berlin Kita tuition-free since 2018 (Kostenfreiheit); ~136 EUR/mo is Verpflegungsgeld (meals) only. Numbeo Jul 2026",
      ),
      lifestyle: m(250, "moderate", "Numbeo Jun 2026: gym+bar+clothing ~250 EUR/mo"),
    },
    childcareMedianLocal: m(136, "high", "Berlin Kita meal-fee median (tuition-free), Numbeo Jul 2026"),
    schoolMedianLocal: {
      public: m(0, "high", "German state school: free; misc ~20 EUR/mo"),
      private: m(1500, "moderate", "Private/international school Berlin ~1,200-1,800 EUR/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(3945, "moderate", "3× rent Kaution on updated rent; BGB max 3 months"),
        keyMoney: m(0, "high", "N/A: prohibited under German tenancy law"),
        moving: m(1500, "moderate", "International shipping estimate EUR"),
        visaAdmin: m(500, "moderate", "EU Blue Card or Niederlassungserlaubnis fees ~500 EUR"),
      },
      liquidityReserve: {
        cashCushion: m(5700, "moderate", "3× monthly essentials (~1,900 EUR/mo on updated figures)"),
      },
    },
  },
  {
    id: "amsterdam",
    name: { en: "Amsterdam", id: "Amsterdam" },
    countryId: "nl",
    currency: "EUR",
    region: "europe",
    expenses: {
      housing: m(2280, "high", "Numbeo Jul 2026: 1BR city centre 2,280.77 EUR/mo"),
      food: m(460, "moderate", "Numbeo Jul 2026: meal-for-two mid-range 80 EUR + groceries; combined ~460 EUR/mo"),
      transport: m(100, "high", "Numbeo Jul 2026: GVB/NS monthly equivalent 100 EUR/mo"),
      utilities: m(272, "high", "Numbeo Jul 2026: elec+heating+cooling+water+garbage 85m² 271.54 EUR/mo"),
      healthcare: m(100, "high", "OOP: ZVW deductible ~385-435 EUR/yr split ~33/mo + copays"),
      childcare: m(
        1050,
        "moderate",
        "Numbeo Jul 2026 gross private full-day fee 2,461.81 EUR/mo; net cost after kinderopvangtoeslag subsidy for a mid-high earner is materially lower, ~950-1,150 EUR/mo",
      ),
      lifestyle: m(300, "moderate", "Numbeo Jun 2026: gym+cafe+cycling ~300 EUR/mo"),
    },
    childcareMedianLocal: m(1050, "moderate", "Amsterdam kinderopvang net median after subsidy"),
    schoolMedianLocal: {
      public: m(0, "high", "Dutch public school: free; misc ~25 EUR/mo"),
      private: m(1600, "moderate", "International school Amsterdam ~1,400-1,800 EUR/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(4560, "moderate", "2× rent deposit typical on updated rent"),
        keyMoney: m(0, "high", "N/A"),
        moving: m(1500, "moderate", "International shipping estimate EUR"),
        visaAdmin: m(500, "moderate", "GVVA / highly skilled migrant permit ~500 EUR"),
      },
      liquidityReserve: {
        cashCushion: m(9000, "moderate", "3× monthly essentials (~3,000 EUR/mo on updated figures)"),
      },
    },
  },
  {
    id: "lisbon",
    name: { en: "Lisbon", id: "Lisbon" },
    countryId: "pt",
    currency: "EUR",
    region: "europe",
    expenses: {
      housing: m(1440, "high", "Numbeo Jul 2026: 1BR city centre 1,442.86 EUR/mo"),
      food: m(360, "moderate", "Numbeo Jul 2026: meal-for-two mid-range 55 EUR + groceries; combined ~360 EUR/mo"),
      transport: m(40, "high", "Numbeo Jul 2026: 40 EUR/mo, matches Carris/Metro Navegante fixed pass price"),
      utilities: m(150, "high", "Numbeo Jul 2026: elec+water+internet 85m² 150.37 EUR/mo"),
      healthcare: m(50, "high", "OOP: SNS copay (taxa moderadora) ~5 EUR/visit + dental"),
      childcare: m(
        610,
        "moderate",
        "Numbeo Jul 2026: private preschool 606.25 EUR/mo; public creche ~150 EUR/mo where available",
      ),
      lifestyle: m(200, "moderate", "Numbeo Jun 2026: pastel+gym+clothing ~200 EUR/mo"),
    },
    childcareMedianLocal: m(610, "moderate", "Lisbon private creche median, Numbeo Jul 2026"),
    schoolMedianLocal: {
      public: m(0, "high", "Portuguese public school: free; misc ~15 EUR/mo"),
      private: m(800, "moderate", "Private school Lisbon ~700-1,000 EUR/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(2880, "moderate", "2× rent deposit on updated rent"),
        keyMoney: m(0, "high", "N/A"),
        moving: m(1200, "moderate", "International shipping estimate EUR"),
        visaAdmin: m(300, "moderate", "D2/D3/D8 visa + SEF/AIMA appointment fees ~300 EUR"),
      },
      liquidityReserve: {
        cashCushion: m(5600, "moderate", "3× monthly essentials (~1,870 EUR/mo on updated figures)"),
      },
    },
  },
  {
    id: "zurich",
    name: { en: "Zurich", id: "Zürich" },
    countryId: "ch",
    currency: "CHF",
    region: "europe",
    expenses: {
      housing: m(2400, "high", "Numbeo Jul 2026: 1BR city centre 2,400.91 CHF/mo"),
      food: m(720, "moderate", "Numbeo Jul 2026: meal-for-two mid-range 120 CHF + groceries; combined ~720 CHF/mo"),
      transport: m(88, "high", "Numbeo Jul 2026: monthly pass 88 CHF; ZVV Zone 110 Abo"),
      utilities: m(225, "high", "Numbeo Jul 2026: elec+heat+water 85m² 225.34 CHF/mo"),
      healthcare: m(150, "high", "OOP copay only: Franchise split ~90/mo + 10% copay; LAMal premium in effectiveRate"),
      childcare: m(
        2800,
        "moderate",
        "Numbeo Jul 2026: 2,927.31 CHF/mo private full-day Kita; consistent with well-documented CHF 2,500-3,500/mo Zurich range",
      ),
      lifestyle: m(400, "moderate", "Numbeo Jun 2026: gym+cafe+recreation ~400 CHF/mo"),
    },
    childcareMedianLocal: m(2800, "moderate", "Zurich Kita median, Numbeo Jul 2026"),
    schoolMedianLocal: {
      public: m(200, "high", "Swiss public school misc fees ~200 CHF/mo"),
      private: m(2500, "moderate", "International school Zurich ~2,200-2,800 CHF/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(7200, "high", "3× rent deposit on updated rent; OR 3 months max per OR 720"),
        keyMoney: m(0, "high", "N/A: no key money in Switzerland"),
        moving: m(3000, "moderate", "International shipping + Swiss moving company estimate"),
        visaAdmin: m(1000, "moderate", "B permit (EU) or L permit processing + relocation admin"),
      },
      liquidityReserve: {
        cashCushion: m(13500, "moderate", "3× monthly essentials (~4,500 CHF/mo on updated figures)"),
      },
    },
    subNational: {
      name: { en: "Canton of Zurich", id: "Kanton Zürich" },
      effectiveRate: {
        low: m(0.04, "high", "Kanton Zurich Steueramt 2026: cantonal+communal ~4% at low"),
        mid: m(0.08, "high", "Kanton Zurich 2026: ~8% at mid band"),
        high: m(
          0.12,
          "high",
          "Kanton Zurich 2026: ~12% at high band; combined federal+cantonal+communal top ~41% (PwC 2026)",
        ),
      },
    },
  },
  {
    id: "warsaw",
    name: { en: "Warsaw", id: "Warsawa" },
    countryId: "pl",
    currency: "PLN",
    region: "europe",
    expenses: {
      housing: m(4630, "high", "Numbeo Jul 2026: 1BR city centre 4,632.14 PLN/mo"),
      food: m(1350, "moderate", "Numbeo Jul 2026: meal-for-two mid-range 235 PLN + groceries; combined ~1,350 PLN/mo"),
      transport: m(110, "high", "Numbeo Jul 2026: ZTM Warsaw monthly pass 110 PLN/mo"),
      utilities: m(
        1310,
        "high",
        "Numbeo Jul 2026: elec+gas+water 85m² 1,311.10 PLN/mo (elevated by 2026 European gas-heating prices)",
      ),
      healthcare: m(220, "moderate", "OOP: private clinic queue-avoidance; NFZ covers basics"),
      childcare: m(2270, "moderate", "Numbeo Jul 2026: private zlobek 2,268.75 PLN/mo"),
      lifestyle: m(600, "moderate", "Numbeo Jun 2026: gym+social ~600 PLN/mo"),
    },
    childcareMedianLocal: m(2270, "moderate", "Warsaw private nursery median, Numbeo Jul 2026"),
    schoolMedianLocal: {
      public: m(0, "high", "Polish public school: free; misc ~20 PLN/mo"),
      private: m(2000, "moderate", "International school Warsaw ~1,800-2,200 PLN/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(9260, "moderate", "2× rent deposit on updated rent"),
        keyMoney: m(0, "high", "N/A"),
        moving: m(4000, "moderate", "International shipping estimate PLN"),
        visaAdmin: m(1500, "moderate", "Work permit + residence card fees ~1,500 PLN"),
      },
      liquidityReserve: {
        cashCushion: m(19500, "moderate", "3× monthly essentials (~6,500 PLN/mo on updated figures)"),
      },
    },
  },
  {
    id: "prague",
    name: { en: "Prague", id: "Praha" },
    countryId: "cz",
    currency: "CZK",
    region: "europe",
    expenses: {
      housing: m(25200, "high", "Numbeo Jul 2026: 1BR city centre 25,185.72 CZK/mo"),
      food: m(
        7300,
        "moderate",
        "Numbeo Jul 2026: meal-for-two mid-range 1,100 CZK + groceries; combined ~7,300 CZK/mo",
      ),
      transport: m(541, "high", "Numbeo Jul 2026: DPP Prague monthly pass 540.96 CZK/mo"),
      utilities: m(6600, "high", "Numbeo Jul 2026: elec+gas+water 85m² 6,593.71 CZK/mo"),
      healthcare: m(550, "moderate", "OOP: private dental + some specialists; VZP covers GP"),
      childcare: m(
        15000,
        "moderate",
        "Numbeo Jul 2026 raw mean 23,183 CZK skewed by international-skolka entries (range 13,400-35,000); using lower-mid of stated range for typical private skolka",
      ),
      lifestyle: m(4200, "moderate", "Numbeo Jun 2026: gym+social ~4,200 CZK/mo"),
    },
    childcareMedianLocal: m(15000, "moderate", "Prague private nursery median (adjusted for outlier skew)"),
    schoolMedianLocal: {
      public: m(0, "high", "Czech public school: free; misc ~100 CZK/mo"),
      private: m(15000, "moderate", "International school Prague ~13K-17K CZK/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(50400, "moderate", "2× rent deposit on updated rent"),
        keyMoney: m(0, "high", "N/A"),
        moving: m(18000, "moderate", "International shipping estimate CZK"),
        visaAdmin: m(5000, "moderate", "Employee card fees ~5,000 CZK"),
      },
      liquidityReserve: {
        cashCushion: m(110000, "moderate", "3× monthly essentials (~37K CZK/mo on updated figures)"),
      },
    },
  },
  {
    id: "paris",
    name: { en: "Paris", id: "Paris" },
    countryId: "fr",
    currency: "EUR",
    region: "europe",
    expenses: {
      housing: m(1415, "high", "Numbeo Jul 2026: 1BR inside Périphérique 1,414.37 EUR/mo"),
      food: m(400, "moderate", "Numbeo Jul 2026: meal-for-two mid-range 70 EUR + groceries; combined ~400 EUR/mo"),
      transport: m(88, "high", "Numbeo Jul 2026: 90 EUR/mo; close to official Navigo all-zones pass ~86.40 EUR"),
      utilities: m(229, "high", "Numbeo Jul 2026: elec+gas+water 85m² 228.76 EUR/mo"),
      healthcare: m(30, "high", "OOP: ticket modérateur residual after Secu 70% + mutuelles"),
      childcare: m(
        650,
        "moderate",
        "Numbeo Jul 2026 gross private fee 1,493.79 EUR/mo; municipal creche + CAF-subsidized complementaire is far lower, ~500-700 EUR/mo net for most incomes",
      ),
      lifestyle: m(310, "moderate", "Numbeo Jun 2026: cafe+gym+clothing ~310 EUR/mo"),
    },
    childcareMedianLocal: m(650, "moderate", "Paris creche net median after CAF subsidy"),
    schoolMedianLocal: {
      public: m(0, "high", "Education nationale: free; misc ~20 EUR/mo"),
      private: m(1200, "moderate", "Private/international school Paris ~1,000-1,400 EUR/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(2830, "moderate", "2× rent deposit typical on updated rent; max 2 months by law"),
        keyMoney: m(0, "high", "N/A: droit au bail only in commercial; residential illegal"),
        moving: m(1500, "moderate", "International shipping + demenageurs estimate"),
        visaAdmin: m(400, "moderate", "Passeport Talent / EU citizenship admin fees ~400 EUR"),
      },
      liquidityReserve: {
        cashCushion: m(7700, "moderate", "3× monthly essentials (~2,550 EUR/mo on updated figures)"),
      },
    },
  },
  // ══════════════════════════════════════════
  // Nordics
  // ══════════════════════════════════════════
  {
    id: "stockholm",
    name: { en: "Stockholm", id: "Stockholm" },
    countryId: "se",
    currency: "SEK",
    region: "nordics",
    expenses: {
      housing: m(
        17000,
        "high",
        "Numbeo Jul 2026 (updated 28 Jul): 1BR city centre avg 16,994 SEK/mo (range 15,000-20,000)",
      ),
      food: m(
        4000,
        "high",
        "Numbeo Jul 2026: mid-range meal for 2 ~1,000 SEK + groceries ~2,700-3,000 SEK/mo blended est.",
      ),
      transport: m(1060, "high", "Numbeo Jul 2026: SL monthly travel card zones A-B ~1,060 SEK/mo (updated from 950)"),
      utilities: m(
        3100,
        "high",
        "Numbeo Jul 2026: elec+heat+water+garbage 2,705 SEK + broadband 407 SEK ≈ 3,100 SEK/mo for 85m² apt (notable increase from prior 1,500 est.)",
      ),
      healthcare: m(250, "high", "OOP: högkostnadsskydd max ~1,300 SEK/yr (2026) ≈ 110 SEK/mo + dental avg"),
      childcare: m(
        1750,
        "high",
        "Maxtaxa 2026: statutory max 1st child ~1,750 SEK/mo (Skolverket); Numbeo Jul 2026 crowd avg 1,636 SEK/mo corroborates",
      ),
      lifestyle: m(2500, "moderate", "Numbeo Jul 2026: gym 477 SEK/mo + fika/entertainment/clothing ≈ 2,500 SEK/mo"),
    },
    childcareMedianLocal: m(1750, "high", "Stockholm maxtaxa preschool max fee 2026"),
    schoolMedianLocal: {
      public: m(0, "high", "Swedish public school: free; misc ~50 SEK/mo"),
      private: m(4000, "moderate", "Friskola (private school) Stockholm ~3,500-4,500 SEK/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(34000, "moderate", "2× rent deposit at refreshed 17,000 SEK/mo"),
        keyMoney: m(0, "high", "N/A: black market queues exist but not licit costs"),
        moving: m(12000, "moderate", "International shipping estimate SEK"),
        visaAdmin: m(3500, "moderate", "Work permit (Migrationsverket) ~3,500 SEK"),
      },
      liquidityReserve: {
        cashCushion: m(70000, "moderate", "3× monthly essentials (~23,400 SEK/mo at refreshed figures)"),
      },
    },
  },
  {
    id: "copenhagen",
    name: { en: "Copenhagen", id: "Kopenhagen" },
    countryId: "dk",
    currency: "DKK",
    region: "nordics",
    expenses: {
      housing: m(12700, "high", "Numbeo Jul 2026 (updated 29 Jul): 1BR city centre avg 12,679 DKK/mo"),
      food: m(
        4300,
        "high",
        "Numbeo Jul 2026: mid-range meal for 2 ~800 DKK + groceries ~2,500-3,000 DKK/mo blended est.",
      ),
      transport: m(750, "high", "Numbeo Jul 2026: Rejsekort monthly equiv. zones 1-2 ~750 DKK (updated from 500)"),
      utilities: m(
        1450,
        "high",
        "Numbeo Jul 2026: elec+heat+water 1,182 DKK + broadband 262 DKK ≈ 1,450 DKK/mo for 85m² apt",
      ),
      healthcare: m(200, "high", "OOP: dental + private physio; GP/hospital free under sygesikring"),
      childcare: m(
        6200,
        "moderate",
        "Numbeo Jul 2026 crowd avg dagtilbud 6,214 DKK/mo; official dagtilbud max-rate 2026 est. lower — kept moderate pending Kbh kommune confirmation",
      ),
      lifestyle: m(3000, "moderate", "Numbeo Jul 2026: gym 410 DKK/mo + hygge/social/clothing ≈ 3,000 DKK/mo"),
    },
    childcareMedianLocal: m(6200, "moderate", "Copenhagen dagpasning Numbeo Jul 2026 crowd median"),
    schoolMedianLocal: {
      public: m(0, "high", "Danish folkeskole: free; misc ~30 DKK/mo"),
      private: m(5000, "moderate", "International school Copenhagen ~4,500-5,500 DKK/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(25400, "moderate", "2× rent deposit at refreshed 12,700 DKK/mo"),
        keyMoney: m(0, "high", "N/A"),
        moving: m(10000, "moderate", "International shipping estimate DKK"),
        visaAdmin: m(4000, "moderate", "Work permit (Styrelsen) ~4,000 DKK"),
      },
      liquidityReserve: {
        cashCushion: m(63000, "moderate", "3× monthly essentials (~21,000 DKK/mo at refreshed figures)"),
      },
    },
  },
  {
    id: "oslo",
    name: { en: "Oslo", id: "Oslo" },
    countryId: "no",
    currency: "NOK",
    region: "nordics",
    expenses: {
      housing: m(18900, "high", "Numbeo Jul 2026 (updated 22 Jul): 1BR city centre avg 18,923 NOK/mo"),
      food: m(
        6500,
        "high",
        "Numbeo Jul 2026: mid-range meal for 2 ~1,200 NOK + groceries (milk/eggs/chicken/produce items) blended est.",
      ),
      transport: m(790, "high", "Numbeo Jul 2026: Ruter 30-day Oslo pass ~790 NOK/mo"),
      utilities: m(
        4270,
        "high",
        "Numbeo Jul 2026: elec+heat+water 3,760 NOK + broadband 513 NOK ≈ 4,270 NOK/mo for 85m² apt (notable increase from prior 2,000 est.)",
      ),
      healthcare: m(300, "high", "OOP: egenandel max ~3,000 NOK/yr ≈ 250/mo; GP free after cap"),
      childcare: m(
        3500,
        "high",
        "Makspris 2026: barnehage max fee ~3,500 NOK/mo per child (statutory); Numbeo Jul 2026 crowd est. 2,488 NOK/mo lower, kept high on official source",
      ),
      lifestyle: m(4000, "moderate", "Numbeo Jul 2026: gym 548 NOK/mo + tur/aktivitet/social ≈ 4,000 NOK/mo"),
    },
    childcareMedianLocal: m(3500, "high", "Oslo barnehage makspris 2026 (official)"),
    schoolMedianLocal: {
      public: m(0, "high", "Norwegian grunnskole: free; misc ~50 NOK/mo"),
      private: m(8000, "moderate", "International school Oslo ~7,000-9,000 NOK/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(37800, "moderate", "2× rent deposit at refreshed 18,900 NOK/mo"),
        keyMoney: m(0, "high", "N/A"),
        moving: m(14000, "moderate", "International shipping estimate NOK"),
        visaAdmin: m(4500, "moderate", "Skilled worker permit (UDI) ~4,500 NOK"),
      },
      liquidityReserve: {
        cashCushion: m(85000, "moderate", "3× monthly essentials (~28,000 NOK/mo at refreshed figures)"),
      },
    },
  },
  {
    id: "helsinki",
    name: { en: "Helsinki", id: "Helsinki" },
    countryId: "fi",
    currency: "EUR",
    region: "nordics",
    expenses: {
      housing: m(1090, "high", "Numbeo Jul 2026 (updated 24 Jul): 1BR city centre avg 1,090 EUR/mo"),
      food: m(420, "high", "Numbeo Jul 2026: mid-range meal for 2 ~100 EUR + groceries blended est. ~420 EUR/mo"),
      transport: m(72, "high", "Numbeo Jul 2026: HSL zone AB monthly ~72 EUR/mo (updated from 62)"),
      utilities: m(135, "high", "Numbeo Jul 2026: elec+heat+water 113 EUR + broadband 22 EUR ≈ 135 EUR/mo"),
      healthcare: m(50, "high", "OOP: terveyskeskusmaksu ~14 EUR/visit; Kela refunds some"),
      childcare: m(
        422,
        "high",
        "Numbeo Jul 2026 crowd figure 422 EUR/mo; consistent with päivähoito income-based max ~300-460 EUR/mo band",
      ),
      lifestyle: m(250, "moderate", "Numbeo Jul 2026: gym 43 EUR/mo + sauna/social/clothing ≈ 250 EUR/mo"),
    },
    childcareMedianLocal: m(422, "high", "Helsinki päivähoito Numbeo Jul 2026 median; income-based cap"),
    schoolMedianLocal: {
      public: m(0, "high", "Finnish peruskoulu: free; misc ~20 EUR/mo"),
      private: m(1000, "moderate", "International school Helsinki ~800-1,200 EUR/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(2180, "moderate", "2× rent deposit at refreshed 1,090 EUR/mo"),
        keyMoney: m(0, "high", "N/A"),
        moving: m(1500, "moderate", "International shipping estimate EUR"),
        visaAdmin: m(500, "moderate", "Residence permit (Migri) ~500 EUR"),
      },
      liquidityReserve: {
        cashCushion: m(5800, "moderate", "3× monthly essentials (~1,950 EUR/mo at refreshed figures)"),
      },
    },
  },
  {
    id: "san-francisco",
    name: { en: "San Francisco", id: "San Francisco" },
    countryId: "us",
    currency: "USD",
    region: "americas",
    expenses: {
      housing: m(3800, "high", "Numbeo Jul 2026 (updated 30 Jul): 1BR city centre avg 3,798 USD/mo"),
      food: m(750, "high", "Numbeo Jul 2026: mid-range meal for 2 ~120 USD + groceries blended est. ~750 USD/mo"),
      transport: m(90, "high", "Numbeo Jul 2026: SFMTA/BART monthly pass ~90 USD/mo (updated from 120)"),
      utilities: m(245, "high", "Numbeo Jul 2026: elec+gas+water 246 USD/mo for 85m² apt (broadband separate ~71 USD)"),
      healthcare: m(450, "moderate", "OOP: employee premium share ~200 + avg copay+deductible ~250 USD/mo"),
      childcare: m(2970, "high", "Numbeo Jul 2026: private daycare SF ~2,966 USD/mo (updated from 2,800)"),
      lifestyle: m(510, "moderate", "Numbeo Jul 2026: gym 136 USD/mo + dining/clothing ≈ 510 USD/mo"),
    },
    childcareMedianLocal: m(2970, "high", "SF private daycare Numbeo Jul 2026 median"),
    schoolMedianLocal: {
      public: m(0, "high", "SFUSD public school: free; misc ~30 USD/mo"),
      private: m(3000, "moderate", "Private school SF ~2,500-3,500 USD/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(7600, "moderate", "2× rent deposit at refreshed 3,800 USD/mo; SF max 2 months"),
        keyMoney: m(0, "high", "N/A: not customary in US rentals"),
        moving: m(4000, "moderate", "International shipping + domestic moving estimate"),
        visaAdmin: m(3000, "moderate", "H-1B filing fees + attorney estimate ~3,000 USD"),
      },
      liquidityReserve: {
        cashCushion: m(19000, "moderate", "3× monthly essentials (~6,300 USD/mo at refreshed figures)"),
      },
    },
    subNational: {
      name: { en: "California", id: "California" },
      effectiveRate: {
        low: m(0.01, "high", "FTB 2025-26: CA state income tax effective ~1% at low band"),
        mid: m(0.04, "high", "FTB 2025-26: ~4% at mid band"),
        high: m(0.08, "high", "FTB 2025-26: ~8% at high band (up to 13.3% marginal)"),
      },
    },
  },
  {
    id: "new-york",
    name: { en: "New York", id: "New York" },
    countryId: "us",
    currency: "USD",
    region: "americas",
    expenses: {
      housing: m(4300, "high", "Numbeo Jul 2026 (updated 29 Jul): 1BR city centre (Manhattan) avg 4,295 USD/mo"),
      food: m(750, "high", "Numbeo Jul 2026: mid-range meal for 2 ~140 USD + groceries blended est. ~750 USD/mo"),
      transport: m(140, "high", "Numbeo Jul 2026: MTA monthly unlimited MetroCard ~140 USD/mo (updated from 133)"),
      utilities: m(250, "high", "Numbeo Jul 2026: elec+gas+water 252 USD/mo for 85m² apt (broadband separate ~78 USD)"),
      healthcare: m(450, "moderate", "OOP: employee premium share + copays ~450 USD/mo"),
      childcare: m(3370, "high", "Numbeo Jul 2026: NYC private daycare ~3,366 USD/mo (updated from 3,000)"),
      lifestyle: m(500, "moderate", "Numbeo Jul 2026: gym 115 USD/mo + dining/clothing ≈ 500 USD/mo"),
    },
    childcareMedianLocal: m(3370, "high", "NYC private daycare Numbeo Jul 2026 median"),
    schoolMedianLocal: {
      public: m(0, "high", "NYC public school: free; misc ~30 USD/mo"),
      private: m(3500, "moderate", "Independent school NYC ~3,000-4,000 USD/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(8600, "moderate", "2× rent deposit at refreshed 4,300 USD/mo; NY max 1 month but common 2"),
        keyMoney: m(0, "high", "N/A"),
        moving: m(4000, "moderate", "International shipping + moving estimate"),
        visaAdmin: m(3000, "moderate", "H-1B filing + legal fees estimate ~3,000 USD"),
      },
      liquidityReserve: {
        cashCushion: m(21000, "moderate", "3× monthly essentials (~7,000 USD/mo at refreshed figures)"),
      },
    },
    subNational: {
      name: { en: "New York State + City", id: "New York State + City" },
      effectiveRate: {
        low: m(0.04, "high", "NYSDTF 2025-26: NY state ~4% + NYC city ~3.8% effective at low"),
        mid: m(0.08, "high", "NYSDTF 2025-26: ~8% combined at mid band"),
        high: m(0.12, "high", "NYSDTF 2025-26: ~12% combined at high band"),
      },
    },
  },
  {
    id: "austin",
    name: { en: "Austin", id: "Austin" },
    countryId: "us",
    currency: "USD",
    region: "americas",
    expenses: {
      housing: m(1900, "high", "Numbeo Jul 2026 (updated 29 Jul): 1BR city centre avg 1,894 USD/mo"),
      food: m(490, "high", "Numbeo Jul 2026: mid-range meal for 2 ~85 USD + groceries blended est. ~490 USD/mo"),
      transport: m(41, "high", "Numbeo Jul 2026: CapMetro monthly pass ~41 USD/mo (updated from 50)"),
      utilities: m(
        223,
        "high",
        "Numbeo Jul 2026: elec (ERCOT)+gas+water 223 USD/mo for 85m² apt (broadband separate ~71 USD)",
      ),
      healthcare: m(400, "moderate", "OOP: employee premium share + copays ~400 USD/mo"),
      childcare: m(1510, "high", "Numbeo Jul 2026: Austin daycare ~1,506 USD/mo (updated from 1,800)"),
      lifestyle: m(340, "moderate", "Numbeo Jul 2026: gym 58 USD/mo + BBQ/outdoor/clothing ≈ 340 USD/mo"),
    },
    childcareMedianLocal: m(1510, "high", "Austin private daycare Numbeo Jul 2026 median"),
    schoolMedianLocal: {
      public: m(0, "high", "AISD public school: free; misc ~25 USD/mo"),
      private: m(1500, "moderate", "Private school Austin ~1,200-1,800 USD/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(3800, "moderate", "2× rent deposit at refreshed 1,900 USD/mo"),
        keyMoney: m(0, "high", "N/A"),
        moving: m(3500, "moderate", "International shipping + domestic moving estimate"),
        visaAdmin: m(3000, "moderate", "H-1B or TN visa fees + legal ~3,000 USD"),
      },
      liquidityReserve: {
        cashCushion: m(11500, "moderate", "3× monthly essentials (~3,800 USD/mo at refreshed figures)"),
      },
    },
    subNational: {
      name: { en: "Texas", id: "Texas" },
      effectiveRate: {
        low: m(0.0, "high", "Texas: no state income tax"),
        mid: m(0.0, "high", "Texas: no state income tax"),
        high: m(0.0, "high", "Texas: no state income tax"),
      },
    },
  },
  {
    id: "toronto",
    name: { en: "Toronto", id: "Toronto" },
    countryId: "ca",
    currency: "CAD",
    region: "americas",
    expenses: {
      housing: m(2270, "high", "Numbeo Jul 2026 (updated 30 Jul): 1BR city centre avg 2,273 CAD/mo"),
      food: m(700, "high", "Numbeo Jul 2026: mid-range meal for 2 ~120 CAD + groceries ~600 CAD/mo blended est."),
      transport: m(156, "high", "Numbeo Jul 2026: TTC monthly pass ~156 CAD/mo"),
      utilities: m(
        194,
        "high",
        "Numbeo Jul 2026: Hydro One+water 194 CAD/mo for 85m² apt (broadband separate ~69 CAD)",
      ),
      healthcare: m(100, "high", "OOP: OHIP covers GP/hospital; dental+vision ~100 CAD/mo"),
      childcare: m(
        1060,
        "high",
        "Numbeo Jul 2026 crowd est. 1,059 CAD/mo; consistent with $10/day federal CWELCC program ~1,000 CAD/mo per child",
      ),
      lifestyle: m(400, "moderate", "Numbeo Jul 2026: gym 62 CAD/mo + patio/social/clothing ≈ 400 CAD/mo"),
    },
    childcareMedianLocal: m(1060, "high", "Ontario CWELCC/Numbeo Jul 2026 median"),
    schoolMedianLocal: {
      public: m(0, "high", "TDSB public school: free; misc ~20 CAD/mo"),
      private: m(2500, "moderate", "Private school Toronto ~2,000-3,000 CAD/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(4540, "moderate", "2× rent deposit at refreshed 2,270 CAD/mo"),
        keyMoney: m(0, "high", "N/A"),
        moving: m(2500, "moderate", "International shipping + moving estimate CAD"),
        visaAdmin: m(2000, "moderate", "LMIA-exempt permit or PR application fees ~2,000 CAD"),
      },
      liquidityReserve: {
        cashCushion: m(12500, "moderate", "3× monthly essentials (~4,150 CAD/mo at refreshed figures)"),
      },
    },
    subNational: {
      name: { en: "Ontario", id: "Ontario" },
      effectiveRate: {
        low: m(0.05, "high", "CRA/Ontario 2025-26: Ontario provincial income tax effective ~5% at low"),
        mid: m(0.09, "high", "CRA/Ontario 2025-26: ~9% at mid band"),
        high: m(0.13, "high", "CRA/Ontario 2025-26: ~13% at high band"),
      },
    },
  },
  {
    id: "sao-paulo",
    name: { en: "São Paulo", id: "São Paulo" },
    countryId: "br",
    currency: "BRL",
    region: "americas",
    expenses: {
      housing: m(3540, "high", "Numbeo Jul 2026 (updated 27 Jul): 1BR city centre avg 3,537 BRL/mo"),
      food: m(1500, "high", "Numbeo Jul 2026: mid-range meal for 2 ~250 BRL + groceries blended est. ~1,500 BRL/mo"),
      transport: m(243, "high", "Numbeo Jul 2026: SPTrans/Metrô monthly pass ~243 BRL/mo (updated from 250)"),
      utilities: m(505, "high", "Numbeo Jul 2026: elec+water 505 BRL/mo for 85m² apt (broadband separate ~109 BRL)"),
      healthcare: m(800, "moderate", "OOP: plano de saúde copay + dental; SUS public but queued"),
      childcare: m(2640, "high", "Numbeo Jul 2026: private escola infantil SP ~2,636 BRL/mo (updated from 2,000)"),
      lifestyle: m(1050, "moderate", "Numbeo Jul 2026: gym 188 BRL/mo + restaurante/social/clothing ≈ 1,050 BRL/mo"),
    },
    childcareMedianLocal: m(2640, "high", "São Paulo private preschool Numbeo Jul 2026 median"),
    schoolMedianLocal: {
      public: m(0, "high", "Brazilian public school: free; misc ~30 BRL/mo"),
      private: m(3000, "moderate", "Private escola São Paulo ~2,500-3,500 BRL/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(7100, "moderate", "2× rent deposit at refreshed 3,540 BRL/mo"),
        keyMoney: m(0, "high", "N/A"),
        moving: m(8000, "moderate", "International shipping estimate BRL"),
        visaAdmin: m(3000, "moderate", "VITEM II work visa + registration fees ~3,000 BRL"),
      },
      liquidityReserve: {
        cashCushion: m(19500, "moderate", "3× monthly essentials (~6,500 BRL/mo at refreshed figures)"),
      },
    },
  },
  {
    id: "mexico-city",
    name: { en: "Mexico City", id: "Kota Meksiko" },
    countryId: "mx",
    currency: "MXN",
    region: "americas",
    expenses: {
      housing: m(
        19500,
        "high",
        "Numbeo Jul 2026 (updated 28 Jul): 1BR city centre avg 19,516 MXN/mo (notable increase from prior 15,000 est.)",
      ),
      food: m(5000, "high", "Numbeo Jul 2026: mid-range meal for 2 ~900 MXN + groceries blended est. ~5,000 MXN/mo"),
      transport: m(500, "high", "Numbeo Jul 2026: Metro CDMX monthly estimate ~500 MXN/mo"),
      utilities: m(1720, "high", "Numbeo Jul 2026: elec+water 1,122 MXN + broadband 596 MXN ≈ 1,720 MXN/mo"),
      healthcare: m(2000, "moderate", "OOP: private clinic + meds; IMSS covers formal employed"),
      childcare: m(7830, "high", "Numbeo Jul 2026: private guardería CDMX ~7,833 MXN/mo"),
      lifestyle: m(3400, "moderate", "Numbeo Jul 2026: gym 971 MXN/mo + tacos/social/clothing ≈ 3,400 MXN/mo"),
    },
    childcareMedianLocal: m(7830, "high", "CDMX private preschool Numbeo Jul 2026 median"),
    schoolMedianLocal: {
      public: m(0, "high", "Mexican public school: free; misc ~100 MXN/mo"),
      private: m(12000, "moderate", "Private school CDMX ~10K-14K MXN/mo"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(39000, "moderate", "2× rent deposit at refreshed 19,500 MXN/mo"),
        keyMoney: m(0, "high", "N/A"),
        moving: m(15000, "moderate", "International shipping estimate MXN"),
        visaAdmin: m(5000, "moderate", "FM3 work permit fees ~5,000 MXN"),
      },
      liquidityReserve: {
        cashCushion: m(90000, "moderate", "3× monthly essentials (~30,000 MXN/mo at refreshed figures)"),
      },
    },
  },
  // ══════════════════════════════════════════
  // Others (MENA, South Asia, East Asia, Oceania, Africa)
  // ══════════════════════════════════════════
  {
    id: "dubai",
    name: { en: "Dubai", id: "Dubai" },
    countryId: "ae",
    currency: "AED",
    region: "mena",
    expenses: {
      housing: m(8400, "high", "Numbeo Jul 2026: 1BR city centre avg AED 8,409 (range 6,000–14,000)"),
      food: m(
        1500,
        "moderate",
        "Numbeo Jul 2026 basket (inexpensive meal Dh45, groceries ~800–1,200) + dining-out uplift; carried close to prior",
      ),
      transport: m(250, "high", "Numbeo Jul 2026: monthly public transport pass AED 250 (range 200–400)"),
      utilities: m(870, "high", "Numbeo Jul 2026: basic utilities 85m² apartment AED 870.63 (range 541–1,500)"),
      healthcare: m(
        600,
        "moderate",
        "OOP: copay/deductible on mandatory employer health plan; DHA; not independently re-verified this cycle",
      ),
      childcare: m(
        3000,
        "moderate",
        "Private nursery Dubai ~2,500–3,500 AED/mo; not independently re-verified this cycle",
      ),
      lifestyle: m(1500, "moderate", "Gym+brunch+social estimate; not independently re-verified this cycle"),
    },
    childcareMedianLocal: m(3000, "moderate", "Dubai private nursery median; carried forward"),
    schoolMedianLocal: {
      public: m(1000, "proxy", "KHDA public school: mainly Emirati nationals; expat proxy fee ~1,000 AED/mo"),
      private: m(3500, "high", "KHDA: private school Dubai ~3,000–4,000 AED/mo; carried forward"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(
          16800,
          "moderate",
          "2× month rent deposit; Dubai standard (recomputed off refreshed AED 8,400 rent)",
        ),
        keyMoney: m(0, "high", "N/A: no key money custom in UAE"),
        moving: m(6000, "moderate", "International shipping estimate AED; carried forward"),
        visaAdmin: m(2500, "moderate", "Employment visa + Emirates ID + medical ~2,500 AED; carried forward"),
      },
      liquidityReserve: {
        cashCushion: m(33000, "moderate", "3× monthly essentials (housing+food+transport+utilities ≈ AED 11,020/mo)"),
      },
    },
  },
  {
    id: "bengaluru",
    name: { en: "Bengaluru", id: "Bangalore" },
    countryId: "in",
    currency: "INR",
    region: "asia",
    expenses: {
      housing: m(30600, "high", "Numbeo Jul 2026: 1BR city centre INR 30,625 (outside centre 17,685)"),
      food: m(
        10000,
        "moderate",
        "Numbeo Jul 2026 minimal basket (restaurants ₹900–1,200 + groceries ₹3,500–4,500) scaled for fuller professional dining pattern; down from prior 12,000",
      ),
      transport: m(1500, "high", "Numbeo Jul 2026 monthly pass ₹1,350 + local auto-rickshaw supplement ~1,500 INR/mo"),
      utilities: m(2800, "high", "Numbeo Jul 2026: basic utilities 85m² apartment ₹2,640"),
      healthcare: m(
        3000,
        "moderate",
        "OOP: private Apollo/Fortis clinic; ESI not applicable at tech salaries; not independently re-verified this cycle",
      ),
      childcare: m(20000, "moderate", "Private play school Bengaluru ~15K–25K INR/mo; carried forward"),
      lifestyle: m(7000, "moderate", "Gym+dining+social estimate; carried forward"),
    },
    childcareMedianLocal: m(20000, "moderate", "Bengaluru private preschool median; carried forward"),
    schoolMedianLocal: {
      public: m(500, "moderate", "Govt school misc fees ~500 INR/mo; carried forward"),
      private: m(15000, "moderate", "CBSE/ICSE private school Bengaluru ~12K–18K INR/mo; carried forward"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(92000, "moderate", "3× rent deposit typical in Bengaluru (recomputed off refreshed ₹30,600 rent)"),
        keyMoney: m(0, "high", "N/A"),
        moving: m(40000, "moderate", "International shipping estimate INR; carried forward"),
        visaAdmin: m(15000, "moderate", "Employment visa fees + FRO registration ~15K INR; carried forward"),
      },
      liquidityReserve: {
        cashCushion: m(135000, "moderate", "3× monthly essentials (housing+food+transport+utilities ≈ ₹44,900/mo)"),
      },
    },
  },
  {
    id: "seoul",
    name: { en: "Seoul", id: "Seoul" },
    countryId: "kr",
    currency: "KRW",
    region: "asia",
    expenses: {
      housing: m(1190000, "high", "Numbeo Jul 2026: 1BR city centre (wolse-equivalent) KRW 1,187,500"),
      food: m(
        500000,
        "moderate",
        "Restaurant + E-Mart groceries ~500K KRW/mo; Numbeo Jul 2026 grocery line item read as an outlier (₩800K–1M) and excluded pending re-verification",
      ),
      transport: m(65000, "high", "Numbeo Jul 2026: T-money monthly Seoul metro/bus pass KRW 63,500"),
      utilities: m(250000, "high", "Numbeo Jul 2026: basic utilities 85m² apartment KRW 252,159"),
      healthcare: m(100000, "moderate", "OOP copay: 30% patient share; NHI premiums in effectiveRate; carried forward"),
      childcare: m(500000, "moderate", "Private English preschool Seoul ~400K–600K KRW/mo; carried forward"),
      lifestyle: m(400000, "moderate", "Gym+social estimate; carried forward"),
    },
    childcareMedianLocal: m(500000, "moderate", "Seoul private preschool (yeong-eo) median; carried forward"),
    schoolMedianLocal: {
      public: m(50000, "moderate", "Korean public school misc fees ~50K KRW/mo; carried forward"),
      private: m(1000000, "moderate", "Private hagwon + international school Seoul ~1M KRW/mo; carried forward"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(
          2380000,
          "moderate",
          "2× rent deposit; or partial jeonse lump-sum substitute (recomputed off refreshed KRW 1,190,000 rent)",
        ),
        keyMoney: m(0, "high", "N/A: jeonse is lump-sum deposit returned, not key money"),
        moving: m(1500000, "moderate", "International shipping estimate KRW; carried forward"),
        visaAdmin: m(500000, "moderate", "D-8 or E-7 visa fees + alien registration ~500K KRW; carried forward"),
      },
      liquidityReserve: {
        cashCushion: m(
          6000000,
          "moderate",
          "3× monthly essentials (housing+food+transport+utilities ≈ KRW 2,005,000/mo); down from prior 8,000,000 reflecting lower Jul 2026 rent",
        ),
      },
    },
  },
  {
    id: "sydney",
    name: { en: "Sydney", id: "Sydney" },
    countryId: "au",
    currency: "AUD",
    region: "oceania",
    expenses: {
      housing: m(3536, "high", "Numbeo, last update 23 Jul 2026: 1BR city centre AUD 3,535.75"),
      food: m(
        700,
        "moderate",
        "Restaurant (inexpensive AUD 25/meal, mid-range ~AUD 68/person) + groceries estimate; carried close to prior",
      ),
      transport: m(217, "high", "Numbeo Jul 2026: monthly public transport pass AUD 217.39"),
      utilities: m(315, "high", "Numbeo Jul 2026: basic utilities small apartment AUD 315.40"),
      healthcare: m(100, "high", "OOP: dental + physio gap; Medicare covers GP bulk-billing; carried forward"),
      childcare: m(1800, "high", "Sydney daycare ~1,600–2,000 AUD/mo after CCS subsidy; carried forward"),
      lifestyle: m(400, "moderate", "Gym+café+outdoor estimate; carried forward"),
    },
    childcareMedianLocal: m(1800, "high", "Sydney daycare median after CCS; carried forward"),
    schoolMedianLocal: {
      public: m(200, "high", "NSW public school voluntary contribution ~200 AUD/mo; carried forward"),
      private: m(2000, "moderate", "Independent school Sydney ~1,700–2,300 AUD/mo; carried forward"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(
          7100,
          "moderate",
          "≈2× rent (NSW bond capped at 4 weeks + 1 month advance rent common practice); recomputed off refreshed AUD 3,536 rent",
        ),
        keyMoney: m(0, "high", "N/A"),
        moving: m(3000, "moderate", "International shipping estimate AUD; carried forward"),
        visaAdmin: m(2000, "moderate", "TSS 482 or Skilled visa application fees ~2,000 AUD; carried forward"),
      },
      liquidityReserve: {
        cashCushion: m(14300, "moderate", "3× monthly essentials (housing+food+transport+utilities ≈ AUD 4,768/mo)"),
      },
    },
  },
  {
    id: "nairobi",
    name: { en: "Nairobi", id: "Nairobi" },
    countryId: "ke",
    currency: "KES",
    region: "africa",
    expenses: {
      housing: m(54000, "high", "Numbeo, last update 29 Jul 2026: 1BR city centre KES 54,375 (range 30,000–78,000)"),
      food: m(
        15000,
        "moderate",
        "Numbeo Jul 2026 basket (groceries KSh8,000–12,000 + dining KSh3,000–5,000); down from prior 30,000 estimate",
      ),
      transport: m(6000, "high", "Numbeo Jul 2026: monthly public transport pass KES 6,000 (range 3,000–7,200)"),
      utilities: m(7300, "high", "Numbeo Jul 2026: basic utilities 85m² apartment KES 7,273"),
      healthcare: m(
        10000,
        "moderate",
        "OOP: private hospital; SHIF covers some; private plans common; carried forward",
      ),
      childcare: m(40000, "moderate", "Private preschool Nairobi ~35K–45K KES/mo; carried forward"),
      lifestyle: m(15000, "moderate", "Gym+social+nyama choma estimate; carried forward"),
    },
    childcareMedianLocal: m(40000, "moderate", "Nairobi private preschool median; carried forward"),
    schoolMedianLocal: {
      public: m(2000, "moderate", "Kenyan public school fees ~2,000 KES/mo; carried forward"),
      private: m(60000, "moderate", "International school Nairobi ~50K–70K KES/mo; carried forward"),
    },
    relocation: {
      sunkCosts: {
        deposit: m(
          108000,
          "moderate",
          "2× rent deposit (recomputed off refreshed KES 54,000 rent); down from prior 160,000",
        ),
        keyMoney: m(0, "high", "N/A"),
        moving: m(60000, "moderate", "International shipping estimate KES; carried forward"),
        visaAdmin: m(20000, "moderate", "Work permit + special pass fees ~20K KES; carried forward"),
      },
      liquidityReserve: {
        cashCushion: m(
          247000,
          "moderate",
          "3× monthly essentials (housing+food+transport+utilities ≈ KES 82,300/mo); down from prior 360,000",
        ),
      },
    },
  },
];

// ─── Dataset Export ──────────────────────────────────────────────────────────

export const dataset: Dataset = {
  snapshotDate: "2026-07-30",
  fx,
  countries,
  cities,
};
