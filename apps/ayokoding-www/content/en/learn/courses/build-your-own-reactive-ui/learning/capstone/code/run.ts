import { effect, signal } from "./signals";
import { patchByKey, renderTasks } from "./vdom";

const tasks = ["Learn", "Measure"] as const;
const first = renderTasks(tasks, 0);
const second = patchByKey(first, renderTasks(tasks, 1));
if (second[1] !== first[1] || second[2] !== first[2]) throw new Error("keyed nodes were recreated");
if (second[0] === first[0]) throw new Error("changed counter was not patched");

const count = signal(0);
const taskCount = signal(tasks.length);
let countRuns = 0;
let taskRuns = 0;
effect(() => {
  count.value;
  countRuns += 1;
});
effect(() => {
  taskCount.value;
  taskRuns += 1;
});
count.value = 1;
if (countRuns !== 2 || taskRuns !== 1) throw new Error("update was not fine-grained");
console.log("PASS: VDOM keyed identity preserved");
console.log("PASS: signals re-ran only the counter effect");
console.log("work: vdom renders=2, signal counter effects=2, signal task effects=1");
