// Kata 7 (before): `import type` erases ApiError from the compiled output --
// using it as a runtime value (`new ApiError(...)`) fails to compile.
import type { ApiError } from "./types";

function fail(): never {
  throw new ApiError(404, "not found");
}

fail();
