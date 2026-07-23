// ex-18: verify querySelectorAll('li').length equals the real item count (co-12).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const length = await page.evaluate(() => document.querySelectorAll("li").length);
console.log("querySelectorAll('li').length:", length);
if (length !== 4) {
  throw new Error(`expected 4 <li> elements, got ${length}`);
}
console.log("PASS: NodeList length (4) matches the real number of <li> elements in the DOM");

await browser.close();
