// patch-text: independently runnable, strict TypeScript demonstration.
// => Run with npx tsx example.ts; every assertion is part of the example.

function assert(condition: boolean, message: string): void {
  // => A failed runtime contract must stop the lesson, not merely log a warning.
  if (!condition) throw new Error(message);
  // => PASS: the invariant remains true and execution continues.
}

type VNode = Readonly<{ type: string; props: Readonly<Record<string, string>>; children: readonly VNode[] }>;
// => A virtual node is data: renderers can inspect it before mutating a host.
const text = (value: string): VNode => ({ type: "#text", props: { value }, children: [] });
// => Text has its own discriminant, so element-only logic cannot use it accidentally.
const h = (type: string, props: Readonly<Record<string, string>>, children: readonly VNode[]): VNode => ({
  type,
  props,
  children,
});
// => Hyperscript builds a typed declarative tree without a browser framework.
const oldTree = h("button", { title: "old", key: "save" }, [text("Save")]);
// => The original tree supplies both stable identity and a previous description.
const nextTree = h("button", { title: "new", key: "save" }, [text("Saved")]);
// => Only text and one property differ; the element type and key remain stable.
const canReuse = oldTree.type === nextTree.type && oldTree.props.key === nextTree.props.key;
// => A minimal reconciler reuses same-type, same-key host nodes.
const changedProps = Object.keys(nextTree.props).filter((key) => oldTree.props[key] !== nextTree.props[key]);
// => Diffing identifies title; patching would mutate only that property.
assert(canReuse, "same type and key should preserve identity");
// => The keyed button is retained instead of replaced.
assert(changedProps.length === 1 && changedProps[0] === "title", "diff should be minimal");
// => The change set names exactly the mutated property.
console.log("PASS: patch-text");
// => Output: PASS: patch-text
