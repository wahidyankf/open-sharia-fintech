// ex-21: verify createElement + append grows the list by exactly one item (co-13).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const before = await page.evaluate(() => document.querySelectorAll("#list li").length);
const after = await page.evaluate(() => {
  const li = document.createElement("li");
  li.textContent = "Second";
  document.getElementById("list").append(li);
  return document.querySelectorAll("#list li").length;
});
console.log("items before:", before, "items after append:", after);
if (after !== before + 1) {
  throw new Error(`expected ${before + 1} items after append, got ${after}`);
}
console.log("PASS: createElement + append grew the list by exactly one item");

await browser.close();
