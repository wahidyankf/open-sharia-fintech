// ex-73: verify only items matching the controlled search input remain rendered (co-21, co-22).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const initialCount = await page.locator("#list li").count();
console.log("initial rendered items:", initialCount);
if (initialCount !== 5) throw new Error("expected all 5 items rendered initially");

await page.locator("#search").fill("ap");
const filtered = await page.locator("#list li").allInnerTexts();
console.log("items matching 'ap':", JSON.stringify(filtered));
if (JSON.stringify(filtered.sort()) !== JSON.stringify(["Apple", "Apricot"].sort())) {
  throw new Error(`unexpected filtered items: ${JSON.stringify(filtered)}`);
}
console.log("PASS: the rendered list narrowed to exactly the items matching the search input");

await browser.close();
