// ex-33: verify the layout changes from side-by-side to stacked below the 600px breakpoint (co-11).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.setViewportSize({ width: 900, height: 400 });
const wideA = await page.locator("#a").boundingBox();
const wideB = await page.locator("#b").boundingBox();
console.log("wide viewport: a.y", wideA.y, "b.y", wideB.y, "(equal means side-by-side)");
if (wideA.y !== wideB.y) throw new Error("expected side-by-side layout above the breakpoint");

await page.setViewportSize({ width: 400, height: 400 });
const narrowA = await page.locator("#a").boundingBox();
const narrowB = await page.locator("#b").boundingBox();
console.log("narrow viewport: a.y", narrowA.y, "b.y", narrowB.y, "(b below a means stacked)");
if (narrowB.y <= narrowA.y) throw new Error("expected stacked layout below the 600px breakpoint");
console.log("PASS: the media query stacked the columns once the viewport shrank below 600px");

await browser.close();
