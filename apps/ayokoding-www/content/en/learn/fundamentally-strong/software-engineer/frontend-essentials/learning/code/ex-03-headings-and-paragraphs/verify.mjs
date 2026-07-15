// ex-03: verify exactly one h1 and a correctly nested outline (co-03).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const levels = await page.evaluate(() =>
  Array.from(document.querySelectorAll("h1, h2, h3, h4, h5, h6")).map((h) => Number(h.tagName.slice(1))),
);
console.log("heading levels in document order:", JSON.stringify(levels));

const h1Count = levels.filter((l) => l === 1).length;
if (h1Count !== 1) {
  throw new Error(`expected exactly one h1, found ${h1Count}`);
}

let previous = levels[0];
for (const level of levels.slice(1)) {
  if (level > previous + 1) {
    throw new Error(`outline skips a level: ${previous} -> ${level}`);
  }
  previous = level;
}
console.log("PASS: exactly one h1 and no skipped heading level in the outline");

await browser.close();
