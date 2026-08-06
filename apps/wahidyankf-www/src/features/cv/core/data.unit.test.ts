import { describe, it, expect } from "vitest";
import {
  parseDate,
  calculateDuration,
  formatDuration,
  calculateTotalDuration,
  getTopSkillsLastFiveYears,
  CVEntry,
} from "./data";

describe("data.ts functions", () => {
  describe("parseDate", () => {
    it("should correctly parse a date string", () => {
      const result = parseDate("January 2020");
      expect(result).toEqual(new Date(2020, 0));
    });

    it("should throw an error for invalid month", () => {
      expect(() => parseDate("InvalidMonth 2020")).toThrowError("Invalid month: InvalidMonth");
    });
  });

  describe("calculateDuration", () => {
    it("should calculate duration correctly", () => {
      const result = calculateDuration("January 2020 - December 2020");
      expect(result).toBe(12);
    });

    it('should handle "Present" as end date', () => {
      const result = calculateDuration("January 2020 - Present");
      expect(result).toBeGreaterThan(12);
    });
  });

  describe("formatDuration", () => {
    it("should format duration correctly for years and months", () => {
      expect(formatDuration(15)).toBe("1 year 3 months");
    });

    it("should format duration correctly for only years", () => {
      expect(formatDuration(24)).toBe("2 years");
    });

    it("should format duration correctly for only months", () => {
      expect(formatDuration(5)).toBe("5 months");
    });
  });

  describe("calculateTotalDuration", () => {
    it("should calculate total duration correctly for the entire work experience, ignoring overlaps and counting partial months", () => {
      const periods = [
        { start: new Date(2017, 9, 1), end: new Date() }, // October 2017 to present
      ];
      const result = calculateTotalDuration(periods);
      const currentDate = new Date();
      const expectedMonths = (currentDate.getFullYear() - 2017) * 12 + (currentDate.getMonth() - 9) + 1; // +1 to include both start and end months
      expect(result).toBe(expectedMonths);
    });

    it("should count October 2017 - December 2017 as 3 months (Junior Frontend Engineer)", () => {
      const periods = [
        { start: new Date(2017, 9, 1), end: new Date(2017, 11, 31) }, // October 1, 2017 to December 31, 2017
      ];
      const result = calculateTotalDuration(periods);
      expect(result).toBe(3);
    });

    it("should handle overlapping periods correctly", () => {
      const periods = [
        { start: new Date(2020, 0, 1), end: new Date(2020, 11, 31) }, // Jan 2020 to Dec 2020
        { start: new Date(2020, 6, 1), end: new Date(2021, 5, 30) }, // Jul 2020 to Jun 2021
      ];
      const result = calculateTotalDuration(periods);
      // Jan 2020 to Jun 2021 inclusive. The overlapping Jul-Dec 2020 counts once.
      expect(result).toBe(18);
    });

    it("should count a shared handover month once when one role starts as another ends", () => {
      // Regression: roles handing over inside one calendar month used to have
      // that month counted twice, inflating the career total by a month per
      // handover.
      const periods = [
        { start: new Date(2021, 10, 1), end: new Date(2022, 6, 1) }, // Nov 2021 to Jul 2022
        { start: new Date(2022, 6, 1), end: new Date(2022, 11, 1) }, // Jul 2022 to Dec 2022
      ];
      const result = calculateTotalDuration(periods);
      expect(result).toBe(14); // Nov 2021 to Dec 2022 inclusive, not 15
    });

    it("should absorb a period fully nested inside another", () => {
      const periods = [
        { start: new Date(2019, 8, 1), end: new Date(2021, 9, 1) }, // Sep 2019 to Oct 2021
        { start: new Date(2021, 7, 1), end: new Date(2021, 9, 1) }, // Aug 2021 to Oct 2021
      ];
      const result = calculateTotalDuration(periods);
      expect(result).toBe(26); // Sep 2019 to Oct 2021 inclusive
    });

    it("should join back-to-back periods without inventing a gap", () => {
      const periods = [
        { start: new Date(2017, 9, 1), end: new Date(2017, 11, 1) }, // Oct 2017 to Dec 2017
        { start: new Date(2018, 0, 1), end: new Date(2018, 2, 1) }, // Jan 2018 to Mar 2018
      ];
      const result = calculateTotalDuration(periods);
      expect(result).toBe(6); // Oct 2017 to Mar 2018 inclusive
    });

    it("should exclude months in a genuine gap between periods", () => {
      const periods = [
        { start: new Date(2018, 0, 1), end: new Date(2018, 2, 1) }, // Jan 2018 to Mar 2018 (3)
        { start: new Date(2019, 0, 1), end: new Date(2019, 1, 1) }, // Jan 2019 to Feb 2019 (2)
      ];
      const result = calculateTotalDuration(periods);
      expect(result).toBe(5); // The 9-month gap is not counted
    });

    it("should not mutate the caller's periods array", () => {
      const periods = [
        { start: new Date(2022, 0, 1), end: new Date(2022, 5, 1) },
        { start: new Date(2020, 0, 1), end: new Date(2020, 5, 1) },
      ];
      const original = [...periods];
      calculateTotalDuration(periods);
      expect(periods).toEqual(original);
    });

    it("should return 0 for empty periods", () => {
      expect(calculateTotalDuration([])).toBe(0);
    });

    it("should count July 2022 - December 2022 as 6 months", () => {
      const periods = [
        { start: new Date(2022, 6, 1), end: new Date(2022, 11, 31) }, // July 1, 2022 to December 31, 2022
      ];
      const result = calculateTotalDuration(periods);
      expect(result).toBe(6);
    });
  });

  describe("getTopSkillsLastFiveYears", () => {
    it("should return top skills from the last five years", () => {
      const mockData: CVEntry[] = [
        {
          title: "Frontend Engineer",
          organization: "PT. Ruangguru Indonesia",
          period: "January 2020 - Present",
          details: [],
          skills: ["JavaScript", "React", "Node.js"],
          type: "work",
          employmentType: "Full-time",
          location: "Jakarta, Indonesia",
          locationType: "Remote",
          programmingLanguages: ["JavaScript", "TypeScript", "ReasonML", "SQL", "HTML", "CSS"],
          frameworks: ["React.js", "React Native", "ReasonReact"],
        },
        {
          title: "Frontend Engineer",
          organization: "PT. Ruangguru Indonesia",
          period: "January 2018 - December 2019",
          details: [],
          skills: ["Python", "Django", "JavaScript"],
          type: "work",
          employmentType: "Full-time",
          location: "Jakarta, Indonesia",
          locationType: "On-site",
          programmingLanguages: ["JavaScript", "Python", "TypeScript"],
          frameworks: ["React.js", "React Native", "ReasonReact"],
        },
      ];

      const result = getTopSkillsLastFiveYears(mockData);
      expect(result.length).toBeLessThanOrEqual(10);
      expect(result[0].name).toBe("JavaScript");
    });

    it("should omit skills whose most recent role ended outside the five-year window", () => {
      const mockData: CVEntry[] = [
        {
          title: "Current Role",
          organization: "Now Corp",
          period: "January 2024 - Present",
          details: [],
          skills: ["TypeScript"],
          type: "work",
        },
        {
          title: "Ancient Role",
          organization: "Then Corp",
          period: "January 2010 - December 2012",
          details: [],
          skills: ["COBOL"],
          type: "work",
        },
      ];

      const names = getTopSkillsLastFiveYears(mockData).map((skill) => skill.name);
      expect(names).toContain("TypeScript");
      expect(names).not.toContain("COBOL");
    });

    it("should report a lifetime total duration rather than one clipped to five years", () => {
      const mockData: CVEntry[] = [
        {
          title: "Long Haul",
          organization: "Same Corp",
          period: "January 2010 - Present",
          details: [],
          skills: ["Software Engineering"],
          type: "work",
        },
      ];

      const [topSkill] = getTopSkillsLastFiveYears(mockData);
      // A window-clipped duration could never exceed 60 months.
      expect(topSkill.duration).toBeGreaterThan(60);
    });
  });
});
