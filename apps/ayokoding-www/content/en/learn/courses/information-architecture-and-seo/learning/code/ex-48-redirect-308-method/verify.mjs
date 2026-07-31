import assert from "node:assert/strict";

const redirect = new Response(null, {
  status: 308,
  headers: { location: "https://example.test/api/v2/orders" },
});

const original = new Request("https://example.test/api/v1/orders", {
  method: "POST",
  body: "order=42",
});
const redirected = new Request(redirect.headers.get("location"), {
  method: original.method,
  body: "order=42",
});

assert.equal(redirect.status, 308);
assert.equal(redirected.method, "POST");
console.log("308 preserves POST method in the modeled redirect request.");
