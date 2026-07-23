// ex-67: verify a zero-length result renders the 'empty' branch's empty-state view (co-27).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const emptyCount = await page.locator("#empty-state").count();
const emptyText = await page.locator("#empty-state").innerText();
console.log("empty-state present:", emptyCount === 1, "text:", emptyText);
if (emptyCount !== 1) throw new Error("expected the empty branch to render #empty-state");
if (emptyText !== "No results") throw new Error(`unexpected empty-state text: "${emptyText}"`);
console.log("PASS: state.status === 'empty' rendered exactly the empty-state branch");

await browser.close();
