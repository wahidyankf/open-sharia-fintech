// ex-56: verify clicking the associated label focuses its input (co-24).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.locator("label").click();
const focused = await page.evaluate(() => document.activeElement.id);
console.log("focused element id after clicking the label:", focused);
if (focused !== "username") {
  throw new Error(`expected clicking the label to focus #username, focus went to "${focused}"`);
}
console.log("PASS: label[for=username] correctly focused the #username input on click");

await browser.close();
