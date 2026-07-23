// ex-22: verify el.remove() means querySelector no longer finds it (co-13).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const before = await page.evaluate(() => document.querySelector("#notice") !== null);
const after = await page.evaluate(() => {
  document.getElementById("notice").remove();
  return document.querySelector("#notice") !== null;
});
console.log("#notice found before remove():", before, "found after remove():", after);
if (!before) throw new Error("#notice should exist before remove()");
if (after) throw new Error("#notice should no longer be found after remove()");
console.log("PASS: el.remove() took the element out of the DOM entirely");

await browser.close();
