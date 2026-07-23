// ex-17: verify document.querySelector returns the matching element (co-12).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const text = await page.evaluate(() => {
  const el = document.querySelector(".title");
  return el ? el.textContent : null;
});
console.log("querySelector('.title').textContent:", text);
if (text !== "Dashboard") {
  throw new Error(`expected "Dashboard", got ${text}`);
}
console.log("PASS: querySelector('.title') returned the real, matching DOM element");

await browser.close();
