// ex-07: verify only links inside #nav receive the descendant-selector rule (co-04).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const navColors = await page.$$eval("#nav a", (els) => els.map((el) => getComputedStyle(el).color));
const outsideColor = await page.locator("p a").evaluate((el) => getComputedStyle(el).color);
console.log("nav link colors:", JSON.stringify(navColors));
console.log("outside link color:", outsideColor);

for (const c of navColors) {
  if (c !== "rgb(0, 100, 200)") throw new Error(`nav link not styled: ${c}`);
}
if (outsideColor === "rgb(0, 100, 200)") {
  throw new Error("outside link should not match #nav a");
}
console.log("PASS: #nav a styled only links inside #nav");

await browser.close();
