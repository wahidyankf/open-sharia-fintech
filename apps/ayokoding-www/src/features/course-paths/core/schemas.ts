import { z } from "zod";

// pathId is variable-depth by design (R2, R8): `careers/<arc>/<role>` (3 segments) or
// `skills/<subject>` (2 segments), and no depth beyond the category segment is ever fixed —
// a future `skills/<arc>/<subject>` (3 segments) or any deeper careers id must keep validating.
// The refine below therefore matches the WHOLE string against one anchored regex: a literal
// category segment (`careers`/`skills`) followed by one or more `/`-separated kebab-case segments
// (`[a-z0-9]+(-[a-z0-9]+)*` — lowercase alphanumerics joined by single hyphens, never empty, never
// leading/trailing a hyphen). Restricting to this charset is defense-in-depth for
// `manifests/README.md`'s documented segment-by-segment directory mapping
// (`careers/interview-ready/software-engineer` -> `manifests/careers/interview-ready/software-engineer.yaml`)
// AND closes two round-trip hazards a looser per-segment check missed (PR review finding #1/#2,
// `pr-review-synthesis-maker` review 4770318960, cycle 2):
// (1) `contentUrl` interpolates `pathId` into a `?path=` query string unencoded, so any character
//     outside this charset (`&`, `=`, `#`, `%`, whitespace, `.`/`..`, backslash, null byte) could
//     silently truncate or corrupt the query string on its `URLSearchParams` round-trip in
//     `parsePathContext`;
// (2) matching the ENTIRE string against one anchored pattern — rather than counting segments after
//     a `.split("/").filter(Boolean)` that drops empty tokens — rejects a trailing slash or a
//     doubled slash outright, instead of silently normalizing it into the same canonical id as its
//     clean form.
const PATH_ID_CATEGORIES = ["careers", "skills"] as const;
const KEBAB_SEGMENT = "[a-z0-9]+(?:-[a-z0-9]+)*";
const pathIdPattern = new RegExp(`^(?:${PATH_ID_CATEGORIES.join("|")})(?:/${KEBAB_SEGMENT}){1,}$`);

const pathIdSchema = z.string().refine((pathId) => pathIdPattern.test(pathId), {
  message:
    "pathId must start with 'careers/' or 'skills/', carry at least one further kebab-case segment " +
    "(lowercase alphanumerics and single internal hyphens only, no empty/trailing/doubled slash), " +
    "and contain no traversal, backslash, null-byte, or other non-kebab character",
});

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
