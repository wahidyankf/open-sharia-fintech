// Example 77: A user-event Interaction Test. (co-36)
//
// user-event drives a REALISTIC interaction sequence (type into an input, click a button) and then
// asserts the resulting UI -- the closest a unit test gets to a real user. This example models a
// type-then-submit flow and asserts the rendered result reflects the user's actions.

// A tiny form component: an input whose value lives in state, and a submit handler.
function makeForm(): {
  // => the component exposes the behaviour a user drives, not its internals
  input: { value: string };
  submitted: string | null;
  type: (text: string) => void; // => user-event.type
  clickSubmit: () => void; // => user-event.click
} {
  const state = { input: { value: "" }, submitted: null as string | null };
  return {
    input: state.input,
    submitted: null,
    type(text: string) {
      // => user-event.type fills the input char by char (a real keystroke sequence)
      state.input.value = text; // => the controlled input updates state
      this.submitted = state.submitted; // => keep the alias current
    },
    clickSubmit() {
      // => user-event.click activates the submit control
      state.submitted = state.input.value; // => the handler reads the current value
      this.submitted = state.submitted;
    },
  };
}

// assertEqual is a tiny assertion helper (stands in for vitest's expect).
function assertEqual<T>(actual: T, expected: T, label: string): void {
  // => a passing assertion prints OK; a mismatch would throw (the test fails)
  const ok = actual === expected;
  console.log(`${ok ? "PASS" : "FAIL"}: ${label}`);
  if (!ok) throw new Error(`expected ${String(expected)}, got ${String(actual)}`);
}

const form = makeForm(); // => mount the component
form.type("buy bread"); // => user-event.type: a realistic keystroke sequence
form.clickSubmit(); // => user-event.click: activate submit

assertEqual(form.submitted, "buy bread", "submit reflects what the user typed"); // => Output: PASS
