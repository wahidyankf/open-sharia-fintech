import fs from "node:fs";
import path from "node:path";
import { describeFeature, loadFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";

const appRoot = process.cwd();
const feature = await loadFeature(
  path.resolve(
    appRoot,
    "../../specs/apps/ayokoding/www/behaviors/frontend/course-paths/skills-path-composition.feature",
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
];

const shariaExtension = [
  "sharia-accounting-and-aaoifi-standards",
  "islamic-contract-modeling-for-systems",
  "zakah-computation-and-reporting-for-systems",
  "sukuk-and-islamic-capital-markets-accounting",
  "sharia-ledger-system-architecture",
];

describeFeature(feature, ({ ScenarioOutline }) => {
  ScenarioOutline(
    "A two-segment skills path ID resolves to its full shared accounting slice",
    ({ Given, When, Then, And }, examples) => {
      const pathId = String(examples["path-id"]);
      let manifest: { pathId: string; courseOrder: string[] };

      Given('the published accounting manifest for "<path-id>"', () => {
        const [, manifestName] = pathId.split("/");
        manifest = JSON.parse(
          fs.readFileSync(
            path.join(appRoot, "src/features/course-paths/manifests/skills", `${manifestName}.json`),
            "utf8",
          ),
        ) as { pathId: string; courseOrder: string[] };
      });

      When("its ordered course context is inspected", () => {
        expect(manifest.pathId).toBe(pathId);
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/skills-path-composition.feature:A two-segment skills path ID resolves to its full shared accounting slice
      Then("it contains its published accounting order", () => {
        expect(manifest.courseOrder).toEqual(
          pathId === "skills/sharia-accounting" ? [...expectedCourseOrder, ...shariaExtension] : expectedCourseOrder,
        );
      });

      And("every course context is represented by one course directory", () => {
        for (const courseId of manifest.courseOrder) {
          expect(fs.statSync(path.join(appRoot, "content/en/learn/courses", courseId)).isDirectory()).toBe(true);
        }
      });

      And("an over-segmented path ID is not a published accounting path", () => {
        expect(manifest.pathId.split("/")).toHaveLength(2);
      });
    },
  );
});
