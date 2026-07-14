// ex-11: verify two independent rules resolve --brand to the same color (co-06).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const headingColor = await page.locator(".heading").evaluate((el) => getComputedStyle(el).color);
const linkColor = await page.locator(".link").evaluate((el) => getComputedStyle(el).color);
console.log("heading color:", headingColor);
console.log("link color:", linkColor);

if (headingColor !== linkColor) {
  throw new Error("var(--brand) resolved to two different colors");
}
if (headingColor !== "rgb(10, 100, 200)") {
  throw new Error(`unexpected resolved color: ${headingColor}`);
}
console.log("PASS: both rules resolved var(--brand) to the identical computed color");

await browser.close();
