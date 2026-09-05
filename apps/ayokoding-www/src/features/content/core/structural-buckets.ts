export interface ContentTreeEntry {
  name: string;
  kind: "directory" | "file";
}

/** Returns the stable, sorted set of structural directories in one content-tree level. */
export function structuralBuckets(entries: readonly ContentTreeEntry[]): string[] {
  return entries
    .filter((entry) => entry.kind === "directory")
    .map((entry) => entry.name)
    .toSorted();
}
