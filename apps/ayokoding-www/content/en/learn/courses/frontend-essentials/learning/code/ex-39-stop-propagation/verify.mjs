// ex-39: verify stopPropagation() on the child keeps the parent listener from firing (co-16, co-15).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.locator("#child").click();
const report = await page.locator("#report").innerText();
console.log("report after click with stopPropagation:", report);
if (report !== "parent not fired") {
  throw new Error(`expected the parent listener to be suppressed, got "${report}"`);
}
console.log("PASS: stopPropagation() on the child kept the click from ever reaching the parent");

await browser.close();
