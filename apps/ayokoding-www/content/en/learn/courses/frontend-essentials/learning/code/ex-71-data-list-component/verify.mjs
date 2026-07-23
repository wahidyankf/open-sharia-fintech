// ex-71: verify a single list component renders correctly across all four discriminated-union states (co-27, co-21).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const app = page.locator("#app");

// loading was already rendered on initial load
if ((await app.locator("#spinner").count()) !== 1) throw new Error("initial loading render missing");

await page.evaluate(() =>
  window.__DataList(document.getElementById("app"), { status: "error", message: "Network down" }),
);
const errorText = await app.locator("#error-message").innerText();

await page.evaluate(() => window.__DataList(document.getElementById("app"), { status: "empty" }));
const emptyCount = await app.locator("#empty-state").count();

await page.evaluate(() =>
  window.__DataList(document.getElementById("app"), { status: "loaded", items: ["Apple", "Banana"] }),
);
const loadedCount = await app.locator("#results li").count();

console.log("error text:", errorText, "empty count:", emptyCount, "loaded item count:", loadedCount);
if (errorText !== "Network down") throw new Error("error state did not render correctly");
if (emptyCount !== 1) throw new Error("empty state did not render correctly");
if (loadedCount !== 2) throw new Error("loaded state did not render the right item count");
console.log("PASS: the same component rendered loading, error, empty, and loaded states correctly");

await browser.close();
