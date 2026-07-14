// Kata 7 (after): a regular (runtime) import -- ApiError survives into the compiled output.
import { ApiError } from "./types";

function fail(): never {
  throw new ApiError(404, "not found");
}

try {
  fail();
} catch (err) {
  if (err instanceof ApiError) {
    console.log(`${err.statusCode}: ${err.message}`);
  }
}
