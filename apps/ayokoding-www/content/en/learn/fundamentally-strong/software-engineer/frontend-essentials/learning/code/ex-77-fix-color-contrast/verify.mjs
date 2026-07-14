// ex-77: verify the raised text/background contrast ratio meets WCAG AA's >= 4.5:1 (co-25, co-05).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

function relativeLuminance([r, g, b]) {
  const toLinear = (channel) => {
    const c = channel / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  };
  const [rl, gl, bl] = [r, g, b].map(toLinear);
  return 0.2126 * rl + 0.7152 * gl + 0.0722 * bl;
}
function parseRgb(str) {
  const match = str.match(/\d+/g).map(Number);
  return match;
}

const [color, background] = await page.locator("#notice").evaluate((el) => {
  const style = getComputedStyle(el);
  return [style.color, style.backgroundColor];
});
console.log("computed color:", color, "computed background:", background);

const l1 = relativeLuminance(parseRgb(color));
const l2 = relativeLuminance(parseRgb(background));
const lighter = Math.max(l1, l2);
const darker = Math.min(l1, l2);
const ratio = (lighter + 0.05) / (darker + 0.05);
console.log("contrast ratio:", ratio.toFixed(2));

if (ratio < 4.5) {
  throw new Error(`contrast ratio ${ratio.toFixed(2)}:1 is below the WCAG AA 4.5:1 minimum`);
}
console.log(`PASS: the fixed text/background contrast ratio (${ratio.toFixed(2)}:1) meets WCAG AA`);

await browser.close();
