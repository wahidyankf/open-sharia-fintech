import { z } from "zod";

// pathId is variable-depth by design (R2, R8): `careers/<arc>/<role>` (3 segments) or
// `skills/<subject>` (2 segments), and no depth beyond the category segment is ever fixed —
// a future `skills/<arc>/<subject>` (3 segments) or any deeper careers id must keep validating.
// The refine below therefore checks: the literal category segment, a minimum-arity floor (never
// a ceiling, never an equality) counted after empty tokens are dropped (so "careers/"
// ("careers", "") is rejected by the same floor as the bare "careers"), and — defense-in-depth
// for `manifests/README.md`'s documented segment-by-segment directory mapping
// (`careers/interview-ready/software-engineer` -> `manifests/careers/interview-ready/software-engineer.yaml`)
// — that no segment is a `.`/`..` traversal token and no raw backslash or null byte appears
// anywhere in the id, since either could otherwise walk that mapping outside `manifests/`.
const PATH_ID_CATEGORIES = ["careers", "skills"] as const;

const hasForbiddenCharacters = (pathId: string): boolean => pathId.includes("\\") || pathId.includes("\0");

const pathIdSchema = z.string().refine(
  (pathId) => {
    if (hasForbiddenCharacters(pathId)) {
      return false;
    }

    const segments = pathId.split("/").filter(Boolean);
    const [category] = segments;

    return (
      segments.length >= 2 &&
      (PATH_ID_CATEGORIES as readonly string[]).includes(category ?? "") &&
      segments.every((segment) => segment !== "." && segment !== "..")
    );
  },
  {
    message:
      "pathId must start with 'careers/' or 'skills/', carry at least one further non-empty segment, and contain no '.'/'..' traversal segments or backslash/null-byte characters",
  },
);

const courseFramingSchema = z.object({
  intro: z.string().optional(),
  outro: z.string().optional(),
});

const courseRefSchema = z.union([
  z.string(),
  z.object({
    id: z.string(),
    framing: courseFramingSchema.optional(),
  }),
]);

export const PathManifestSchema = z.object({
  pathId: pathIdSchema,
  // `arc` is required on every manifest regardless of category (R8) — for `skills/*` paths the
  // arc is omitted from the URL, but it is never optional in the manifest data.
  arc: z.string(),
  title: z.string(),
  description: z.string(),
  courseOrder: z.array(courseRefSchema),
});

export type PathManifest = z.infer<typeof PathManifestSchema>;
export type CourseRef = z.infer<typeof courseRefSchema>;
