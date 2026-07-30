// AUTHORITATIVE FX SNAPSHOT — the single source for every USD conversion in the app.
// Sources: ECB Euro reference rates 2026-07-29, Xe.com mid-market 2026-07-29,
//          various cross-checks (investing.com, exchange-rates.org, tradingeconomics.com) 2026-07-24 to 2026-07-29.
// Each entry is the USD value of 1 unit of that currency.
// A city's USD rate is DERIVED from this table via city.currency — no city stores its own rate.
// fxSnapshotDate may differ from cities/roles snapshotDate (each dataset tracks its own date).

export type FxTable = {
  fxSnapshotDate: string; // ISO date of this FX snapshot
  ratesUsdPerUnit: Record<string, number>; // ISO-4217 -> USD value per 1 unit
};

export const fx: FxTable = {
  fxSnapshotDate: "2026-07-29",
  ratesUsdPerUnit: {
    // Always
    USD: 1.0,

    // ASEAN
    IDR: 0.000055339, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29; ~18,070 IDR/USD [high]
    MYR: 0.24449, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]
    SGD: 0.7744, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]
    THB: 0.029802, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]
    VND: 0.00003797, // Xe.com 2026-07-29; Investing.com 2026-07-29 cross-check; ~26,335 VND/USD [high]
    PHP: 0.016283, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]
    KHR: 0.00024738, // Xe.com 2026-07-29; freecurrencyrates.com 2026-07-29 cross-check; ~4,042 KHR/USD [moderate — thin/dollarized market]
    LAK: 0.000044131, // Xe.com 2026-07-29; exchange-rates.org 2026-07-29 cross-check; ~22,664 LAK/USD [moderate — thin, volatile market]
    MMK: 0.00047692, // Xe.com 2026-07-29 official ~2,097 MMK/USD; tradingeconomics.com 2026-07-24 cross-check [moderate — dual-rate system; parallel/black-market rate materially diverges at ~3,900-4,200 MMK/USD, roughly half the official value]
    BND: 0.7744, // Pegged 1:1 to SGD via Currency Interchangeability Agreement; Xe.com 2026-07-29 [high]

    // Japan
    JPY: 0.0061059, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]

    // Europe (non-Nordic)
    GBP: 1.32844, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]
    EUR: 1.1379, // ECB euro reference rate 2026-07-29; Xe.com 2026-07-29 cross-check [high]
    CHF: 1.21939, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]
    PLN: 0.26308, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]
    CZK: 0.047063, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]

    // Nordics
    SEK: 0.10291, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]
    DKK: 0.15223, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]
    NOK: 0.1035, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]
    ISK: 0.0079824, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]

    // Americas
    CAD: 0.7091, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]
    MXN: 0.057151, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]
    BRL: 0.1951, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]
    ARS: 0.00066842, // Xe.com 2026-07-29 official/mid-market ~1,496 ARS/USD; wanderwallet.io mid-Jul 2026 [moderate — parallel "blue dollar" trades ~2-3% above official, spread narrowed sharply since April 2025 currency-control liberalization]
    CLP: 0.0010707, // Xe.com 2026-07-29; investing.com/foreignexchange.org.uk 2026-07-29 cross-check [high]

    // Middle East
    AED: 0.27229, // Fixed peg 3.6725 AED/USD since 1997; Xe.com 2026-07-29 confirms [high]

    // South & East Asia
    INR: 0.010448, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]
    KRW: 0.0006898, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]
    TWD: 0.03088, // Xe.com 2026-07-29; investing.com/coincodex.com 2026-07-29 cross-check [high]
    CNY: 0.14775, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]

    // Oceania
    AUD: 0.69422, // Xe.com 2026-07-29; ECB EUR-cross 2026-07-29 [high]

    // Africa
    KES: 0.007727, // Xe.com 2026-07-29; exchange-rates.org 2026-07-27 cross-check [high]
    NGN: 0.00073256, // Xe.com 2026-07-29 official window ~1,365 NGN/USD; withinnigeria.com 2026-07-28 cross-check [moderate — parallel/street market trades ~1.5-3% above official (~₦1,400 vs ~₦1,362-1,380), spread narrowed sharply after 2023 FX unification reforms]
    EGP: 0.019731, // Xe.com 2026-07-29; exchange-rates.org 2026-07-29 cross-check [high]
  },
};

// ONLY conversion primitive — every *Usd function in calc.ts routes through this.
// Throws if the currency is not in the fx table, rather than returning NaN.
export function fxToUsd(fxTable: FxTable, currency: string): number {
  const rate = fxTable.ratesUsdPerUnit[currency];
  if (rate === undefined) {
    throw new Error(`Currency "${currency}" not found in fx table (fxSnapshotDate: ${fxTable.fxSnapshotDate})`);
  }
  return rate;
}

// Convenience: reads the rate for a city's own currency from the fx table.
export function cityFxToUsd(fxTable: FxTable, city: { currency: string }): number {
  return fxToUsd(fxTable, city.currency);
}

// Convert a USD amount to a chosen display currency.
// result = usd / fxToUsd(fx, displayCurrency)
export function usdToDisplay(fxTable: FxTable, usd: number, displayCurrency: string): number {
  const displayRate = fxToUsd(fxTable, displayCurrency);
  return usd / displayRate;
}
