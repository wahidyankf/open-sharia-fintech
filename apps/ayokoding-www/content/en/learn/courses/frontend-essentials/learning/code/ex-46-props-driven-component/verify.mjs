// ex-46: verify Greeting(props) yields different output for different props (co-19).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const a = await page.locator("#a").innerText();
const b = await page.locator("#b").innerText();
console.log("a:", a, "b:", b);
if (a !== "Hello, Ada!") throw new Error(`unexpected a: "${a}"`);
if (b !== "Hello, Grace!") throw new Error(`unexpected b: "${b}"`);
if (a === b) throw new Error("different props should not produce identical output");
console.log("PASS: the same Greeting function produced different output for different props");

await browser.close();
