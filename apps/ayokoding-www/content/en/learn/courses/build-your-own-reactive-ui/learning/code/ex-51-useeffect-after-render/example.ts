// useeffect-after-render: independently runnable, strict TypeScript demonstration.
// => Run with npx tsx example.ts; every assertion is part of the example.

function assert(condition: boolean, message: string): void {
  // => A failed runtime contract must stop the lesson, not merely log a warning.
  if (!condition) throw new Error(message);
  // => PASS: the invariant remains true and execution continues.
}

const slots: unknown[] = [];
// => A tiny hook runtime keeps local state in render-order slots.
let cursor = 0;
// => Every render rewinds the cursor before calling the component.
function useState<T>(initial: T): readonly [T, (next: T) => void] {
  // => The current cursor selects this call's stable state location.
  const index = cursor++;
  // => Unconditional call order is therefore a correctness requirement.
  if (slots[index] === undefined) slots[index] = initial;
  // => First render allocates the slot; later renders retain it.
  return [
    slots[index] as T,
    (next: T): void => {
      slots[index] = next;
    },
  ];
  // => Setter updates the same slot rather than capturing a stale local value.
}
function Counter(): string {
  // => A function component returns a view derived from its local state.
  const [count, setCount] = useState(0);
  // => First hook occupies slot zero on every valid render.
  setCount(count + 1);
  // => This example schedules the next state value in that stable slot.
  return "count=" + count;
  // => The current render uses its snapshot, not the just-scheduled value.
}
cursor = 0;
const first = Counter();
// => First render allocates slot zero and shows the initial value.
cursor = 0;
const second = Counter();
// => Rewinding gives the hook the same slot on the next render.
assert(first === "count=0" && second === "count=1", "state must follow call order");
// => PASS: local state persists because hook order is stable.
console.log("PASS: useeffect-after-render");
// => Output: PASS: useeffect-after-render
