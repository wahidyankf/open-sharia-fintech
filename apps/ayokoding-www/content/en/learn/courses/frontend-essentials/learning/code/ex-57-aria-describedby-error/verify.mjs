// ex-57: verify the accessible description exposed to assistive tech includes the error text (co-24, co-25).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const description = await page.locator("#age").evaluate((el) => {
  const id = el.getAttribute("aria-describedby");
  return document.getElementById(id).textContent;
});
console.log("accessible description text:", description);
if (description !== "Enter a whole number of years") {
  throw new Error(`unexpected description: "${description}"`);
}
console.log("PASS: aria-describedby wired the error paragraph in as the input's accessible description");

await browser.close();
