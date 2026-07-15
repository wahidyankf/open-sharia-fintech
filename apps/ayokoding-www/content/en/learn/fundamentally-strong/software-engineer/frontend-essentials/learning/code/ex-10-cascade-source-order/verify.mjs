// ex-10: verify the later, equal-specificity declaration applies (co-05).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const color = await page.locator(".badge").evaluate((el) => getComputedStyle(el).color);
console.log("computed color:", color);
if (color !== "rgb(128, 0, 128)") {
  throw new Error(`expected the later declaration's purple to win, got ${color}`);
}
console.log("PASS: the second .badge rule (later in source order) applied");

await browser.close();
