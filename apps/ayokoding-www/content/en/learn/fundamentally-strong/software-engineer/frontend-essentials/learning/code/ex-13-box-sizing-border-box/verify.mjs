// ex-13: verify box-sizing: border-box makes rendered width equal the declared width (co-07).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const offsetWidth = await page.locator("#box").evaluate((el) => el.offsetWidth);
console.log("offsetWidth:", offsetWidth);
if (offsetWidth !== 200) {
  throw new Error(`expected offsetWidth 200 (border-box folds padding+border in), got ${offsetWidth}`);
}
console.log("PASS: border-box keeps the rendered width at the declared 200px");

await browser.close();
