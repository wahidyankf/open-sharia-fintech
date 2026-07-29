// broken.ts: the REQUIRED `label` prop is omitted -> a compile-time type error.
// This is exactly what precise required-prop typing buys you: the mistake is caught at compile
// time, not as a runtime "undefined" in the rendered button.
interface ButtonProps {
  label: string; // => REQUIRED
  disabled?: boolean;
  type?: "button" | "submit";
}

function renderButton(props: ButtonProps): string {
  const disabled = props.disabled ?? false;
  const type = props.type ?? "button";
  return `<button disabled="${disabled}" type="${type}">${props.label}</button>`;
}

// => TYPE ERROR: Property 'label' is missing (it is required, not optional)
const broken = renderButton({ type: "submit" }); // => error TS2741: Property 'label' is missing

console.log(broken);
