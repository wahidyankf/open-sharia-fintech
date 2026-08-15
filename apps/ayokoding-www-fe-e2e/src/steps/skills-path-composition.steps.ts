import fs from "node:fs";
import path from "node:path";
import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";

const { Given, When, Then } = createBdd();
const workspaceRoot = path.resolve(process.cwd(), "../..");

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

type AccountingWorld = { pathId: string; courseOrder: string[] };
let activeAccountingWorld: AccountingWorld | undefined;

Given("the published accounting manifest for {string}", async ({}, pathId: string) => {
  const [, manifestName] = pathId.split("/");
  const manifestPath = path.join(
    workspaceRoot,
    "apps/ayokoding-www/src/features/course-paths/manifests/skills",
    `${manifestName}.json`,
  );
  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8")) as { pathId: string; courseOrder: string[] };
  activeAccountingWorld = { pathId: manifest.pathId, courseOrder: manifest.courseOrder };
});

When("its ordered course context is inspected", async () => {
  expect(activeAccountingWorld).toBeDefined();
});

Then("it contains its published accounting order", async () => {
  expect(activeAccountingWorld?.courseOrder).toEqual(
    activeAccountingWorld?.pathId === "skills/sharia-accounting"
      ? [...expectedCourseOrder, ...shariaExtension]
      : expectedCourseOrder,
  );
});

Then("every course context is represented by one course directory", async () => {
  const courseOrder = activeAccountingWorld?.courseOrder ?? [];
  const coursesRoot = path.join(workspaceRoot, "apps/ayokoding-www/content/en/learn/courses");
  for (const courseId of courseOrder) {
    expect(fs.statSync(path.join(coursesRoot, courseId)).isDirectory()).toBe(true);
  }
});

Then("an over-segmented path ID is not a published accounting path", async () => {
  expect(activeAccountingWorld?.pathId.split("/")).toHaveLength(2);
});
