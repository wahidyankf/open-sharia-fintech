// effect-dependency-track: independently runnable, strict TypeScript demonstration.
// => Run with npx tsx example.ts; every assertion is part of the example.

function assert(condition: boolean, message: string): void {
  // => A failed runtime contract must stop the lesson, not merely log a warning.
  if (!condition) throw new Error(message);
  // => PASS: the invariant remains true and execution continues.
}

type Effect = () => void;
// => Effects are callable subscribers; no framework-specific type is required.
let active: Effect | undefined;
// => The currently running effect receives subscriptions from signal reads.
function signal<T>(initial: T): { get value(): T; set value(next: T) } {
  // => A signal retains one stable container around a mutable value.
  let value = initial;
  // => The set stores computations that read this signal.
  const subscribers = new Set<Effect>();
  // => A set avoids registering the same effect more than once.
  return {
    get value(): T {
      if (active) subscribers.add(active);
      return value;
    },
    // => Reading during an effect links the active computation to this signal.
    set value(next: T) {
      if (!Object.is(value, next)) {
        value = next;
        subscribers.forEach((run) => run());
      }
    },
    // => A changed value synchronously triggers only its subscribers.
  };
}
const count = signal(0);
// => This primitive holds the UI's source state.
let runs = 0;
// => The counter makes dependency-triggered work observable.
const render = (): void => {
  count.value;
  runs += 1;
};
// => Reading count is the subscription; increment models a dependent render.
active = render;
render();
active = undefined;
// => Initial execution establishes the graph edge.
count.value = 1;
// => Setting count reaches only render through the recorded subscriber set.
assert(runs === 2 && count.value === 1, "signal should update its dependent effect");
// => PASS: one initial render plus exactly one reactive update occurred.
console.log("PASS: effect-dependency-track");
// => Output: PASS: effect-dependency-track
