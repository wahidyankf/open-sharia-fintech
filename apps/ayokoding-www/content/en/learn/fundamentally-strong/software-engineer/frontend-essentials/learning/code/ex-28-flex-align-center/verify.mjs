// ex-28: verify align-items: center vertically centers the child inside the row (co-09).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const rowBox = await page.locator(".row").boundingBox();
const chipBox = await page.locator("#chip").boundingBox();
const rowCenter = rowBox.y + rowBox.height / 2;
const chipCenter = chipBox.y + chipBox.height / 2;
console.log("row center y:", rowCenter, "chip center y:", chipCenter);

if (Math.abs(rowCenter - chipCenter) > 1) {
  throw new Error(`chip is not vertically centered: row center ${rowCenter}, chip center ${chipCenter}`);
}
console.log("PASS: align-items: center vertically centered the chip within the row");

await browser.close();
