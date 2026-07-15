// ex-04: verify every anchor has an href and visible link text (co-03).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const anchors = await page.evaluate(() =>
  Array.from(document.querySelectorAll("li a")).map((a) => ({
    href: a.getAttribute("href"),
    text: a.textContent.trim(),
  })),
);
console.log("anchors:", JSON.stringify(anchors));

if (anchors.length !== 3) {
  throw new Error(`expected 3 anchors, found ${anchors.length}`);
}
for (const a of anchors) {
  if (!a.href) throw new Error("an anchor is missing href");
  if (!a.text) throw new Error("an anchor is missing visible text");
}
console.log("PASS: every list anchor has both an href and non-empty link text");

await browser.close();
