// ex-12: verify offsetWidth equals content width + padding + border (default content-box) (co-07).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const offsetWidth = await page.locator("#box").evaluate((el) => el.offsetWidth);
console.log("offsetWidth:", offsetWidth);
// content 200 + padding 10*2 + border 5*2 = 230; margin is OUTSIDE offsetWidth entirely
const expected = 200 + 10 * 2 + 5 * 2;
if (offsetWidth !== expected) {
  throw new Error(`expected offsetWidth ${expected}, got ${offsetWidth}`);
}
console.log("PASS: offsetWidth (230) = content (200) + padding (20) + border (10); margin excluded");

await browser.close();
