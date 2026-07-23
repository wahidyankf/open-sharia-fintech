// ex-09: verify the id rule wins over the class rule (co-05).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const color = await page.locator("#price").evaluate((el) => getComputedStyle(el).color);
console.log("computed color:", color);
if (color !== "rgb(255, 0, 0)") {
  throw new Error(`expected the id rule's red to win, got ${color}`);
}
console.log("PASS: #price (specificity 1-0-0) beat .label (specificity 0-1-0)");

await browser.close();
