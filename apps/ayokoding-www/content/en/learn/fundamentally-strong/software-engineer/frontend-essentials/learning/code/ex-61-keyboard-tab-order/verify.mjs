// ex-61: verify Tab moves focus through the form in the natural, logical DOM order (co-26).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.locator("#first-name").focus();
const order = [await page.evaluate(() => document.activeElement.id)];
for (let i = 0; i < 2; i++) {
  await page.keyboard.press("Tab");
  order.push(await page.evaluate(() => document.activeElement.id));
}
console.log("tab order:", JSON.stringify(order));
if (JSON.stringify(order) !== JSON.stringify(["first-name", "last-name", "submit-btn"])) {
  throw new Error(`unexpected tab order: ${JSON.stringify(order)}`);
}
console.log("PASS: pressing Tab moved focus through the form in the expected logical sequence");

await browser.close();
