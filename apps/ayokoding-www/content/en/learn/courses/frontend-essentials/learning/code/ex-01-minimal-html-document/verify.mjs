// ex-01: verify the minimal document renders and the tab shows the title (co-01).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const title = await page.title();
console.log("document.title:", title);
if (title !== "Example 1: Minimal HTML Document") {
  throw new Error("title did not match the <title> element's text");
}

const bodyText = await page.locator("body").innerText();
console.log("body renders text:", bodyText.length > 0);
if (bodyText.trim().length === 0) {
  throw new Error("body has no rendered text");
}

await browser.close();
console.log("PASS: document renders and tab title matches <title>");
