// ex-25: verify event.target identifies exactly the clicked element (co-14).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.locator("#b").click();
const report = await page.locator("#report").innerText();
console.log("reported clicked id:", report);
if (report !== "b") {
  throw new Error(`expected event.target to identify "b", got "${report}"`);
}
console.log("PASS: event.target correctly identified button b as the clicked element");

await browser.close();
