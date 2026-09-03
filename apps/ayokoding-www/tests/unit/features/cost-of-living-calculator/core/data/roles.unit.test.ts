import { describe, expect, it } from "vitest";
import { roleMatrix } from "../../../../../../src/features/cost-of-living-calculator/core/data/roles";

const EXPECTED_COUNTRY_IDS = new Set([
  "sg",
  "th",
  "id",
  "my",
  "vn",
  "ph",
  "jp",
  "gb",
  "de",
  "nl",
  "pt",
  "ch",
  "pl",
  "cz",
  "fr",
  "se",
  "dk",
  "no",
  "fi",
  "us",
  "ca",
  "br",
  "mx",
  "ae",
  "in",
  "kr",
  "au",
  "ke",
]);

const EXPECTED_ROLES = [
  "swe_1",
  "swe_2",
  "senior_swe",
  "eng_manager",
  "staff_swe",
  "senior_eng_manager",
  "senior_staff_swe",
  "director",
  "principal_swe",
  "senior_director",
  "distinguished_swe",
  "vp_eng",
  "fellow",
  "svp_eng",
  "cto",
] as const;

const VALID_CONFIDENCE = new Set(["high", "moderate", "proxy"]);

describe("roleMatrix", () => {
  describe("snapshotDate", () => {
    it("is an ISO date string", () => {
      expect(roleMatrix.snapshotDate).toMatch(/^\d{4}-\d{2}-\d{2}$/);
    });
  });

  describe("ladder", () => {
    it("has exactly 15 rungs", () => {
      expect(roleMatrix.ladder).toHaveLength(15);
    });

    it("contains all expected roles", () => {
      const ladderRoles = roleMatrix.ladder.map((r) => r.role);
      for (const role of EXPECTED_ROLES) {
        expect(ladderRoles).toContain(role);
      }
    });

    it("has strictly increasing rank 1..15", () => {
      const ranks = roleMatrix.ladder.map((r) => r.rank);
      for (let i = 0; i < ranks.length; i++) {
        expect(ranks[i]).toBe(i + 1);
      }
    });

    it("has valid track on every rung", () => {
      for (const rung of roleMatrix.ladder) {
        expect(["ic", "mgmt"]).toContain(rung.track);
      }
    });

    it("has bilingual labels on every rung", () => {
      for (const rung of roleMatrix.ladder) {
        expect(typeof rung.label.en).toBe("string");
        expect(rung.label.en.length).toBeGreaterThan(0);
        expect(typeof rung.label.id).toBe("string");
        expect(rung.label.id.length).toBeGreaterThan(0);
      }
    });

    it("IC and mgmt tracks each stay strictly ascending by rank", () => {
      const icRanks = roleMatrix.ladder.filter((r) => r.track === "ic").map((r) => r.rank);
      const mgmtRanks = roleMatrix.ladder.filter((r) => r.track === "mgmt").map((r) => r.rank);
      for (let i = 1; i < icRanks.length; i++) {
        expect(icRanks[i]!).toBeGreaterThan(icRanks[i - 1]!);
      }
      for (let i = 1; i < mgmtRanks.length; i++) {
        expect(mgmtRanks[i]!).toBeGreaterThan(mgmtRanks[i - 1]!);
      }
    });
  });

  describe("salaries key set", () => {
    it("exactly matches the 28 countries in cities.ts", () => {
      const matrixCountries = new Set(Object.keys(roleMatrix.salaries));
      expect(matrixCountries).toEqual(EXPECTED_COUNTRY_IDS);
    });

    it("contains no Israeli or ILS entries", () => {
      const keys = Object.keys(roleMatrix.salaries);
      expect(keys).not.toContain("il");
      for (const countryId of keys) {
        const countryRoles = roleMatrix.salaries[countryId]!;
        for (const role of Object.keys(countryRoles)) {
          const dist = countryRoles[role as keyof typeof countryRoles]!;
          expect(dist.p25.note ?? "").not.toContain("ILS");
          expect(dist.median.note ?? "").not.toContain("ILS");
          expect(dist.p75.note ?? "").not.toContain("ILS");
        }
      }
    });
  });

  describe("per-cell distribution invariants", () => {
    it.each(Array.from(EXPECTED_COUNTRY_IDS))("country %s has all 15 roles with valid distributions", (countryId) => {
      const countryDist = roleMatrix.salaries[countryId]!;
      expect(countryDist).toBeDefined();
      for (const role of EXPECTED_ROLES) {
        const dist = countryDist[role]!;
        expect(dist).toBeDefined();

        // p25 ≤ median ≤ p75, all positive
        expect(dist.p25.monthlyGrossLocal).toBeGreaterThan(0);
        expect(dist.median.monthlyGrossLocal).toBeGreaterThan(0);
        expect(dist.p75.monthlyGrossLocal).toBeGreaterThan(0);
        expect(dist.p25.monthlyGrossLocal).toBeLessThanOrEqual(dist.median.monthlyGrossLocal);
        expect(dist.median.monthlyGrossLocal).toBeLessThanOrEqual(dist.p75.monthlyGrossLocal);

        // valid confidence on each percentile
        expect(VALID_CONFIDENCE).toContain(dist.p25.confidence);
        expect(VALID_CONFIDENCE).toContain(dist.median.confidence);
        expect(VALID_CONFIDENCE).toContain(dist.p75.confidence);

        // nonSalaryComp present and non-negative
        expect(dist.nonSalaryComp).toBeDefined();
        expect(dist.nonSalaryComp.annualLocal).toBeGreaterThanOrEqual(0);
        expect(VALID_CONFIDENCE).toContain(dist.nonSalaryComp.confidence);
      }
    });
  });

  describe("monotonic salary within each track", () => {
    it.each(Array.from(EXPECTED_COUNTRY_IDS))("country %s IC track medians non-decrease by rank", (countryId) => {
      const countryDist = roleMatrix.salaries[countryId]!;
      const icRoles = roleMatrix.ladder.filter((r) => r.track === "ic");
      const medians = icRoles.map((r) => countryDist[r.role]!.median.monthlyGrossLocal);
      for (let i = 1; i < medians.length; i++) {
        expect(medians[i]!).toBeGreaterThanOrEqual(medians[i - 1]!);
      }
    });

    it.each(Array.from(EXPECTED_COUNTRY_IDS))("country %s mgmt track medians non-decrease by rank", (countryId) => {
      const countryDist = roleMatrix.salaries[countryId]!;
      const mgmtRoles = roleMatrix.ladder.filter((r) => r.track === "mgmt");
      const medians = mgmtRoles.map((r) => countryDist[r.role]!.median.monthlyGrossLocal);
      for (let i = 1; i < medians.length; i++) {
        expect(medians[i]!).toBeGreaterThanOrEqual(medians[i - 1]!);
      }
    });
  });
});
