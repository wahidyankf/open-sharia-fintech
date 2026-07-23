// ex-64: verify arrow keys move both focus and the roving tabindex among menu items (co-26).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const startId = await page.evaluate(() => document.activeElement.id);
const startTabIndex = await page.locator("#item-0").getAttribute("tabindex");
await page.keyboard.press("ArrowRight");
const afterId = await page.evaluate(() => document.activeElement.id);
const item0Index = await page.locator("#item-0").getAttribute("tabindex");
const item1Index = await page.locator("#item-1").getAttribute("tabindex");
console.log("start focus:", startId, "tabindex:", startTabIndex);
console.log("after ArrowRight, focus:", afterId, "item-0 tabindex:", item0Index, "item-1 tabindex:", item1Index);

if (startId !== "item-0") throw new Error("menu should start focused on item-0");
if (afterId !== "item-1") throw new Error("ArrowRight should move focus to item-1");
if (item0Index !== "-1" || item1Index !== "0") {
  throw new Error("roving tabindex did not move from item-0 to item-1");
}
console.log("PASS: ArrowRight moved both DOM focus and the roving tabindex=0 to the next item");

await browser.close();
