// ex-15: verify inline-block elements sit on the same line yet honor declared width/height (co-08).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const w1 = await page.locator("#chip1").evaluate((el) => el.offsetWidth);
const h1 = await page.locator("#chip1").evaluate((el) => el.offsetHeight);
const box1 = await page.locator("#chip1").boundingBox();
const box2 = await page.locator("#chip2").boundingBox();
console.log("chip1 size:", w1, h1, "chip1.y:", box1.y, "chip2.y:", box2.y);

if (w1 !== 80 || h1 !== 30) {
  throw new Error(`expected 80x30, got ${w1}x${h1}`);
}
if (Math.abs(box1.y - box2.y) > 1) {
  throw new Error("chips did not sit on the same inline line");
}
console.log("PASS: inline-block chips share a line and honor their declared 80x30 size");

await browser.close();
