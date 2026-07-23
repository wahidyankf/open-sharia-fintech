// ex-20: verify classList.toggle('active') adds the class, then removes it on a second call (co-13).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const afterFirst = await page.locator("#panel").evaluate((el) => {
  el.classList.toggle("active");
  return el.classList.contains("active");
});
const afterSecond = await page.locator("#panel").evaluate((el) => {
  el.classList.toggle("active");
  return el.classList.contains("active");
});
console.log("has 'active' after first toggle:", afterFirst);
console.log("has 'active' after second toggle:", afterSecond);

if (afterFirst !== true) throw new Error("first toggle should add the class");
if (afterSecond !== false) throw new Error("second toggle should remove the class");
console.log("PASS: classList.toggle added the class, then removed it on the next call");

await browser.close();
