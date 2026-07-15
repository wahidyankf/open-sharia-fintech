// ex-31: verify each element occupies its named grid-template-areas region (co-10).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const header = await page.locator("#header").boundingBox();
const sidebar = await page.locator("#sidebar").boundingBox();
const content = await page.locator("#content").boundingBox();
console.log(
  "header:",
  JSON.stringify(header),
  "sidebar:",
  JSON.stringify(sidebar),
  "content:",
  JSON.stringify(content),
);

if (header.width !== 400) throw new Error("header should span both columns (400px)");
if (sidebar.x !== 0 || Math.abs(sidebar.width - 100) > 1)
  throw new Error("sidebar should occupy the left 100px column");
if (Math.abs(content.x - 100) > 1 || Math.abs(content.width - 300) > 1)
  throw new Error("content should occupy the right 300px column");
if (sidebar.y !== content.y) throw new Error("sidebar and content should share the second row");
console.log("PASS: header/sidebar/content each landed in their named grid-template-areas region");

await browser.close();
