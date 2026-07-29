// Example 35: A Redux Toolkit Slice for Large Shared State. (co-16)
//
// Reach for a global store (Redux Toolkit-style) only when state is LARGE, frequently updated, and
// shared across many components. A slice bundles the state for one domain plus the reducers that
// update it; selectors read derived values without re-running when unrelated state changes.

// A counter slice: state plus reducers plus selectors (the createSlice shape, modeled).
interface CounterState {
  // => the slice owns ONE piece of the global state tree
  value: number; // => the counter value
}

// Actions are discriminated by their `type` string; the reducer narrows on it.
type Action = { type: "counter/increment" } | { type: "counter/setValue"; payload: number };
// => the union + literal `type` is the classic Redux action shape (a discriminated union, co-33)

// reducer is a pure function: (state, action) -> newState. It NEVER mutates in place.
function reducer(state: CounterState, action: Action): CounterState {
  // => co-16: reducers are pure; immutability is what lets subscribers detect changes
  switch (action.type) {
    case "counter/increment":
      return { value: state.value + 1 }; // => new object, not a mutation
    case "counter/setValue":
      return { value: action.payload }; // => new object carrying the new value
  }
}

// selectValue reads a derived value out of the slice (a selector).
function selectValue(state: CounterState): number {
  // => selectors keep the read logic in one place; memoized selectors are Example 36
  return state.value; // => the projected value components subscribe to
}

let store: CounterState = { value: 0 }; // => the initial global state
store = reducer(store, { type: "counter/increment" }); // => dispatch increment
store = reducer(store, { type: "counter/setValue", payload: 42 }); // => dispatch setValue

console.log("selected value:", selectValue(store)); // => Output: selected value: 42
