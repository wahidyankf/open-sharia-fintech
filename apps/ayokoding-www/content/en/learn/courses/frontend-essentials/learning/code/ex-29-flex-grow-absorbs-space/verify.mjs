// ex-29: verify the flex-grow:1 child absorbs all remaining free space (co-09).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const growerWidth = await page.locator("#grower").evaluate((el) => el.offsetWidth);
console.log("grower width:", growerWidth);
// row 400 - fixed 60 = 340 remaining, all of which the sole grow:1 child absorbs
if (growerWidth !== 340) {
  throw new Error(`expected grower to absorb 340px of free space, got ${growerWidth}`);
}
console.log("PASS: flex-grow:1 child absorbed exactly the row's remaining free space");

await browser.close();
