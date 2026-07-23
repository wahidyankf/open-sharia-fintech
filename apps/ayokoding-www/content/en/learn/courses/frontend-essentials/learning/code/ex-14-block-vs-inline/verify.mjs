// ex-14: verify a block div spans full width while an inline span wraps only its content (co-08).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const bodyWidth = await page.locator("body").evaluate((el) => el.clientWidth);
const blockWidth = await page.locator("#blockBox").evaluate((el) => el.offsetWidth);
const spanBox = await page.locator("#inlineSpan").boundingBox();
console.log("body width:", bodyWidth, "block div width:", blockWidth, "inline span width:", spanBox.width);

if (blockWidth !== bodyWidth) {
  throw new Error(`expected block div to span full body width ${bodyWidth}, got ${blockWidth}`);
}
if (spanBox.width >= bodyWidth) {
  throw new Error("inline span unexpectedly spans the full width");
}
console.log("PASS: block div fills the container width; inline span wraps only its own content");

await browser.close();
