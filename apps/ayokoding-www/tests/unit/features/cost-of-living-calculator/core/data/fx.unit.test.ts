import { describe, it, expect } from "vitest";
import {
  fx,
  fxToUsd,
  cityFxToUsd,
  usdToDisplay,
} from "../../../../../../src/features/cost-of-living-calculator/core/data/fx";

// All currencies referenced by any city/country/role in the dataset, plus every supported
// display-currency selector. This list is the expected superset — if a currency is added to
// cities.ts or roles.ts it must also appear here, and the test ensures fx.ts stays in sync.
const REQUIRED_CURRENCIES = [
  // Always
  "USD",
  // ASEAN
  "IDR",
  "MYR",
  "SGD",
  "THB",
  "VND",
  "PHP",
  "KHR",
  "LAK",
  "MMK",
  "BND",
  // Japan
  "JPY",
  // Europe (non-Nordic)
  "GBP",
  "EUR",
  "CHF",
  "PLN",
  "CZK",
  // Nordics
  "SEK",
  "DKK",
  "NOK",
  "ISK",
  // Americas
  "CAD",
  "MXN",
  "BRL",
  "ARS",
  "CLP",
  // Middle East / South & East Asia / Oceania / Africa
  "AED",
  "INR",
  "KRW",
  "TWD",
  "CNY",
  "AUD",
  "KES",
  "NGN",
  "EGP",
];

describe("FxTable — single-source invariants", () => {
  it("has a fxSnapshotDate that is a non-empty ISO date string", () => {
    expect(fx.fxSnapshotDate).toMatch(/^\d{4}-\d{2}-\d{2}$/);
  });

  it("has ratesUsdPerUnit as a plain object", () => {
    expect(typeof fx.ratesUsdPerUnit).toBe("object");
    expect(fx.ratesUsdPerUnit).not.toBeNull();
  });

  it("maps USD to exactly 1", () => {
    expect(fx.ratesUsdPerUnit["USD"]).toBe(1);
  });

  it.each(REQUIRED_CURRENCIES)("has a positive rate for required currency %s", (currency) => {
    const rate = fx.ratesUsdPerUnit[currency];
    expect(rate, `Missing or zero rate for ${currency}`).toBeDefined();
    expect(typeof rate).toBe("number");
    expect(rate).toBeGreaterThan(0);
  });

  it("has no negative rates for any currency in the table", () => {
    for (const [code, rate] of Object.entries(fx.ratesUsdPerUnit)) {
      expect(rate, `Negative rate for ${code}`).toBeGreaterThan(0);
    }
  });
});

describe("fxToUsd helper", () => {
  it("returns the rate for a known currency", () => {
    expect(fxToUsd(fx, "USD")).toBe(1);
    expect(fxToUsd(fx, "EUR")).toBeGreaterThan(1);
  });

  it("throws (or returns a sentinel) for a missing currency rather than NaN", () => {
    expect(() => fxToUsd(fx, "XYZ_UNKNOWN")).toThrow();
  });

  it("does not return NaN for any required currency", () => {
    for (const currency of REQUIRED_CURRENCIES) {
      const result = fxToUsd(fx, currency);
      expect(isNaN(result), `NaN for ${currency}`).toBe(false);
    }
  });
});

describe("cityFxToUsd helper", () => {
  it("returns fx.ratesUsdPerUnit[city.currency] for a city with a known currency", () => {
    const mockCity = { currency: "EUR" } as { currency: string };
    expect(cityFxToUsd(fx, mockCity)).toBe(fx.ratesUsdPerUnit["EUR"]);
  });

  it("matches fxToUsd(fx, city.currency) exactly", () => {
    for (const currency of ["USD", "JPY", "IDR", "GBP", "AUD"]) {
      const mockCity = { currency } as { currency: string };
      expect(cityFxToUsd(fx, mockCity)).toBe(fxToUsd(fx, currency));
    }
  });

  it("throws for a city with an unknown currency", () => {
    const mockCity = { currency: "XYZ_UNKNOWN" } as { currency: string };
    expect(() => cityFxToUsd(fx, mockCity)).toThrow();
  });
});

describe("usdToDisplay helper", () => {
  it("returns 1 when displayCurrency is USD", () => {
    expect(usdToDisplay(fx, 100, "USD")).toBe(100);
  });

  it("converts USD to EUR correctly (usd / fxToUsd(fx, displayCurrency))", () => {
    const eurRate = fx.ratesUsdPerUnit["EUR"]!;
    const usdAmount = 200;
    expect(usdToDisplay(fx, usdAmount, "EUR")).toBeCloseTo(usdAmount / eurRate, 5);
  });

  it("throws for an unknown displayCurrency", () => {
    expect(() => usdToDisplay(fx, 100, "XYZ_UNKNOWN")).toThrow();
  });
});
