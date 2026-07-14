// Example 56 (invalid): as const makes every property readonly, so assignment fails.
const cfg = { mode: "dark" } as const;

cfg.mode = "light"; // => TYPE ERROR: Cannot assign to 'mode' because it is a read-only property
console.log(cfg.mode);
