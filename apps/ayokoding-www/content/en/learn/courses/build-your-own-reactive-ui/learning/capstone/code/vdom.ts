// Typed virtual-DOM capstone runtime: keyed nodes retain their object identity.
export type VNode = Readonly<{ key: string; text: string }>;

export function renderTasks(tasks: readonly string[], count: number): readonly VNode[] {
  return [{ key: "count", text: "Count: " + count }, ...tasks.map((task) => ({ key: "task:" + task, text: task }))];
}

export function patchByKey(previous: readonly VNode[], next: readonly VNode[]): readonly VNode[] {
  const previousByKey = new Map(previous.map((node) => [node.key, node]));
  return next.map((node) => {
    const oldNode = previousByKey.get(node.key);
    return oldNode?.text === node.text ? oldNode : node;
  });
}
