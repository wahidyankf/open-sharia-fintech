// ex-60: verify the aria-live region's content updates after the triggering event (co-25).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const before = await page.locator("#status").innerText();
await page.locator("#save").click();
const after = await page.locator("#status").innerText();
console.log("status before:", JSON.stringify(before), "status after save:", JSON.stringify(after));
if (before !== "") throw new Error("expected the live region to start empty");
if (after !== "Saved successfully") throw new Error(`live region did not update: "${after}"`);
console.log('PASS: the aria-live="polite" region\'s content updated after the save action');

await browser.close();
