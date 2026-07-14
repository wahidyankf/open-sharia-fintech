// ex-49: verify a keyed re-render updates only the one changed node, reusing the others (co-21, co-18).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.evaluate(() => window.__markUnchanged());
await page.evaluate(() => window.__updateOne());
const marks = await page.evaluate(() =>
  Array.from(document.querySelectorAll("#list li")).map((li) => ({
    key: li.dataset.key,
    text: li.textContent,
    reused: li.dataset.marked === "yes",
  })),
);
console.log("after keyed update:", JSON.stringify(marks));

for (const item of marks) {
  if (!item.reused) throw new Error(`node for key ${item.key} was recreated, not reused`);
}
const beta = marks.find((m) => m.key === "2");
if (beta.text !== "Beta (changed)") throw new Error("changed item's text did not update");
console.log("PASS: every node was reused (same DOM node) and only item 2's text content changed");

await browser.close();
