// ex-48: verify the rendered <li> count equals the source array's length (co-21).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const count = await page.evaluate(() => document.querySelectorAll("#list li").length);
console.log("rendered <li> count:", count);
if (count !== 5) throw new Error(`expected 5 rendered items, got ${count}`);
console.log("PASS: mapping the 5-item array produced exactly 5 rendered <li> elements");

await browser.close();
