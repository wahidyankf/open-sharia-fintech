// ex-59: verify the accessibility tree exposes the button role on the div (co-25).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const count = await page.getByRole("button", { name: "Do the thing" }).count();
console.log("elements exposing the button role:", count);
if (count !== 1) {
  throw new Error(`expected exactly one button-role element, found ${count}`);
}
console.log('PASS: role="button" exposed the <div> as a real button in the accessibility tree');

await browser.close();
