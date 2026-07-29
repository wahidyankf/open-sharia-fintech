// Example 69: Precise Required and Optional Prop Typing. (co-33)
//
// Precise prop typing marks which props are required and which are optional (`?`). A missing
// required prop is a COMPILE error, not a runtime undefined; an optional prop has an explicit type
// plus a sensible default. The "broken" variant below shows the missing-required-prop error.

// Button props: `label` is required; `disabled` and `type` are optional with defaults.
interface ButtonProps {
  // => required props have no `?`; optional props do, and callers may omit them
  label: string; // => REQUIRED -- callers must supply it
  disabled?: boolean; // => optional (defaults to false below)
  type?: "button" | "submit"; // => optional, a literal union (defaults to "button")
}

// renderButton applies defaults for the optional props.
function renderButton(props: ButtonProps): string {
  // => co-33: optional props arrive as T | undefined; defaults fill them in
  const disabled = props.disabled ?? false; // => default false when omitted
  const type = props.type ?? "button"; // => default "button" when omitted
  return `<button disabled="${disabled}" type="${type}">${props.label}</button>`;
  // => props.label is always present (it is required), so no default needed
}

const ok = renderButton({ label: "Save", type: "submit" }); // => valid: label required, type optional
const minimal = renderButton({ label: "Cancel" }); // => valid: only the required prop given

console.log(ok); // => Output: <button disabled="false" type="submit">Save</button>
console.log(minimal); // => Output: <button disabled="false" type="button">Cancel</button>
