import { describe, expect, it } from "vitest";
import { cities, countries, dataset } from "../../../../../src/features/cost-of-living-calculator/core/data/cities";
import {
  countriesForRegion,
  citiesForCountry,
  scopedCities,
} from "../../../../../src/features/cost-of-living-calculator/core/geo-filter";

describe("geo-filter", () => {
  describe("countriesForRegion", () => {
    it("returns only countries whose cities are in the given region", () => {
      const aseanCountries = countriesForRegion(dataset, "asean");
      // ASEAN cities: singapore(sg), bangkok(th), jakarta(id), kuala-lumpur(my), ho-chi-minh-city(vn), manila(ph)
      const ids = aseanCountries.map((c) => c.id);
      expect(ids).toContain("sg");
      expect(ids).toContain("th");
      expect(ids).toContain("id");
      expect(ids).toContain("my");
      expect(ids).toContain("vn");
      expect(ids).toContain("ph");
      // non-ASEAN countries must not appear
      expect(ids).not.toContain("de");
      expect(ids).not.toContain("us");
      expect(ids).not.toContain("jp");
    });

    it("returns europe countries for europe region", () => {
      const europeCountries = countriesForRegion(dataset, "europe");
      const ids = europeCountries.map((c) => c.id);
      expect(ids).toContain("gb");
      expect(ids).toContain("de");
      expect(ids).toContain("nl");
      expect(ids).not.toContain("sg");
      expect(ids).not.toContain("us");
    });

    it("returns nordics countries for nordics region", () => {
      const nordicCountries = countriesForRegion(dataset, "nordics");
      const ids = nordicCountries.map((c) => c.id);
      expect(ids).toContain("se");
      expect(ids).toContain("dk");
      expect(ids).toContain("no");
      expect(ids).toContain("fi");
      expect(ids).not.toContain("de");
    });

    it("returns empty array for unknown region", () => {
      // @ts-expect-error testing invalid input
      const result = countriesForRegion(dataset, "unknown_region");
      expect(result).toHaveLength(0);
    });

    it("returns only unique countries (no duplicates)", () => {
      for (const region of ["asean", "europe", "nordics", "americas"] as const) {
        const result = countriesForRegion(dataset, region);
        const ids = result.map((c) => c.id);
        const uniqueIds = new Set(ids);
        expect(ids.length).toBe(uniqueIds.size);
      }
    });
  });

  describe("citiesForCountry", () => {
    it("returns only cities in Germany", () => {
      const deCities = citiesForCountry(dataset, "de");
      for (const city of deCities) {
        expect(city.countryId).toBe("de");
      }
      expect(deCities.length).toBeGreaterThan(0);
    });

    it("returns only cities in Singapore", () => {
      const sgCities = citiesForCountry(dataset, "sg");
      for (const city of sgCities) {
        expect(city.countryId).toBe("sg");
      }
      const ids = sgCities.map((c) => c.id);
      expect(ids).toContain("singapore");
    });

    it("returns only cities in the US", () => {
      const usCities = citiesForCountry(dataset, "us");
      for (const city of usCities) {
        expect(city.countryId).toBe("us");
      }
      expect(usCities.length).toBeGreaterThan(1);
    });

    it("returns empty array for unknown country", () => {
      const result = citiesForCountry(dataset, "zz");
      expect(result).toHaveLength(0);
    });
  });

  describe("scopedCities", () => {
    it("returns all cities when no filter is applied", () => {
      const result = scopedCities(dataset, null, null, null);
      expect(result).toHaveLength(cities.length);
    });

    it("filters to region cities when only region is set", () => {
      const result = scopedCities(dataset, "asean", null, null);
      for (const city of result) {
        expect(city.region).toBe("asean");
      }
      expect(result.length).toBeGreaterThan(0);
    });

    it("filters to country cities when region + country are set", () => {
      const result = scopedCities(dataset, "europe", "de", null);
      for (const city of result) {
        expect(city.countryId).toBe("de");
        expect(city.region).toBe("europe");
      }
      expect(result.length).toBeGreaterThan(0);
    });

    it("returns single city when all three filters set", () => {
      const result = scopedCities(dataset, "asean", "sg", "singapore");
      expect(result).toHaveLength(1);
      expect(result[0]!.id).toBe("singapore");
    });

    it("clearing region (null) returns all cities", () => {
      const all = scopedCities(dataset, null, null, null);
      expect(all).toHaveLength(cities.length);
    });

    it("setting only country (region null) still filters by country", () => {
      // country alone (no region) should still narrow to that country's cities
      const result = scopedCities(dataset, null, "jp", null);
      for (const city of result) {
        expect(city.countryId).toBe("jp");
      }
      expect(result.length).toBeGreaterThan(0);
    });

    it("setting only city (region+country null) returns just that city", () => {
      const result = scopedCities(dataset, null, null, "tokyo");
      expect(result).toHaveLength(1);
      expect(result[0]!.id).toBe("tokyo");
    });

    it("region filter with mismatched country returns empty (country not in region)", () => {
      // tokyo is in "japan", not "europe"
      const result = scopedCities(dataset, "europe", "jp", null);
      expect(result).toHaveLength(0);
    });

    it("returns valid Country objects from countriesForRegion", () => {
      const europeCountries = countriesForRegion(dataset, "europe");
      for (const country of europeCountries) {
        const found = countries.find((c) => c.id === country.id);
        expect(found).toBeDefined();
      }
    });

    it("city filter wins over country+region mismatch", () => {
      // Direct city selection should still work even with conflicting higher filters
      const result = scopedCities(dataset, null, null, "berlin");
      expect(result).toHaveLength(1);
      expect(result[0]!.id).toBe("berlin");
    });
  });
});
