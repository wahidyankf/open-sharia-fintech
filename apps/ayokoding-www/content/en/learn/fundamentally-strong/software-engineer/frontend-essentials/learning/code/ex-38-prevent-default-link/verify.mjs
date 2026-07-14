// ex-38: verify preventDefault() on a link click stops the browser from navigating (co-16).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const urlBefore = page.url();
await page.locator("#link").click();
const urlAfter = page.url();
const report = await page.locator("#report").innerText();
console.log("url before:", urlBefore, "url after click:", urlAfter, "report:", report);
if (urlAfter !== urlBefore) {
  throw new Error("navigation occurred even though preventDefault() was called");
}
if (report !== "click handled, default prevented") {
  throw new Error("click handler did not run as expected");
}
console.log("PASS: preventDefault() suppressed the navigation; the page URL never changed");

await browser.close();
