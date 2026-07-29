// Example 48: Accessible Form Validation via aria invalid and aria describedby. (co-26)
//
// An accessible error must be PROGRAMMATICALLY associated with its input: the input carries
// aria-invalid when it has an error, and aria-describedby points at the error text's id. A screen
// reader then announces "invalid, described by <error text>" -- the error is reachable, not just
// visible.

// A validated field: its value, validity, the associated error id, and the error text.
interface Field {
  // => the ARIA wiring is what ties the visible error text to the input programmatically
  inputId: string; // => the input's id
  value: string; // => the current value
  required: boolean; // => whether empty is an error
  errorId: string; // => the id aria-describedby points at
  errorText: string; // => the live error message ("" when valid)
}

// validate sets the error text and returns whether the field is valid.
function validate(field: Field): boolean {
  // => co-26: validation sets BOTH the message and the invalid flag together
  const valid = !field.required || field.value.trim().length > 0; // => required + empty => invalid
  field.errorText = valid ? "" : "This field is required"; // => the message shown AND announced
  return valid; // => drives aria-invalid below
}

// ariaState renders the exact ARIA attributes the input exposes.
function ariaState(field: Field): Record<string, string> {
  // => the contract: aria-invalid reflects validity, aria-describedby points at the error id
  const valid = field.errorText === "";
  return {
    "aria-invalid": String(!valid), // => true when there is an error
    "aria-describedby": field.errorId, // => points at the error text element
  };
}

const email: Field = { inputId: "email", value: "", required: true, errorId: "email-error", errorText: "" };
validate(email); // => empty + required => invalid
const aria = ariaState(email); // => the ARIA the input now exposes

console.log("aria-invalid:", aria["aria-invalid"]); // => Output: aria-invalid: true
console.log("aria-describedby:", aria["aria-describedby"]); // => Output: aria-describedby: email-error
console.log("associated error text:", email.errorText); // => Output: associated error text: This field is required
