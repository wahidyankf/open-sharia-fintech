// ex-32: verify the measured spacing between tracks equals the declared gap (co-10).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const boxA = await page.locator("#a").boundingBox();
const boxB = await page.locator("#b").boundingBox();
const spacing = boxB.x - (boxA.x + boxA.width);
console.log("spacing between tracks:", spacing);
if (spacing !== 16) {
  throw new Error(`expected 16px gap, measured ${spacing}`);
}
console.log("PASS: the measured gap between the two grid tracks was exactly the declared 16px");

await browser.close();
