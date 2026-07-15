// ex-36: verify a parent listener sees a click that originated on its child (co-15).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.locator("#child").click();
const report = await page.locator("#report").innerText();
console.log("report:", report);
if (report !== "parent saw it") {
  throw new Error(`expected the parent's listener to fire, got "${report}"`);
}
console.log("PASS: the click on #child bubbled up and the #parent listener saw it");

await browser.close();
