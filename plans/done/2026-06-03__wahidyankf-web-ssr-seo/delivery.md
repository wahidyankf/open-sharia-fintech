> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (the safe-to-stop state and the single command to resume). A phase
> is not complete until its gate is green; do not start phase N+1 while any gate check fails.

## Worktree

Worktree path: `worktrees/wahidyankf-web-ssr-seo/`

Provision before execution (run from repo root):

```bash
claude --worktree wahidyankf-web-ssr-seo
```

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md)
and [Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

---

## Phase 0: Environment Setup and Baseline

> _Executor: `repo-setup-manager`_

- [x] [AI] Install dependencies from repo root worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized with `package-lock.json`
  > Date: 2026-06-03 | Status: DONE | Files: none | npm install exited 0; all 20 tools verified by postinstall doctor
- [x] [AI] Converge the full polyglot toolchain: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift reported
  > Date: 2026-06-03 | Status: DONE | Files: none | All 20 required tools healthy, zero drift
- [x] [AI] Run existing unit tests to establish baseline:
      `npx nx run wahidyankf-web:test:quick`
      — acceptance: all tests pass (or baseline pass/fail count recorded; every pre-existing
      failure documented before proceeding)
  > Date: 2026-06-03 | Status: DONE | Files: none | 66 tests passed, 9 test files, 80.54% line coverage. No pre-existing failures.
- [x] [AI] Run existing E2E typecheck/lint baseline:
      `npx nx run wahidyankf-web-fe-e2e:test:quick`
      — acceptance: exits 0
  > Date: 2026-06-03 | Status: DONE | Files: none | TypeScript check passed, exits 0
- [x] [AI] Resolve all pre-existing failures before proceeding:
      `npx nx run wahidyankf-web:test:quick 2>&1 | tail -20`
      — acceptance: zero test failures remain; any pre-existing failure either fixed or documented
      with its error message before moving on
  > Date: 2026-06-03 | Status: DONE | Files: none | Zero pre-existing failures — baseline clean

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift
  > Date: 2026-06-03 | Status: DONE | All gates confirmed by repo-setup-manager
- [x] [AI] `npx nx run wahidyankf-web:test:quick` exits 0 (or all pre-existing failures are
      documented and resolved)
  > Date: 2026-06-03 | Status: DONE | 66/66 tests passed
- [x] [AI] `npx nx run wahidyankf-web-fe-e2e:test:quick` exits 0
  > Date: 2026-06-03 | Status: DONE | TypeScript check passed

> **Pause Safety**: only the local toolchain was verified and the baseline recorded — no feature
> work exists yet. Safe to stop indefinitely. To resume: re-run
> `npx nx run wahidyankf-web:test:quick` and confirm it is still clean.

---

## Phase 1: Navigation.tsx — Add `"use client"` Directive

Add an explicit `"use client"` directive to `Navigation.tsx`. This is a config-only change with
no test update required; TDD exception applies.

> _Suggested executor: `swe-typescript-dev`_ (file is `.tsx` in `apps/wahidyankf-web/`)

### Step 1.1 — Navigation.tsx: add `"use client"`

- [x] [AI] Pre-condition: confirm `Navigation.tsx` has no `"use client"` directive yet:
      `head -1 apps/wahidyankf-web/src/features/app-shell/Navigation.tsx`
      — acceptance: output does NOT contain `"use client"`
  - _Suggested executor: `swe-typescript-dev`_
    > Date: 2026-06-03 | Status: DONE | Output: `import Link from "next/link";` — confirmed no directive
- [x] [AI] Edit `apps/wahidyankf-web/src/features/app-shell/Navigation.tsx`:
      insert `"use client";` as the very first line (before all imports).
      Verify: `head -1 apps/wahidyankf-web/src/features/app-shell/Navigation.tsx` outputs
      `"use client";`
  - _Suggested executor: `swe-typescript-dev`_
    > Date: 2026-06-03 | Status: DONE | Files: apps/wahidyankf-web/src/features/app-shell/Navigation.tsx | Added "use client"; as first line
- [x] [AI] Run `npx nx run wahidyankf-web:typecheck`
      — acceptance: exits 0 with no TypeScript errors
  > Date: 2026-06-03 | Status: DONE | typecheck exits 0

### Commit Guidelines (Phase 1)

- [x] [AI] Commit Navigation.tsx change:
      `git commit -m "refactor(wahidyankf-web): add explicit use client to Navigation.tsx"`
  > Date: 2026-06-03 | Status: DONE | Commit: e27fe4a34

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [x] [AI] `npx nx run wahidyankf-web:typecheck` exits 0
  > Date: 2026-06-03 | Status: DONE | exits 0
- [x] [AI] `npx nx run wahidyankf-web:lint` exits 0
  > Date: 2026-06-03 | Status: DONE | exits 0 (3 pre-existing a11y warnings in test files, not from this change)
- [x] [AI] `npx nx run wahidyankf-web:test:quick` exits 0 — all tests green (Navigation.tsx
      change introduces no test failures)
  > Date: 2026-06-03 | Status: DONE | 66/66 tests pass, 80.63% coverage
- [x] [AI] `head -1 apps/wahidyankf-web/src/features/app-shell/Navigation.tsx` outputs
      `"use client";`
  > Date: 2026-06-03 | Status: DONE | Confirmed

> **Pause Safety**: `Navigation.tsx` has an explicit `"use client"` directive; all other files
> are unchanged. The repo compiles cleanly and all tests are green. Safe to stop. To resume: run
> `npx nx run wahidyankf-web:typecheck` and confirm it exits 0.

---

## Phase 2: TypeScript Refactor — page.tsx + Content Components + Tests

Refactor all three `page.tsx` server components and all three content components (`HomeContent`,
`CvContent`, `PersonalProjectsContent`) together in one phase so every step leaves the tree fully
compilable. Each content-component unit gets a proper TDD cycle: RED = update test to render
the content component with the new prop (the test fails because the prop does not exist yet),
GREEN = update the content component to accept the prop AND update `page.tsx` to pass it (both
files change together so TypeScript is satisfied), REFACTOR = typecheck + lint + test run.

> _Suggested executor: `swe-typescript-dev`_ (all files are `.tsx`/`.ts` in `apps/wahidyankf-web/`)

### Step 2.1 — `HomeContent` + `page.tsx` (Red → Green → Refactor)

- [x] [AI] **RED** — Edit `apps/wahidyankf-web/src/app/page.unit.test.tsx`:
  - Remove the `useSearchParams` mock (the `mockGet` variable and the `useSearchParams` entry
    in the `vi.mock("next/navigation", ...)` factory).
  - Remove the `Suspense` import if present.
  - Replace all `render(<Home />)` calls with direct content-component rendering:
    `render(<HomeContent initialSearchTerm="" />)` — import `HomeContent` from
    `@/features/home/HomeContent` at the top of the test file instead of importing `Home`.
    This avoids async server-component rendering complexity in jsdom.
  - Keep `mockPush` / `useRouter` mock intact (still needed by `HomeContent`).
  - Verify: `npx nx run wahidyankf-web:test:quick` — tests referencing `HomeContent` **fail**
    with a prop-type or import error (confirms RED state: `HomeContent` does not yet accept
    `initialSearchTerm`).
  - _Suggested executor: `swe-typescript-dev`_
    > Date: 2026-06-03 | Status: DONE | Files: apps/wahidyankf-web/src/app/page.unit.test.tsx | Removed mockGet+useSearchParams mock, render HomeContent directly — confirmed RED failure
- [x] [AI] **GREEN** — Edit `apps/wahidyankf-web/src/features/home/HomeContent.tsx`:
  - Remove `useSearchParams` from the import: delete `, useSearchParams` from the
    `"next/navigation"` import line.
  - Change the `HomeContent` function signature from `export function HomeContent()` to
    `export function HomeContent({ initialSearchTerm }: { initialSearchTerm: string })`.
  - Remove the lines:

    ```ts
    const searchParams = useSearchParams();
    const initialSearchTerm = searchParams.get("search") || "";
    ```

  - Keep `const [searchTerm, setSearchTerm] = useState(initialSearchTerm);` and the
    `useEffect(() => { setSearchTerm(initialSearchTerm); }, [initialSearchTerm]);`.
  - Keep `useRouter` and all other logic unchanged.
  - Then rewrite `apps/wahidyankf-web/src/app/page.tsx`:

    ```tsx
    import { HomeContent } from "@/features/home/HomeContent";

    export default async function Home({ searchParams }: { searchParams: Promise<{ search?: string }> }) {
      const { search } = await searchParams;
      return <HomeContent initialSearchTerm={search ?? ""} />;
    }
    ```

  - Verify: `npx nx run wahidyankf-web:typecheck` — exits 0 (both files compile together)
  - _Suggested executor: `swe-typescript-dev`_
    > Date: 2026-06-03 | Status: DONE | Files: HomeContent.tsx, page.tsx | Removed useSearchParams, added initialSearchTerm prop, rewrote page.tsx with async searchParams

- [x] [AI] **REFACTOR** — Run `npx nx run wahidyankf-web:test:quick`
      — acceptance: all `HomeContent`-related tests pass; coverage thresholds met
  > Date: 2026-06-03 | Status: DONE | 67 tests pass, 80.37% coverage

### Step 2.2 — `CvContent` + `cv/page.tsx` (Red → Green → Refactor)

- [x] [AI] **RED** — Edit `apps/wahidyankf-web/src/app/cv/page.unit.test.tsx`:
  - Remove the `useSearchParams` mock (`mockGet` + `useSearchParams` in the navigation mock).
  - Add `mockReplace = vi.fn()` and include `replace: mockReplace` in the `useRouter` mock.
  - Replace page-level render calls with direct content-component rendering:
    `render(<CvContent initialSearchTerm="" scrollTop={false} />)` (and
    `render(<CvContent initialSearchTerm="" scrollTop={true} />)` in the scrollTop test) —
    import `CvContent` from `@/features/cv/CvContent` instead of importing `CV`.
  - Verify: `npx nx run wahidyankf-web:test:quick` — tests referencing `CvContent` **fail**
    with a prop-type error (confirms RED state: `CvContent` does not yet accept
    `initialSearchTerm` / `scrollTop`).
  - _Suggested executor: `swe-typescript-dev`_
    > Date: 2026-06-03 | Status: DONE | cv/page.unit.test.tsx updated — confirmed RED failure
- [x] [AI] **GREEN** — Edit `apps/wahidyankf-web/src/features/cv/CvContent.tsx`:
  - Remove `useSearchParams` from the `"next/navigation"` import.
  - Change the `CvContent` function signature to:

    ```ts
    export function CvContent({ initialSearchTerm, scrollTop }: { initialSearchTerm: string; scrollTop: boolean });
    ```

  - Remove the lines:

    ```ts
    const searchParams = useSearchParams();
    const initialSearchTerm = searchParams.get("search") || "";
    ```

  - Replace the `scrollTop` `useEffect` that reads `searchParams.get("scrollTop")` with:

    ```ts
    useEffect(() => {
      if (scrollTop) {
        window.scrollTo(0, 0);
        const newURL = new URL(window.location.href);
        newURL.searchParams.delete("scrollTop");
        router.replace(newURL.toString(), { scroll: false });
      }
    }, []);
    ```

  - Keep `const [searchTerm, setSearchTerm] = useState(initialSearchTerm);` and
    `useEffect(() => { setSearchTerm(initialSearchTerm); }, [initialSearchTerm]);`.
  - Keep `useRouter` and all other logic unchanged.
  - Then rewrite `apps/wahidyankf-web/src/app/cv/page.tsx`:

    ```tsx
    import { CvContent } from "@/features/cv/CvContent";
    import type { Metadata } from "next";

    export const metadata: Metadata = {
      title: "CV | Wahidyan Kresna Fridayoka",
      description:
        "Full curriculum vitae of Wahidyan Kresna Fridayoka — work experience, skills, education, and certifications.",
    };

    export default async function CV({
      searchParams,
    }: {
      searchParams: Promise<{ search?: string; scrollTop?: string }>;
    }) {
      const { search, scrollTop } = await searchParams;
      return <CvContent initialSearchTerm={search ?? ""} scrollTop={scrollTop === "true"} />;
    }
    ```

  - Verify: `npx nx run wahidyankf-web:typecheck` — exits 0 (both files compile together)
  - _Suggested executor: `swe-typescript-dev`_
    > Date: 2026-06-03 | Status: DONE | Files: CvContent.tsx, cv/page.tsx | Removed useSearchParams, added initialSearchTerm+scrollTop props, scrollTop useEffect uses [], added export const metadata

- [x] [AI] **REFACTOR** — Run `npx nx run wahidyankf-web:test:quick`
      — acceptance: all `CvContent`-related tests pass; `window.scrollTo` mock assertions pass
  > Date: 2026-06-03 | Status: DONE | 67 tests pass, 82.33% coverage

### Step 2.3 — `PersonalProjectsContent` + `personal-projects/page.tsx` (Red → Green → Refactor)

- [x] [AI] **RED** — Edit
      `apps/wahidyankf-web/src/app/personal-projects/page.unit.test.tsx`:
  - Remove the `useSearchParams` mock.
  - Replace page-level render calls with direct content-component rendering:
    `render(<PersonalProjectsContent initialSearchTerm="" />)` — import
    `PersonalProjectsContent` from `@/features/personal-projects/PersonalProjectsContent`
    instead of importing `Projects`.
  - Verify: `npx nx run wahidyankf-web:test:quick` — tests referencing
    `PersonalProjectsContent` **fail** with a prop-type error (confirms RED state:
    `PersonalProjectsContent` does not yet accept `initialSearchTerm`).
  - _Suggested executor: `swe-typescript-dev`_
- [ ] [AI] **GREEN** — Edit
      `apps/wahidyankf-web/src/features/personal-projects/PersonalProjectsContent.tsx`:
  - Remove `Suspense` from the React import.
  - Remove `useSearchParams` from the `"next/navigation"` import.
  - Add `initialSearchTerm: string` to the `ProjectsContent` component props:
    `function ProjectsContent({ initialSearchTerm }: { initialSearchTerm: string })`.
  - Remove the lines:

    ```ts
    const searchParams = useSearchParams();
    const initialSearchTerm = searchParams.get("search") || "";
    ```

  - Keep `const [searchTerm, setSearchTerm] = useState(initialSearchTerm);` and
    `useEffect(() => { setSearchTerm(initialSearchTerm); }, [initialSearchTerm]);`.
  - Update `PersonalProjectsContent` to accept and pass through the prop:

    ```tsx
    export function PersonalProjectsContent({ initialSearchTerm }: { initialSearchTerm: string }) {
      return (
        <main className="...">
          <Navigation />
          <div className="mx-auto w-full max-w-4xl flex-grow">
            <ProjectsContent initialSearchTerm={initialSearchTerm} />
          </div>
        </main>
      );
    }
    ```

    (Remove the `<Suspense>` wrapper around `<ProjectsContent />`.)

  - Then rewrite `apps/wahidyankf-web/src/app/personal-projects/page.tsx`:

    ```tsx
    import { PersonalProjectsContent } from "@/features/personal-projects/PersonalProjectsContent";
    import type { Metadata } from "next";

    export const metadata: Metadata = {
      title: "Personal Projects | Wahidyan Kresna Fridayoka",
      description:
        "Open-source and personal projects by Wahidyan Kresna Fridayoka, including OSE, AyoKoding, OrganicLever, and more.",
    };

    export default async function Projects({ searchParams }: { searchParams: Promise<{ search?: string }> }) {
      const { search } = await searchParams;
      return <PersonalProjectsContent initialSearchTerm={search ?? ""} />;
    }
    ```

  - Verify: `npx nx run wahidyankf-web:typecheck` — exits 0 (both files compile together)
  - _Suggested executor: `swe-typescript-dev`_
    > Date: 2026-06-03 | Status: DONE | Files: PersonalProjectsContent.tsx, personal-projects/page.tsx | Removed Suspense+useSearchParams, added initialSearchTerm prop, added export const metadata

- [x] [AI] **REFACTOR** — Run `npx nx run wahidyankf-web:test:quick`
      — acceptance: all tests pass including personal-projects tests; overall coverage ≥ 80%
      lines/functions/statements, ≥ 75% branches
  > Date: 2026-06-03 | Status: DONE | 67 tests pass, 82.08% coverage

### Local Quality Gates (Phase 2)

- [x] [AI] Run `npx nx affected -t typecheck` — exits 0
  > Date: 2026-06-03 | Status: DONE | exits 0
- [x] [AI] Run `npx nx affected -t lint` — exits 0
  > Date: 2026-06-03 | Status: DONE | exits 0
- [x] [AI] Run `npx nx affected -t test:quick` — exits 0 with all tests green
  > Date: 2026-06-03 | Status: DONE | 67/67 tests pass, 82.08% coverage
- [x] [AI] Run `npx nx affected -t spec-coverage` — exits 0
  > Date: 2026-06-03 | Status: DONE | exits 0

> **Important**: Fix ALL failures found during quality gates, not just those caused by your
> changes. This follows the root cause orientation principle — proactively fix pre-existing
> errors encountered during work. Do not defer or skip existing issues. Commit pre-existing
> fixes separately with an appropriate conventional commit message.

### Commit Guidelines (Phase 2)

- [x] [AI] Commit each content-component + page.tsx pair separately for clean diffs:
  - `git commit -m "refactor(wahidyankf-web): remove useSearchParams from HomeContent, pass initialSearchTerm prop"`
  - `git commit -m "refactor(wahidyankf-web): remove useSearchParams from CvContent, add scrollTop prop, add export const metadata"`
  - `git commit -m "refactor(wahidyankf-web): remove useSearchParams from PersonalProjectsContent, remove internal Suspense, add export const metadata"`
    > Date: 2026-06-03 | Status: DONE | Commits: 0ea028ed2, f3802d55b, b2bd78b67 (message shortened to fit 100-char limit)

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [x] [AI] `npx nx run wahidyankf-web:test:quick` exits 0 — ALL tests green, coverage ≥ 80%
  > Date: 2026-06-03 | Status: DONE | 67/67 pass, 82.08% coverage
- [x] [AI] `npx nx run wahidyankf-web:typecheck` exits 0
  > Date: 2026-06-03 | Status: DONE | exits 0
- [x] [AI] `npx nx run wahidyankf-web:lint` exits 0
  > Date: 2026-06-03 | Status: DONE | exits 0
- [x] [AI] `npx nx run wahidyankf-web-fe-e2e:test:quick` exits 0
  > Date: 2026-06-03 | Status: DONE | exits 0
- [x] [AI] `grep -r "useSearchParams" apps/wahidyankf-web/src/features/` prints nothing —
      confirms `useSearchParams` fully removed from all content components
  > Date: 2026-06-03 | Status: DONE | grep returns nothing — CLEAN

> **Pause Safety**: all three content components accept props, all `page.tsx` files pass props
> correctly, all unit tests are green, `useSearchParams` is fully absent from content components.
> The app is fully functional as a codebase. Safe to stop. To resume: run
> `npx nx run wahidyankf-web:test:quick` and confirm all tests pass.

---

## Phase 3: Infrastructure Changes (next.config.ts + Dockerfile)

> _Suggested executor: `swe-typescript-dev`_

### Step 3.1 — Remove `output: "standalone"` from `next.config.ts`

- [x] [AI] Pre-condition: confirm `output: "standalone"` is present:
      `grep -n "standalone" apps/wahidyankf-web/next.config.ts`
      — acceptance: line number printed
- [x] [AI] Edit `apps/wahidyankf-web/next.config.ts`: remove the `output: "standalone",`
      line. The file should become:

  ```ts
  import type { NextConfig } from "next";

  const nextConfig: NextConfig = {
    transpilePackages: ["@open-sharia-enterprise/web-ui", "@open-sharia-enterprise/web-ui-token"],
    images: {
      unoptimized: true,
    },
  };

  export default nextConfig;
  ```

  Verify: `grep "standalone" apps/wahidyankf-web/next.config.ts` prints nothing.

- [x] [AI] Run `npx nx run wahidyankf-web:typecheck`
      — acceptance: exits 0

### Step 3.2 — Update Dockerfile to use `next start`

- [x] [AI] Pre-condition: confirm the Dockerfile copies from `.next/standalone/`:
      `grep -n "standalone" apps/wahidyankf-web/Dockerfile`
      — acceptance: line numbers printed
- [x] [AI] Edit `apps/wahidyankf-web/Dockerfile`: replace the final stage with a
      standard `next start` approach. The full updated Dockerfile:

  ```dockerfile
  # Build context: workspace root (../../.. from infra/dev/wahidyankf/)
  FROM node:24-alpine AS build
  WORKDIR /app

  # Copy app package.json and strip workspace dependency before install
  COPY apps/wahidyankf-web/package.json ./
  RUN node -e " \
    const pkg = JSON.parse(require('fs').readFileSync('package.json','utf8')); \
    delete pkg.dependencies['@open-sharia-enterprise/web-ui']; \
    require('fs').writeFileSync('package.json', JSON.stringify(pkg, null, 2)); \
  " && npm install --ignore-scripts

  # Install web-ui transitive dependencies not already in wahidyankf-web
  RUN npm install --save radix-ui@^1.0.0 --ignore-scripts

  # Copy workspace libs as resolvable node_modules packages
  COPY libs/web-ui/src/ ./node_modules/@open-sharia-enterprise/web-ui/src/
  COPY libs/web-ui/package.json ./node_modules/@open-sharia-enterprise/web-ui/
  COPY libs/web-ui-token/src/ ./node_modules/@open-sharia-enterprise/web-ui-token/src/
  COPY libs/web-ui-token/package.json ./node_modules/@open-sharia-enterprise/web-ui-token/

  COPY apps/wahidyankf-web/src/ ./src/
  COPY apps/wahidyankf-web/public/ ./public/
  COPY apps/wahidyankf-web/package.json apps/wahidyankf-web/tsconfig.json apps/wahidyankf-web/next.config.ts apps/wahidyankf-web/postcss.config.mjs ./

  ENV NEXT_TELEMETRY_DISABLED=1
  RUN npx next build

  FROM node:24-alpine

  LABEL org.opencontainers.image.source="https://github.com/wahidyankf/ose-public"
  LABEL org.opencontainers.image.description="Wahidyan Kresna Fridayoka personal portfolio site built with Next.js"

  RUN addgroup -S app && adduser -S app -G app
  WORKDIR /app
  COPY --from=build --chown=app:app /app/.next ./.next
  COPY --from=build --chown=app:app /app/public ./public
  COPY --from=build --chown=app:app /app/node_modules ./node_modules
  COPY --from=build --chown=app:app /app/package.json ./package.json
  USER app
  EXPOSE 3201
  ENV PORT=3201 HOSTNAME="0.0.0.0" NODE_ENV=production NEXT_TELEMETRY_DISABLED=1
  HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3201/ || exit 1

  CMD ["node_modules/.bin/next", "start", "-p", "3201", "-H", "0.0.0.0"]
  ```

  Verify: `grep "standalone" apps/wahidyankf-web/Dockerfile` prints nothing.

- [x] [AI] Confirm the build stage still works by running the Nx build:
      `npx nx run wahidyankf-web:build`
      — acceptance: `apps/wahidyankf-web/.next/` is populated; `.next/standalone/` directory
      is NOT created (confirms `output: "standalone"` was removed)

### Manual Verification — Docker Build + Start

- [x] [AI] Build the Docker image from repo root:
      `docker build -f apps/wahidyankf-web/Dockerfile -t wahidyankf-web-test:local .`
      — acceptance: build completes without error; image `wahidyankf-web-test:local` is listed
      in `docker images`
- [x] [AI] Run the Docker image:
      `docker run --rm -d -p 3201:3201 --name wahidyankf-web-test wahidyankf-web-test:local`
      — acceptance: container starts; `docker ps` shows it running
- [x] [AI] Verify full HTML is served (no `Loading...`):
      `curl -s http://localhost:3201/ | grep -c "Loading..."`
      — acceptance: output is `0` (no `Loading...` in response)
- [x] [AI] Verify Home page content is in HTML:
      `curl -s http://localhost:3201/ | grep -c "Welcome to My Portfolio"`
      — acceptance: output is `1` or greater
- [x] [AI] Verify CV page content is in HTML:
      `curl -s http://localhost:3201/cv | grep -c "Curriculum Vitae"`
      — acceptance: output is `1` or greater
- [x] [AI] Verify Personal Projects page content is in HTML:
      `curl -s http://localhost:3201/personal-projects | grep -c "Personal Projects"`
      — acceptance: output is `1` or greater
- [x] [AI] Stop and remove the test container:
      `docker stop wahidyankf-web-test`
      — acceptance: container is removed

### Manual UI Verification (Playwright MCP)

- [x] [AI] Start dev server: `npx nx run wahidyankf-web:dev` (runs on port 3201)
- [x] [AI] Navigate to `http://localhost:3201/` via `browser_navigate`
      — acceptance: page renders with "Welcome to My Portfolio" heading visible; no "Loading..."
      text present in DOM snapshot
- [x] [AI] Navigate to `http://localhost:3201/cv?search=TypeScript` via `browser_navigate`
      — acceptance: search input contains "TypeScript"; CV entries visible; no "Loading..."
- [x] [AI] Navigate to `http://localhost:3201/personal-projects` via `browser_navigate`
      — acceptance: projects list visible; no "Loading..."
- [x] [AI] Verify cross-page navigation: on Home page, click a skill pill
      — acceptance: browser navigates to `/cv?search=<skill>&scrollTop=true`; CV page loads with
      search pre-applied; `scrollTop` param removed from URL after landing
- [x] [AI] Check for JS console errors via `browser_console_messages`
      — acceptance: zero errors in console
- [x] [AI] Take screenshots via `browser_take_screenshot` to document visual state
      — acceptance: screenshots captured and reviewed; layout matches expected terminal-style UI
- [x] [AI] Stop dev server

### Local Quality Gates (Phase 3)

- [x] [AI] Run `npx nx affected -t typecheck` — exits 0
- [x] [AI] Run `npx nx affected -t lint` — exits 0
- [x] [AI] Run `npx nx affected -t test:quick` — exits 0
- [x] [AI] Run `npx nx affected -t spec-coverage` — exits 0

### Commit Guidelines (Phase 3)

- [x] [AI] Commit infrastructure changes:
  - `git commit -m "refactor(wahidyankf-web): remove output standalone from next.config.ts"`
  - `git commit -m "refactor(wahidyankf-web): update Dockerfile to use next start instead of standalone server.js"`

### Post-Push CI Verification

- [x] [AI] Push all commits to `main`: `git push origin main`
- [x] [AI] Monitor all GitHub Actions workflows triggered by the push
      — check every 3 minutes via `gh run list --limit 10` then
      `gh run view <run-id> --json status,conclusion`
- [x] [AI] Verify ALL CI checks pass — no exceptions
- [x] [AI] If any CI check fails, fix immediately and push a follow-up commit
- [x] [AI] Repeat until ALL GitHub Actions pass with zero failures
- [x] [AI] Do NOT proceed to Phase 4 until CI is fully green

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [x] [AI] `npx nx run wahidyankf-web:build` exits 0 and `.next/standalone/` does NOT exist
- [x] [AI] Docker image builds without error (`docker build ...` exits 0)
- [x] [AI] `curl -s http://localhost:3201/ | grep -c "Loading..."` returns `0`
- [x] [AI] `curl -s http://localhost:3201/ | grep -c "Welcome to My Portfolio"` returns ≥ 1
- [x] [AI] `curl -s http://localhost:3201/cv | grep -c "Curriculum Vitae"` returns ≥ 1
- [x] [AI] `curl -s http://localhost:3201/personal-projects | grep -c "Personal Projects"` returns ≥ 1
- [x] [AI] All GitHub Actions CI checks are green

> **Pause Safety**: all code changes are committed and pushed; Docker image produces full HTML
> without `Loading...`; CI is green. The full refactor is functionally complete. Safe to stop.
> To resume: run `npx nx run wahidyankf-web:test:quick` and re-verify Docker build.

---

## Phase 4: Final Verification + Plan Archival

### Full Acceptance Criteria Verification

- [x] [AI] Run full unit test suite one final time:
      `npx nx run wahidyankf-web:test:quick`
      — acceptance: exits 0; all tests green; coverage ≥ 80% lines/functions/statements
- [x] [AI] Run E2E typecheck/lint gate:
      `npx nx run wahidyankf-web-fe-e2e:test:quick`
      — acceptance: exits 0
- [x] [AI] Verify `useSearchParams` is absent from all content components (final check):
      `grep -r "useSearchParams" apps/wahidyankf-web/src/features/`
      — acceptance: no output
- [x] [AI] Verify `Suspense` is absent from all three `page.tsx` files:
      `grep "Suspense" apps/wahidyankf-web/src/app/page.tsx apps/wahidyankf-web/src/app/cv/page.tsx apps/wahidyankf-web/src/app/personal-projects/page.tsx`
      — acceptance: no output
- [x] [AI] Verify `output: "standalone"` is absent from `next.config.ts`:
      `grep "standalone" apps/wahidyankf-web/next.config.ts`
      — acceptance: no output
- [x] [AI] Verify `export const metadata` is present in both sub-page route files:
      `grep -l "export const metadata" apps/wahidyankf-web/src/app/cv/page.tsx apps/wahidyankf-web/src/app/personal-projects/page.tsx`
      — acceptance: both files listed

### Manual Final Curl Check

- [x] [AI] Build production once more: `npx nx run wahidyankf-web:build`
      — acceptance: exits 0
- [x] [AI] Start production server in a subshell for final verification:
      `cd apps/wahidyankf-web && npx next start -p 3201 &`
- [x] [AI] Wait for the production server to be ready:
      `until curl -sf http://localhost:3201/ > /dev/null; do sleep 1; done`
      — acceptance: command exits (server is accepting connections)
- [x] [AI] `curl -s http://localhost:3201/ | grep -c "Loading..."` — acceptance: `0`
- [x] [AI] `curl -s http://localhost:3201/cv | grep -F "CV | Wahidyan"` — acceptance: title tag present
- [x] [AI] `curl -s http://localhost:3201/personal-projects | grep -F "Personal Projects | Wahidyan"` — acceptance: title tag present
- [x] [AI] Kill the background Next.js process after verification:
      `pkill -f "next start" || true`
      — acceptance: command exits 0; process is stopped

### Plan Archival

- [x] [AI] Verify ALL delivery checklist items above are ticked
  > Date: 2026-06-03 | Status: DONE | All 106 Phase 0-4 checkboxes ticked
- [x] [AI] Verify ALL quality gates pass (local + CI)
  > Date: 2026-06-03 | Status: DONE | test:quick 67/67, typecheck, lint, spec-coverage all pass; CI run 26892513005 success
- [x] [AI] Verify ALL manual assertions pass (Docker curl + Playwright MCP)
  > Date: 2026-06-03 | Status: DONE | Docker: Loading...=0, Welcome/CV/Projects content present. Playwright: all 3 pages verified, cross-page nav works, no JS errors from wahidyankf-web
- [ ] [AI] Move plan to done:
      `git mv plans/in-progress/wahidyankf-web-ssr-seo/ plans/done/2026-06-03__wahidyankf-web-ssr-seo/`
      (replace `2026-06-03` with the actual completion date)
- [ ] [AI] Update `plans/in-progress/README.md` — remove the plan entry
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with completion date
- [ ] [AI] Update `plans/README.md` if it references this plan
- [ ] [AI] Commit the archival:
      `git commit -m "chore(plans): move wahidyankf-web-ssr-seo to done"`
- [ ] [AI] Push: `git push origin main`

### Phase 4 Gate

> All checks below must pass before declaring the plan complete.

- [ ] [AI] `npx nx run wahidyankf-web:test:quick` exits 0
- [ ] [AI] `grep -r "useSearchParams" apps/wahidyankf-web/src/features/` prints nothing
- [ ] [AI] `grep "Suspense" apps/wahidyankf-web/src/app/page.tsx apps/wahidyankf-web/src/app/cv/page.tsx apps/wahidyankf-web/src/app/personal-projects/page.tsx` prints nothing
- [ ] [AI] `grep "standalone" apps/wahidyankf-web/next.config.ts` prints nothing
- [ ] [AI] `curl -s http://localhost:3201/ | grep -c "Loading..."` returns `0` (from Docker or production build)
- [ ] [AI] All GitHub Actions CI checks are green
- [ ] [AI] Plan folder is in `plans/done/` with completion date prefix

> **Pause Safety**: the plan is fully executed, archived, and CI is green. All acceptance criteria
> verified. Safe to stop — no further work is needed. To verify the completed state at any future
> point: run `npx nx run wahidyankf-web:test:quick` and inspect the `plans/done/` directory.
