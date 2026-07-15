// ex-75: verify the fixed input now has a real accessible name, supplied by its label (co-24).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const accessible = page.getByRole("textbox", { name: "Search" });
const count = await accessible.count();
console.log("textbox with accessible name 'Search' found:", count);
if (count !== 1) {
  throw new Error("expected the labeled input to expose 'Search' as its accessible name");
}
console.log("PASS: adding label[for=search] gave the input a real accessible name");

await browser.close();
