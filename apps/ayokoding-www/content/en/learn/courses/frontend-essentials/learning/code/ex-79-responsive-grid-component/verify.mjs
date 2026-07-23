// ex-79: verify the card grid's column count changes with the viewport width (co-10, co-11).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

async function columnCount() {
  const boxes = await page.locator(".card").evaluateAll((els) => els.map((el) => el.getBoundingClientRect().y));
  return new Set(boxes.map((y) => Math.round(y))).size === 1
    ? new Set(boxes.map((y) => Math.round(y))).size
    : boxes.length;
}
async function firstRowCount() {
  const ys = await page
    .locator(".card")
    .evaluateAll((els) => els.map((el) => Math.round(el.getBoundingClientRect().y)));
  const topY = Math.min(...ys);
  return ys.filter((y) => y === topY).length;
}

await page.setViewportSize({ width: 400, height: 400 });
const narrow = await firstRowCount();
await page.setViewportSize({ width: 700, height: 400 });
const medium = await firstRowCount();
await page.setViewportSize({ width: 1000, height: 400 });
const wide = await firstRowCount();
console.log("cards in first row -- narrow:", narrow, "medium:", medium, "wide:", wide);

if (narrow !== 1) throw new Error(`expected 1 column under 500px, got ${narrow}`);
if (medium !== 2) throw new Error(`expected 2 columns between 500-900px, got ${medium}`);
if (wide !== 3) throw new Error(`expected 3 columns above 900px, got ${wide}`);
console.log("PASS: the grid's column count changed correctly at each breakpoint (1 -> 2 -> 3)");

await browser.close();
