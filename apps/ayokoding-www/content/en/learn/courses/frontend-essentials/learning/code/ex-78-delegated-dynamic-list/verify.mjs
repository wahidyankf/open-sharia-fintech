// ex-78: verify an item added AFTER initial render still responds to the one delegated listener, with no rebinding (co-15, co-21).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.locator("#add").click();
await page.locator("#add").click();
const beforeCount = await page.locator("#list li").count();
console.log("items after adding two dynamically:", beforeCount);
if (beforeCount !== 3) throw new Error(`expected 3 items, got ${beforeCount}`);

// remove the SECOND item, which was created after the page loaded and never
// had its own listener attached -- only the delegated <ul> listener handles it
await page.locator("#list li", { hasText: "Task 2" }).locator("button").click();
const afterCount = await page.locator("#list li").count();
const remaining = await page.locator("#list li").allInnerTexts();
console.log("items after removing a dynamically-added one:", afterCount, JSON.stringify(remaining));

if (afterCount !== 2) throw new Error(`expected 2 items after removal, got ${afterCount}`);
if (remaining.some((t) => t.includes("Task 2"))) throw new Error("Task 2 should have been removed");
console.log("PASS: the dynamically-added item worked correctly through the one delegated listener");

await browser.close();
