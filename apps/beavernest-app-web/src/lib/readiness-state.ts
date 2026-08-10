import type { ReadinessResponse } from "./readiness-client";

export type ReadinessState =
  | { readonly kind: "loading" }
  | { readonly kind: "ready"; readonly response: ReadinessResponse }
  | { readonly kind: "unavailable" };

export type ReadinessAction =
  | { readonly type: "request" }
  | { readonly type: "resolved"; readonly response: ReadinessResponse }
  | { readonly type: "failed" };

export const initialReadinessState: ReadinessState = { kind: "loading" };

export function reduceReadiness(_state: ReadinessState, action: ReadinessAction): ReadinessState {
  switch (action.type) {
    case "request":
      return initialReadinessState;
    case "resolved":
      return action.response.status === "ready"
        ? { kind: "ready", response: action.response }
        : { kind: "unavailable" };
    case "failed":
      return { kind: "unavailable" };
  }
}
