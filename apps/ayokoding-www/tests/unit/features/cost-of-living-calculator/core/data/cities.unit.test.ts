import { describe, expect, it } from "vitest";
import { fx } from "../../../../../../src/features/cost-of-living-calculator/core/data/fx";
import { cities, countries, dataset } from "../../../../../../src/features/cost-of-living-calculator/core/data/cities";

const EXPENSE_KEYS = ["housing", "food", "transport", "utilities", "healthcare", "childcare", "lifestyle"] as const;

const RELOCATION_SUNK_KEYS = ["deposit", "keyMoney", "moving", "visaAdmin"] as const;

describe("dataset", () => {
  it("has a snapshotDate in ISO format", () => {
    expect(dataset.snapshotDate).toMatch(/^\d{4}-\d{2}-\d{2}$/);
  });

  it("has non-empty cities and countries arrays", () => {
    expect(cities.length).toBeGreaterThan(0);
    expect(countries.length).toBeGreaterThan(0);
  });
});

describe("cities — expense categories", () => {
  it.each(cities)("$id has all 7 expense categories", (city) => {
    for (const key of EXPENSE_KEYS) {
      expect(city.expenses[key], `${city.id}: missing expenses.${key}`).toBeDefined();
      expect(typeof city.expenses[key].amount, `${city.id}: expenses.${key}.amount must be number`).toBe("number");
      expect(city.expenses[key].amount, `${city.id}: expenses.${key}.amount must be > 0`).toBeGreaterThan(0);
      expect(["high", "moderate", "proxy"], `${city.id}: expenses.${key}.confidence must be valid`).toContain(
        city.expenses[key].confidence,
      );
    }
  });
});

describe("cities — childcare & school", () => {
  it.each(cities)("$id has childcareMedianLocal", (city) => {
    expect(city.childcareMedianLocal).toBeDefined();
    expect(city.childcareMedianLocal.amount).toBeGreaterThan(0);
  });

  it.each(cities)("$id has schoolMedianLocal.public and .private", (city) => {
    expect(city.schoolMedianLocal.public).toBeDefined();
    expect(city.schoolMedianLocal.private).toBeDefined();
    expect(city.schoolMedianLocal.public.amount).toBeGreaterThanOrEqual(0);
    expect(city.schoolMedianLocal.private.amount).toBeGreaterThan(0);
  });
});

describe("cities — relocation block", () => {
  it.each(cities)("$id has full split relocation block", (city) => {
    for (const key of RELOCATION_SUNK_KEYS) {
      expect(city.relocation.sunkCosts[key], `${city.id}: missing relocation.sunkCosts.${key}`).toBeDefined();
      expect(
        city.relocation.sunkCosts[key].amount,
        `${city.id}: relocation.sunkCosts.${key}.amount must be >= 0`,
      ).toBeGreaterThanOrEqual(0);
    }
    expect(
      city.relocation.liquidityReserve.cashCushion,
      `${city.id}: missing liquidityReserve.cashCushion`,
    ).toBeDefined();
    expect(city.relocation.liquidityReserve.cashCushion.amount).toBeGreaterThan(0);
  });
});

describe("cities — country resolves", () => {
  const countryIndex = new Map(countries.map((c) => [c.id, c]));

  it.each(cities)("$id countryId resolves to a country", (city) => {
    expect(countryIndex.has(city.countryId), `${city.id}: countryId "${city.countryId}" not in countries`).toBe(true);
  });
});

describe("cities — currency resolves via fx.ts", () => {
  it.each(cities)("$id currency resolves to an fx.ts entry (no standalone fxToUsd field)", (city) => {
    expect(
      fx.ratesUsdPerUnit[city.currency],
      `${city.id}: currency "${city.currency}" not found in fx.ts`,
    ).toBeDefined();
    // city must NOT carry its own fxToUsd field
    expect(
      (city as Record<string, unknown>)["fxToUsd"],
      `${city.id}: city must not carry a standalone fxToUsd field`,
    ).toBeUndefined();
  });
});

describe("cities — subNational for US/CA/CH cities", () => {
  const subnationalCountries = new Set(["us", "ca", "ch"]);

  it.each(cities)("$id has subNational iff country is US/CA/CH", (city) => {
    if (subnationalCountries.has(city.countryId)) {
      expect(city.subNational, `${city.id} (${city.countryId}): must have subNational`).toBeDefined();
      const sn = city.subNational!;
      expect(sn.effectiveRate.low.amount).toBeGreaterThanOrEqual(0);
      expect(sn.effectiveRate.mid.amount).toBeGreaterThanOrEqual(0);
      expect(sn.effectiveRate.high.amount).toBeGreaterThanOrEqual(0);
    }
  });
});

describe("countries — tax bands + healthcare + insurance", () => {
  it.each(countries)("$id has banded effectiveRate with valid confidence", (country) => {
    const { effectiveRate } = country;
    for (const band of ["low", "mid", "high"] as const) {
      const m = effectiveRate[band];
      expect(typeof m.amount, `${country.id}: effectiveRate.${band}.amount must be number`).toBe("number");
      expect(m.amount, `${country.id}: effectiveRate.${band}.amount must be >= 0`).toBeGreaterThanOrEqual(0);
      expect(["high", "moderate", "proxy"]).toContain(m.confidence);
    }
    expect(effectiveRate.mid.amount, `${country.id}: mid >= low`).toBeGreaterThanOrEqual(effectiveRate.low.amount);
    expect(effectiveRate.high.amount, `${country.id}: high >= mid`).toBeGreaterThanOrEqual(effectiveRate.mid.amount);
  });

  it.each(countries)("$id has valid healthcareModelType", (country) => {
    expect(["oop", "tax-funded", "mixed"]).toContain(country.healthcareModelType);
  });

  it.each(countries)("$id has compulsoryInsurance with boolean health + socialSecurity", (country) => {
    expect(typeof country.compulsoryInsurance.health).toBe("boolean");
    expect(typeof country.compulsoryInsurance.socialSecurity).toBe("boolean");
  });

  it.each(countries)("$id has foreignerPublicSchool with a valid access + confidence", (country) => {
    expect(["open", "limited", "nationals-only"]).toContain(country.foreignerPublicSchool.access);
    expect(["high", "moderate", "proxy"]).toContain(country.foreignerPublicSchool.confidence);
  });
});

describe("dataset — region coverage", () => {
  it("has at least one ASEAN city", () => {
    expect(cities.some((c) => c.region === "asean")).toBe(true);
  });

  it("has at least one Japan city", () => {
    expect(cities.some((c) => c.region === "japan")).toBe(true);
  });

  it("has at least one Europe (non-Nordic) city", () => {
    expect(cities.some((c) => c.region === "europe")).toBe(true);
  });

  it("has at least one Nordic city", () => {
    expect(cities.some((c) => c.region === "nordics")).toBe(true);
  });
});

describe("dataset — no Israel", () => {
  it("has no city with currency ILS", () => {
    expect(cities.every((c) => c.currency !== "ILS")).toBe(true);
  });

  it("has no country with id il", () => {
    expect(countries.every((c) => c.id !== "il")).toBe(true);
  });

  it("has no city with countryId il", () => {
    expect(cities.every((c) => c.countryId !== "il")).toBe(true);
  });
});
