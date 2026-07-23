// Example 70: Typed State -- tsc catches an invalid state assignment.
// => co-20: local state plus a typed shape is what makes state changes safe to reason about
interface CounterState {
  count: number; // => the component's state shape, count must stay a number
}

const state: CounterState = { count: 0 }; // => count is 0 (type: number)
// => this is the same kind of state object Example 45's counter mutates at runtime
state.count = "nope"; // => TYPE ERROR: a string is not assignable to a number-typed field
// => tsc catches this the moment it's written, long before any render() ever runs
