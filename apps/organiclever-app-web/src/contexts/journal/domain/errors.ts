import { Data } from "effect";
import { StorageUnavailable, NotFound } from "@/shared/runtime";

// `StorageUnavailable` and `NotFound` are the cross-context storage errors;
// the canonical owner is `@/shared/runtime`. Re-exported here so callers
// importing `@/contexts/journal/domain` continue to resolve the same
// constructor. New cross-context callers should consume `@/shared/runtime`
// directly.
export { StorageUnavailable, NotFound };

export class EmptyBatch extends Data.TaggedError("EmptyBatch")<{}> {}

export type StoreError = StorageUnavailable | EmptyBatch;
