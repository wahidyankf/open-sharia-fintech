import fs from "node:fs";
import path from "node:path";
import { describeFeature, loadFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";

const feature = await loadFeature(
  path.resolve(
    process.cwd(),
    "../../specs/apps/ayokoding/www/behaviours/frontend/course-paths/skills-path-composition.feature",
  ),
);

const expectedCourseOrder = [
  "accounting-foundations",
  "chart-of-accounts-and-data-modeling",
  "financial-statements-and-close-cycle",
  "journal-entries-and-posting-mechanics",
  "accrual-accounting-and-revenue-recognition",
  "accounts-payable-and-procure-to-pay",
  "accounts-receivable-and-order-to-cash",
  "managerial-and-cost-accounting",
  "fixed-assets-and-depreciation",
  "inventory-and-cogs-accounting",
  "lease-and-intangible-asset-accounting",
  "multi-currency-accounting-and-fx-translation",
  "consolidation-and-multi-entity-accounting",
  "financial-reporting-standards-ifrs-vs-gaap",
  "audit-controls-and-compliance",
  "payroll-and-tax-accounting-essentials",
  "treasury-and-cash-management",
  "financial-reporting-and-xbrl",
  "general-ledger-system-architecture",
] as const;

const shariaExtension = [
  "sharia-accounting-and-aaoifi-standards",
  "islamic-contract-modeling-for-systems",
  "zakah-computation-and-reporting-for-systems",
  "sukuk-and-islamic-capital-markets-accounting",
  "sharia-ledger-system-architecture",
] as const;

describeFeature(feature, ({ ScenarioOutline }) => {
  ScenarioOutline(
    "A two-segment skills path ID resolves to its full shared accounting slice",
    ({ Given, When, Then, And }, variables) => {
      let manifest: { pathId: string; courseOrder: string[] };
      Given('the published accounting manifest for "<path-id>"', () => {
        const pathId = String(variables["path-id"]);
        const [, manifestName] = pathId.split("/");
        const manifestPath = path.resolve(
          process.cwd(),
          `src/features/course-paths/manifests/skills/${manifestName}.json`,
        );
        manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8")) as typeof manifest;
        expect(manifest.pathId).toBe(pathId);
      });
      When("its ordered course context is inspected", () => {
        expect(manifest.courseOrder.length).toBeGreaterThan(0);
      });
      Then("it contains its published accounting order", () => {
        expect(manifest.courseOrder).toEqual(
          manifest.pathId === "skills/sharia-accounting"
            ? [...expectedCourseOrder, ...shariaExtension]
            : expectedCourseOrder,
        );
      });
      And("every course context is represented by one course directory", () => {
        const coursesRoot = path.resolve(process.cwd(), "content/en/learn/courses");
        for (const courseId of manifest.courseOrder) {
          expect(fs.statSync(path.join(coursesRoot, courseId)).isDirectory()).toBe(true);
        }
      });
      And("an over-segmented path ID is not a published accounting path", () => {
        expect(manifest.pathId.split("/")).toHaveLength(2);
      });
    },
  );
});
