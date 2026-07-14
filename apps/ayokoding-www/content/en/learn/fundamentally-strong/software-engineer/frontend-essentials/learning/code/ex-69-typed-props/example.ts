// Example 69: Typed Props -- tsc rejects a prop of the wrong type.
// => a Props interface is a component's typed input contract, checked at every call site
interface GreetingProps {
  name: string; // => must be a string
  count: number; // => must be a number
}

function Greeting(props: GreetingProps): string {
  // => props is fully typed here; props.count is KNOWN to be number, not just assumed
  return "Hello, " + props.name + "! (" + props.count + ")";
  // => co-19: a component is just a function of its typed props, nothing more
}

Greeting({ name: "Ada", count: "3" }); // => TYPE ERROR: count expects number, "3" is a string
// => "3" looks like a number but is a real string -- exactly the kind of value form input sends
