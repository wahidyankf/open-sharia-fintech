// ex-27: verify justify-content: space-between spreads children to the container's edges (co-09).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const rowBox = await page.locator(".row").boundingBox();
const leftBox = await page.locator("#left").boundingBox();
const rightBox = await page.locator("#right").boundingBox();
console.log(
  "row.x:",
  rowBox.x,
  "left.x:",
  leftBox.x,
  "right.right:",
  rightBox.x + rightBox.width,
  "row.right:",
  rowBox.x + rowBox.width,
);

if (Math.abs(leftBox.x - rowBox.x) > 1) {
  throw new Error("first chip is not flush with the row's left edge");
}
if (Math.abs(rightBox.x + rightBox.width - (rowBox.x + rowBox.width)) > 1) {
  throw new Error("last chip is not flush with the row's right edge");
}
console.log("PASS: space-between pinned the first and last chip to the row's edges");

await browser.close();
