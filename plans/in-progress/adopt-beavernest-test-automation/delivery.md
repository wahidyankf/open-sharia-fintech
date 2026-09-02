# Delivery Plan

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it. `[AI+HUMAN]`: the agent prepares and the human finishes.

This checklist is prospective. It does not authorize implementation, staging, committing, pushing,
opening PRs, or changing either repository. Execute it only after the user explicitly names this
plan for execution.

## Delivery Mode

`worktree-to-pr` applies independently to `ose-public` and `ose-private`. The plan is single-sourced
in public. Each repository has its own worktree, branches, commits, PRs, current-head/base CI,
rules-propagation evidence, recovery proof, merge, and cleanup.

## Worktree

- Public: `R-PUB:worktrees/adopt-beavernest-test-automation/`
- Private: `R-PRI:worktrees/adopt-beavernest-test-automation/`
- Current plan-authoring exception: `R-PUB:worktrees/rules-update/`

Provisioning status: provisioned

The user required plan authoring to remain in `rules-update`; both matching execution worktrees
were provisioned through the supported harness command. Their immutable identity appears below;
the explicit fallback commands remain recovery-only and must not be run for these registered roots.

### Provisioned Worktree Identity

- Public declared repository-relative route: `worktrees/adopt-beavernest-test-automation/`
- Public initial branch: `worktree/adopt-beavernest-test-automation`
- Private declared repository-relative route: `worktrees/adopt-beavernest-test-automation/`
- Private initial branch: `worktree/adopt-beavernest-test-automation`
- Created by: Codex plan-execution coordinator through `claude --worktree`
- Created at: `2026-08-30T22:09:49Z`
- Runtime location evidence: ignored Phase 0 runtime evidence only

### Cross-Repository Parity Identity

- Objective slug: `adopt-beavernest-test-automation`
- Worktree basename: `adopt-beavernest-test-automation`

| Repository    | Corresponding short-lived branch                  |
| ------------- | ------------------------------------------------- |
| `ose-public`  | `not applicable — Phase 0 has no delivery branch` |
| `ose-private` | `not applicable — Phase 0 has no delivery branch` |

### Delivery Branch Inventory

| Repository    | Branch                                      | Mode          | Lifecycle state | Proof                                                                          |
| ------------- | ------------------------------------------- | ------------- | --------------- | ------------------------------------------------------------------------------ |
| `ose-public`  | `worktree/adopt-beavernest-test-automation` | `provisioned` | `active`        | `claude --worktree adopt-beavernest-test-automation` at `2026-08-30T22:09:49Z` |
| `ose-private` | `worktree/adopt-beavernest-test-automation` | `provisioned` | `active`        | `claude --worktree adopt-beavernest-test-automation` at `2026-08-30T22:09:49Z` |

From the selected `ose-public` checkout, run only its invocation:

```bash
rtk bash -lc 'set -euo pipefail; plan_identity="$(rtk node -e '"'"'const fs=require("node:fs"),path=require("node:path"),cp=require("node:child_process"); const id="adopt-beavernest-test-automation"; const fail=()=>{throw Error("Execution root validation failed; stop and recheck the selected checkouts and Phase 0 evidence")}; const check=x=>{if(!x)fail()}; const real=x=>fs.realpathSync(x); const git=(root,...args)=>cp.execFileSync("git",["-C",root,...args],{encoding:"utf8",stdio:["ignore","pipe","pipe"]}); const text=x=>x.replace(/\n$/,""); const origin=root=>{const raw=text(git(root,"remote","get-url","origin")); let u; try{u=new URL(raw.replace(/^git@github\.com:/,"ssh://git@github.com/"))}catch{fail()} check(["https:","ssh:"].includes(u.protocol)&&u.hostname==="github.com"&&!u.port&&!u.search&&!u.hash); const name=u.pathname.replace(/^\//,"").replace(/\.git\/?$/,"").replace(/\/$/,""); check(["wahidyankf/ose-public","wahidyankf/ose-private"].includes(name)); return name.endsWith("ose-public")?"public":"private"}; const records=root=>git(root,"worktree","list","--porcelain","-z").split("\0\0").filter(Boolean).map(x=>Object.fromEntries(x.split("\0").filter(Boolean).map(l=>{const n=l.indexOf(" ");return n<0?[l,""]:[l.slice(0,n),l.slice(n+1)]}))); const discover=(selected,repo,registered)=>{check(typeof selected==="string"&&selected.length>0&&!/[\r\n\0]/.test(selected)); const common=real(text(git(selected,"rev-parse","--path-format=absolute","--git-common-dir"))); check(path.basename(common)===".git"); const primary=path.dirname(common); check(real(text(git(primary,"rev-parse","--show-toplevel")))===primary&&real(text(git(primary,"rev-parse","--path-format=absolute","--git-common-dir")))===common&&origin(primary)===repo); const worktree=path.join(primary,"worktrees",id); if(registered){check(real(worktree)===worktree&&real(text(git(worktree,"rev-parse","--path-format=absolute","--git-common-dir")))===common); check(records(primary).filter(r=>r.worktree===worktree).length===1)} return {primary,common,worktree}}; const current=()=>real(text(git(process.cwd(),"rev-parse","--show-toplevel"))); const mapPath=(repo,root)=>path.join(root,"local-tmp",id,"evidence/runtime",repo,"phase-0",repo==="public"?"R-PUB":"R-PRI","execution-roots.json"); const ignored=(root,file)=>{check(fs.lstatSync(file).isFile()); git(root,"check-ignore","-q","--",file); check(git(root,"ls-files","--",file)==="")}; const validate=m=>{check(m&&typeof m==="object"&&!Array.isArray(m)&&Object.keys(m).sort().join(",")==="planId,privatePrimary,privateWorktree,publicPrimary,publicWorktree"); check(m.planId===id); for(const key of ["publicPrimary","privatePrimary","publicWorktree","privateWorktree"])check(typeof m[key]==="string"&&path.isAbsolute(m[key])&&!/[\r\n\0]/.test(m[key])); const a=discover(m.publicPrimary,"public",true),b=discover(m.privatePrimary,"private",true); check(a.primary!==b.primary&&a.common!==b.common&&a.primary===m.publicPrimary&&b.primary===m.privatePrimary&&a.worktree===m.publicWorktree&&b.worktree===m.privateWorktree); return m}; const load=expected=>{const repo=origin(process.cwd()); check(expected==="either"||repo===expected); const d=discover(process.cwd(),repo,true); check(current()===d.worktree); const file=mapPath(repo,d.worktree); ignored(d.worktree,file); const m=validate(JSON.parse(fs.readFileSync(file,"utf8"))); check(m[repo+"Worktree"]===current()); for(const other of ["public","private"]){const p=mapPath(other,m[other+"Worktree"]); ignored(m[other+"Worktree"],p); const peer=validate(JSON.parse(fs.readFileSync(p,"utf8"))); check(Object.keys(m).every(k=>m[k]===peer[k]))} return m}; const d=discover(process.cwd(),"public",false); process.stdout.write(JSON.stringify(d))'"'"')"; plan_primary="$(printf "%s" "$plan_identity" | rtk jq -r .primary)"; plan_worktree="$(printf "%s" "$plan_identity" | rtk jq -r .worktree)"; test ! -e "$plan_worktree"; if rtk git -C "$plan_primary" show-ref --verify --quiet refs/heads/adopt-beavernest-test-automation; then exit 1; fi; cd "$plan_primary"; claude --worktree adopt-beavernest-test-automation'
```

From the selected `ose-private` checkout, run only its invocation:

```bash
rtk bash -lc 'set -euo pipefail; plan_identity="$(rtk node -e '"'"'const fs=require("node:fs"),path=require("node:path"),cp=require("node:child_process"); const id="adopt-beavernest-test-automation"; const fail=()=>{throw Error("Execution root validation failed; stop and recheck the selected checkouts and Phase 0 evidence")}; const check=x=>{if(!x)fail()}; const real=x=>fs.realpathSync(x); const git=(root,...args)=>cp.execFileSync("git",["-C",root,...args],{encoding:"utf8",stdio:["ignore","pipe","pipe"]}); const text=x=>x.replace(/\n$/,""); const origin=root=>{const raw=text(git(root,"remote","get-url","origin")); let u; try{u=new URL(raw.replace(/^git@github\.com:/,"ssh://git@github.com/"))}catch{fail()} check(["https:","ssh:"].includes(u.protocol)&&u.hostname==="github.com"&&!u.port&&!u.search&&!u.hash); const name=u.pathname.replace(/^\//,"").replace(/\.git\/?$/,"").replace(/\/$/,""); check(["wahidyankf/ose-public","wahidyankf/ose-private"].includes(name)); return name.endsWith("ose-public")?"public":"private"}; const records=root=>git(root,"worktree","list","--porcelain","-z").split("\0\0").filter(Boolean).map(x=>Object.fromEntries(x.split("\0").filter(Boolean).map(l=>{const n=l.indexOf(" ");return n<0?[l,""]:[l.slice(0,n),l.slice(n+1)]}))); const discover=(selected,repo,registered)=>{check(typeof selected==="string"&&selected.length>0&&!/[\r\n\0]/.test(selected)); const common=real(text(git(selected,"rev-parse","--path-format=absolute","--git-common-dir"))); check(path.basename(common)===".git"); const primary=path.dirname(common); check(real(text(git(primary,"rev-parse","--show-toplevel")))===primary&&real(text(git(primary,"rev-parse","--path-format=absolute","--git-common-dir")))===common&&origin(primary)===repo); const worktree=path.join(primary,"worktrees",id); if(registered){check(real(worktree)===worktree&&real(text(git(worktree,"rev-parse","--path-format=absolute","--git-common-dir")))===common); check(records(primary).filter(r=>r.worktree===worktree).length===1)} return {primary,common,worktree}}; const current=()=>real(text(git(process.cwd(),"rev-parse","--show-toplevel"))); const mapPath=(repo,root)=>path.join(root,"local-tmp",id,"evidence/runtime",repo,"phase-0",repo==="public"?"R-PUB":"R-PRI","execution-roots.json"); const ignored=(root,file)=>{check(fs.lstatSync(file).isFile()); git(root,"check-ignore","-q","--",file); check(git(root,"ls-files","--",file)==="")}; const validate=m=>{check(m&&typeof m==="object"&&!Array.isArray(m)&&Object.keys(m).sort().join(",")==="planId,privatePrimary,privateWorktree,publicPrimary,publicWorktree"); check(m.planId===id); for(const key of ["publicPrimary","privatePrimary","publicWorktree","privateWorktree"])check(typeof m[key]==="string"&&path.isAbsolute(m[key])&&!/[\r\n\0]/.test(m[key])); const a=discover(m.publicPrimary,"public",true),b=discover(m.privatePrimary,"private",true); check(a.primary!==b.primary&&a.common!==b.common&&a.primary===m.publicPrimary&&b.primary===m.privatePrimary&&a.worktree===m.publicWorktree&&b.worktree===m.privateWorktree); return m}; const load=expected=>{const repo=origin(process.cwd()); check(expected==="either"||repo===expected); const d=discover(process.cwd(),repo,true); check(current()===d.worktree); const file=mapPath(repo,d.worktree); ignored(d.worktree,file); const m=validate(JSON.parse(fs.readFileSync(file,"utf8"))); check(m[repo+"Worktree"]===current()); for(const other of ["public","private"]){const p=mapPath(other,m[other+"Worktree"]); ignored(m[other+"Worktree"],p); const peer=validate(JSON.parse(fs.readFileSync(p,"utf8"))); check(Object.keys(m).every(k=>m[k]===peer[k]))} return m}; const d=discover(process.cwd(),"private",false); process.stdout.write(JSON.stringify(d))'"'"')"; plan_primary="$(printf "%s" "$plan_identity" | rtk jq -r .primary)"; plan_worktree="$(printf "%s" "$plan_identity" | rtk jq -r .worktree)"; test ! -e "$plan_worktree"; if rtk git -C "$plan_primary" show-ref --verify --quiet refs/heads/adopt-beavernest-test-automation; then exit 1; fi; cd "$plan_primary"; claude --worktree adopt-beavernest-test-automation'
```

If `claude --worktree` succeeds for a repository, do not also run that repository's fallback
`worktree add`. Record its declared repository-relative route, branch, and base SHA in Phase 0. Keep
any resolved host path only in ignored runtime evidence. If the command is unavailable or exits
non-zero, save its output and use only the matching explicit fallback below.

Phase 0 provisions the pending worktrees from each repository's latest `origin/main`:

From the selected `ose-public` checkout, run the matching fallback only:

```bash
rtk bash -lc 'set -euo pipefail; plan_identity="$(rtk node -e '"'"'const fs=require("node:fs"),path=require("node:path"),cp=require("node:child_process"); const id="adopt-beavernest-test-automation"; const fail=()=>{throw Error("Execution root validation failed; stop and recheck the selected checkouts and Phase 0 evidence")}; const check=x=>{if(!x)fail()}; const real=x=>fs.realpathSync(x); const git=(root,...args)=>cp.execFileSync("git",["-C",root,...args],{encoding:"utf8",stdio:["ignore","pipe","pipe"]}); const text=x=>x.replace(/\n$/,""); const origin=root=>{const raw=text(git(root,"remote","get-url","origin")); let u; try{u=new URL(raw.replace(/^git@github\.com:/,"ssh://git@github.com/"))}catch{fail()} check(["https:","ssh:"].includes(u.protocol)&&u.hostname==="github.com"&&!u.port&&!u.search&&!u.hash); const name=u.pathname.replace(/^\//,"").replace(/\.git\/?$/,"").replace(/\/$/,""); check(["wahidyankf/ose-public","wahidyankf/ose-private"].includes(name)); return name.endsWith("ose-public")?"public":"private"}; const records=root=>git(root,"worktree","list","--porcelain","-z").split("\0\0").filter(Boolean).map(x=>Object.fromEntries(x.split("\0").filter(Boolean).map(l=>{const n=l.indexOf(" ");return n<0?[l,""]:[l.slice(0,n),l.slice(n+1)]}))); const discover=(selected,repo,registered)=>{check(typeof selected==="string"&&selected.length>0&&!/[\r\n\0]/.test(selected)); const common=real(text(git(selected,"rev-parse","--path-format=absolute","--git-common-dir"))); check(path.basename(common)===".git"); const primary=path.dirname(common); check(real(text(git(primary,"rev-parse","--show-toplevel")))===primary&&real(text(git(primary,"rev-parse","--path-format=absolute","--git-common-dir")))===common&&origin(primary)===repo); const worktree=path.join(primary,"worktrees",id); if(registered){check(real(worktree)===worktree&&real(text(git(worktree,"rev-parse","--path-format=absolute","--git-common-dir")))===common); check(records(primary).filter(r=>r.worktree===worktree).length===1)} return {primary,common,worktree}}; const current=()=>real(text(git(process.cwd(),"rev-parse","--show-toplevel"))); const mapPath=(repo,root)=>path.join(root,"local-tmp",id,"evidence/runtime",repo,"phase-0",repo==="public"?"R-PUB":"R-PRI","execution-roots.json"); const ignored=(root,file)=>{check(fs.lstatSync(file).isFile()); git(root,"check-ignore","-q","--",file); check(git(root,"ls-files","--",file)==="")}; const validate=m=>{check(m&&typeof m==="object"&&!Array.isArray(m)&&Object.keys(m).sort().join(",")==="planId,privatePrimary,privateWorktree,publicPrimary,publicWorktree"); check(m.planId===id); for(const key of ["publicPrimary","privatePrimary","publicWorktree","privateWorktree"])check(typeof m[key]==="string"&&path.isAbsolute(m[key])&&!/[\r\n\0]/.test(m[key])); const a=discover(m.publicPrimary,"public",true),b=discover(m.privatePrimary,"private",true); check(a.primary!==b.primary&&a.common!==b.common&&a.primary===m.publicPrimary&&b.primary===m.privatePrimary&&a.worktree===m.publicWorktree&&b.worktree===m.privateWorktree); return m}; const load=expected=>{const repo=origin(process.cwd()); check(expected==="either"||repo===expected); const d=discover(process.cwd(),repo,true); check(current()===d.worktree); const file=mapPath(repo,d.worktree); ignored(d.worktree,file); const m=validate(JSON.parse(fs.readFileSync(file,"utf8"))); check(m[repo+"Worktree"]===current()); for(const other of ["public","private"]){const p=mapPath(other,m[other+"Worktree"]); ignored(m[other+"Worktree"],p); const peer=validate(JSON.parse(fs.readFileSync(p,"utf8"))); check(Object.keys(m).every(k=>m[k]===peer[k]))} return m}; const d=discover(process.cwd(),"public",false); process.stdout.write(JSON.stringify(d))'"'"')"; plan_primary="$(printf "%s" "$plan_identity" | rtk jq -r .primary)"; plan_worktree="$(printf "%s" "$plan_identity" | rtk jq -r .worktree)"; rtk git -C "$plan_primary" fetch origin main'
rtk bash -lc 'set -euo pipefail; plan_identity="$(rtk node -e '"'"'const fs=require("node:fs"),path=require("node:path"),cp=require("node:child_process"); const id="adopt-beavernest-test-automation"; const fail=()=>{throw Error("Execution root validation failed; stop and recheck the selected checkouts and Phase 0 evidence")}; const check=x=>{if(!x)fail()}; const real=x=>fs.realpathSync(x); const git=(root,...args)=>cp.execFileSync("git",["-C",root,...args],{encoding:"utf8",stdio:["ignore","pipe","pipe"]}); const text=x=>x.replace(/\n$/,""); const origin=root=>{const raw=text(git(root,"remote","get-url","origin")); let u; try{u=new URL(raw.replace(/^git@github\.com:/,"ssh://git@github.com/"))}catch{fail()} check(["https:","ssh:"].includes(u.protocol)&&u.hostname==="github.com"&&!u.port&&!u.search&&!u.hash); const name=u.pathname.replace(/^\//,"").replace(/\.git\/?$/,"").replace(/\/$/,""); check(["wahidyankf/ose-public","wahidyankf/ose-private"].includes(name)); return name.endsWith("ose-public")?"public":"private"}; const records=root=>git(root,"worktree","list","--porcelain","-z").split("\0\0").filter(Boolean).map(x=>Object.fromEntries(x.split("\0").filter(Boolean).map(l=>{const n=l.indexOf(" ");return n<0?[l,""]:[l.slice(0,n),l.slice(n+1)]}))); const discover=(selected,repo,registered)=>{check(typeof selected==="string"&&selected.length>0&&!/[\r\n\0]/.test(selected)); const common=real(text(git(selected,"rev-parse","--path-format=absolute","--git-common-dir"))); check(path.basename(common)===".git"); const primary=path.dirname(common); check(real(text(git(primary,"rev-parse","--show-toplevel")))===primary&&real(text(git(primary,"rev-parse","--path-format=absolute","--git-common-dir")))===common&&origin(primary)===repo); const worktree=path.join(primary,"worktrees",id); if(registered){check(real(worktree)===worktree&&real(text(git(worktree,"rev-parse","--path-format=absolute","--git-common-dir")))===common); check(records(primary).filter(r=>r.worktree===worktree).length===1)} return {primary,common,worktree}}; const current=()=>real(text(git(process.cwd(),"rev-parse","--show-toplevel"))); const mapPath=(repo,root)=>path.join(root,"local-tmp",id,"evidence/runtime",repo,"phase-0",repo==="public"?"R-PUB":"R-PRI","execution-roots.json"); const ignored=(root,file)=>{check(fs.lstatSync(file).isFile()); git(root,"check-ignore","-q","--",file); check(git(root,"ls-files","--",file)==="")}; const validate=m=>{check(m&&typeof m==="object"&&!Array.isArray(m)&&Object.keys(m).sort().join(",")==="planId,privatePrimary,privateWorktree,publicPrimary,publicWorktree"); check(m.planId===id); for(const key of ["publicPrimary","privatePrimary","publicWorktree","privateWorktree"])check(typeof m[key]==="string"&&path.isAbsolute(m[key])&&!/[\r\n\0]/.test(m[key])); const a=discover(m.publicPrimary,"public",true),b=discover(m.privatePrimary,"private",true); check(a.primary!==b.primary&&a.common!==b.common&&a.primary===m.publicPrimary&&b.primary===m.privatePrimary&&a.worktree===m.publicWorktree&&b.worktree===m.privateWorktree); return m}; const load=expected=>{const repo=origin(process.cwd()); check(expected==="either"||repo===expected); const d=discover(process.cwd(),repo,true); check(current()===d.worktree); const file=mapPath(repo,d.worktree); ignored(d.worktree,file); const m=validate(JSON.parse(fs.readFileSync(file,"utf8"))); check(m[repo+"Worktree"]===current()); for(const other of ["public","private"]){const p=mapPath(other,m[other+"Worktree"]); ignored(m[other+"Worktree"],p); const peer=validate(JSON.parse(fs.readFileSync(p,"utf8"))); check(Object.keys(m).every(k=>m[k]===peer[k]))} return m}; const d=discover(process.cwd(),"public",false); process.stdout.write(JSON.stringify(d))'"'"')"; plan_primary="$(printf "%s" "$plan_identity" | rtk jq -r .primary)"; plan_worktree="$(printf "%s" "$plan_identity" | rtk jq -r .worktree)"; test ! -e "$plan_worktree"; if rtk git -C "$plan_primary" show-ref --verify --quiet refs/heads/adopt-beavernest-test-automation; then exit 1; fi; rtk git -C "$plan_primary" worktree add -b adopt-beavernest-test-automation "$plan_worktree" origin/main'
```

From the selected `ose-private` checkout, run the matching fallback only:

```bash
rtk bash -lc 'set -euo pipefail; plan_identity="$(rtk node -e '"'"'const fs=require("node:fs"),path=require("node:path"),cp=require("node:child_process"); const id="adopt-beavernest-test-automation"; const fail=()=>{throw Error("Execution root validation failed; stop and recheck the selected checkouts and Phase 0 evidence")}; const check=x=>{if(!x)fail()}; const real=x=>fs.realpathSync(x); const git=(root,...args)=>cp.execFileSync("git",["-C",root,...args],{encoding:"utf8",stdio:["ignore","pipe","pipe"]}); const text=x=>x.replace(/\n$/,""); const origin=root=>{const raw=text(git(root,"remote","get-url","origin")); let u; try{u=new URL(raw.replace(/^git@github\.com:/,"ssh://git@github.com/"))}catch{fail()} check(["https:","ssh:"].includes(u.protocol)&&u.hostname==="github.com"&&!u.port&&!u.search&&!u.hash); const name=u.pathname.replace(/^\//,"").replace(/\.git\/?$/,"").replace(/\/$/,""); check(["wahidyankf/ose-public","wahidyankf/ose-private"].includes(name)); return name.endsWith("ose-public")?"public":"private"}; const records=root=>git(root,"worktree","list","--porcelain","-z").split("\0\0").filter(Boolean).map(x=>Object.fromEntries(x.split("\0").filter(Boolean).map(l=>{const n=l.indexOf(" ");return n<0?[l,""]:[l.slice(0,n),l.slice(n+1)]}))); const discover=(selected,repo,registered)=>{check(typeof selected==="string"&&selected.length>0&&!/[\r\n\0]/.test(selected)); const common=real(text(git(selected,"rev-parse","--path-format=absolute","--git-common-dir"))); check(path.basename(common)===".git"); const primary=path.dirname(common); check(real(text(git(primary,"rev-parse","--show-toplevel")))===primary&&real(text(git(primary,"rev-parse","--path-format=absolute","--git-common-dir")))===common&&origin(primary)===repo); const worktree=path.join(primary,"worktrees",id); if(registered){check(real(worktree)===worktree&&real(text(git(worktree,"rev-parse","--path-format=absolute","--git-common-dir")))===common); check(records(primary).filter(r=>r.worktree===worktree).length===1)} return {primary,common,worktree}}; const current=()=>real(text(git(process.cwd(),"rev-parse","--show-toplevel"))); const mapPath=(repo,root)=>path.join(root,"local-tmp",id,"evidence/runtime",repo,"phase-0",repo==="public"?"R-PUB":"R-PRI","execution-roots.json"); const ignored=(root,file)=>{check(fs.lstatSync(file).isFile()); git(root,"check-ignore","-q","--",file); check(git(root,"ls-files","--",file)==="")}; const validate=m=>{check(m&&typeof m==="object"&&!Array.isArray(m)&&Object.keys(m).sort().join(",")==="planId,privatePrimary,privateWorktree,publicPrimary,publicWorktree"); check(m.planId===id); for(const key of ["publicPrimary","privatePrimary","publicWorktree","privateWorktree"])check(typeof m[key]==="string"&&path.isAbsolute(m[key])&&!/[\r\n\0]/.test(m[key])); const a=discover(m.publicPrimary,"public",true),b=discover(m.privatePrimary,"private",true); check(a.primary!==b.primary&&a.common!==b.common&&a.primary===m.publicPrimary&&b.primary===m.privatePrimary&&a.worktree===m.publicWorktree&&b.worktree===m.privateWorktree); return m}; const load=expected=>{const repo=origin(process.cwd()); check(expected==="either"||repo===expected); const d=discover(process.cwd(),repo,true); check(current()===d.worktree); const file=mapPath(repo,d.worktree); ignored(d.worktree,file); const m=validate(JSON.parse(fs.readFileSync(file,"utf8"))); check(m[repo+"Worktree"]===current()); for(const other of ["public","private"]){const p=mapPath(other,m[other+"Worktree"]); ignored(m[other+"Worktree"],p); const peer=validate(JSON.parse(fs.readFileSync(p,"utf8"))); check(Object.keys(m).every(k=>m[k]===peer[k]))} return m}; const d=discover(process.cwd(),"private",false); process.stdout.write(JSON.stringify(d))'"'"')"; plan_primary="$(printf "%s" "$plan_identity" | rtk jq -r .primary)"; plan_worktree="$(printf "%s" "$plan_identity" | rtk jq -r .worktree)"; rtk git -C "$plan_primary" fetch origin main'
rtk bash -lc 'set -euo pipefail; plan_identity="$(rtk node -e '"'"'const fs=require("node:fs"),path=require("node:path"),cp=require("node:child_process"); const id="adopt-beavernest-test-automation"; const fail=()=>{throw Error("Execution root validation failed; stop and recheck the selected checkouts and Phase 0 evidence")}; const check=x=>{if(!x)fail()}; const real=x=>fs.realpathSync(x); const git=(root,...args)=>cp.execFileSync("git",["-C",root,...args],{encoding:"utf8",stdio:["ignore","pipe","pipe"]}); const text=x=>x.replace(/\n$/,""); const origin=root=>{const raw=text(git(root,"remote","get-url","origin")); let u; try{u=new URL(raw.replace(/^git@github\.com:/,"ssh://git@github.com/"))}catch{fail()} check(["https:","ssh:"].includes(u.protocol)&&u.hostname==="github.com"&&!u.port&&!u.search&&!u.hash); const name=u.pathname.replace(/^\//,"").replace(/\.git\/?$/,"").replace(/\/$/,""); check(["wahidyankf/ose-public","wahidyankf/ose-private"].includes(name)); return name.endsWith("ose-public")?"public":"private"}; const records=root=>git(root,"worktree","list","--porcelain","-z").split("\0\0").filter(Boolean).map(x=>Object.fromEntries(x.split("\0").filter(Boolean).map(l=>{const n=l.indexOf(" ");return n<0?[l,""]:[l.slice(0,n),l.slice(n+1)]}))); const discover=(selected,repo,registered)=>{check(typeof selected==="string"&&selected.length>0&&!/[\r\n\0]/.test(selected)); const common=real(text(git(selected,"rev-parse","--path-format=absolute","--git-common-dir"))); check(path.basename(common)===".git"); const primary=path.dirname(common); check(real(text(git(primary,"rev-parse","--show-toplevel")))===primary&&real(text(git(primary,"rev-parse","--path-format=absolute","--git-common-dir")))===common&&origin(primary)===repo); const worktree=path.join(primary,"worktrees",id); if(registered){check(real(worktree)===worktree&&real(text(git(worktree,"rev-parse","--path-format=absolute","--git-common-dir")))===common); check(records(primary).filter(r=>r.worktree===worktree).length===1)} return {primary,common,worktree}}; const current=()=>real(text(git(process.cwd(),"rev-parse","--show-toplevel"))); const mapPath=(repo,root)=>path.join(root,"local-tmp",id,"evidence/runtime",repo,"phase-0",repo==="public"?"R-PUB":"R-PRI","execution-roots.json"); const ignored=(root,file)=>{check(fs.lstatSync(file).isFile()); git(root,"check-ignore","-q","--",file); check(git(root,"ls-files","--",file)==="")}; const validate=m=>{check(m&&typeof m==="object"&&!Array.isArray(m)&&Object.keys(m).sort().join(",")==="planId,privatePrimary,privateWorktree,publicPrimary,publicWorktree"); check(m.planId===id); for(const key of ["publicPrimary","privatePrimary","publicWorktree","privateWorktree"])check(typeof m[key]==="string"&&path.isAbsolute(m[key])&&!/[\r\n\0]/.test(m[key])); const a=discover(m.publicPrimary,"public",true),b=discover(m.privatePrimary,"private",true); check(a.primary!==b.primary&&a.common!==b.common&&a.primary===m.publicPrimary&&b.primary===m.privatePrimary&&a.worktree===m.publicWorktree&&b.worktree===m.privateWorktree); return m}; const load=expected=>{const repo=origin(process.cwd()); check(expected==="either"||repo===expected); const d=discover(process.cwd(),repo,true); check(current()===d.worktree); const file=mapPath(repo,d.worktree); ignored(d.worktree,file); const m=validate(JSON.parse(fs.readFileSync(file,"utf8"))); check(m[repo+"Worktree"]===current()); for(const other of ["public","private"]){const p=mapPath(other,m[other+"Worktree"]); ignored(m[other+"Worktree"],p); const peer=validate(JSON.parse(fs.readFileSync(p,"utf8"))); check(Object.keys(m).every(k=>m[k]===peer[k]))} return m}; const d=discover(process.cwd(),"private",false); process.stdout.write(JSON.stringify(d))'"'"')"; plan_primary="$(printf "%s" "$plan_identity" | rtk jq -r .primary)"; plan_worktree="$(printf "%s" "$plan_identity" | rtk jq -r .worktree)"; test ! -e "$plan_worktree"; if rtk git -C "$plan_primary" show-ref --verify --quiet refs/heads/adopt-beavernest-test-automation; then exit 1; fi; rtk git -C "$plan_primary" worktree add -b adopt-beavernest-test-automation "$plan_worktree" origin/main'
```

If a branch or path exists, stop. Inspect `rtk git worktree list --porcelain` and the branch ledger;
never force, delete, or reuse an unproven worktree. Never edit `ose-private` through its primary
checkout.

### Portable execution roots

`R-PUB:` and `R-PRI:` are location labels, not shell syntax. They mean the validated public
and private primary checkouts selected by the executor. Append the suffix after the colon to that
root before selecting a tool's working directory. Thus `R-PUB:worktrees/adopt-beavernest-test-automation`
selects the public execution worktree; no checkout basename or sibling-folder layout is assumed.

Before provisioning, select each existing checkout explicitly from the execution context. If its
location is unknown, ask the user; do not search unrelated directories or guess a sibling. The
commands below derive the primary root from Git's absolute common directory and verify the
canonical GitHub owner/repository for accepted SSH or HTTPS origins without printing the remote.
Use each repository's own terminal/working directory. Every command resolves its inputs again;
no exported root variable, previous shell, or shell startup file is required. Paths are passed as
quoted arguments, never interpolated into program source or regexes. Newline-containing paths are
rejected explicitly rather than silently misread.

After both Phase 0 worktrees exist, their existing ignored Phase 0 evidence trees each hold the
same five-field `execution-roots.json`: `planId`, `publicPrimary`, `privatePrimary`,
`publicWorktree`, and `privateWorktree`. The root setup actions below create and verify these
runtime-only files. Every cross-repository command validates both files, both repository origins,
the current checkout, and registered worktree/common-directory identities before doing work.
Missing, malformed, moved, mismatched, or same-clone maps stop the command; correct the selected
locations and rerun the root setup actions, never bypass validation. Maps contain raw local roots:
never commit them, copy them to sanitized exports, or put them in `implementation-notes.md`.
Cleanup independently rediscovers the primary checkout and does not load maps from a deleted tree.

## How This Plan Ships

This plan originally carried a 4,817-item `DB`/`RP`/`OM` checklist ledger — a 53-step lifecycle
repeated across 91 bindings, plus prospective size gates, per-leaf allocation freezing, natural-seam
essays, shared-plumbing SHA tables, and roughly forty evidence files per delivery unit.

On 2026-09-01 the user replaced all of it with the process below, on the explicit basis that only
the end result matters. Nothing removed was enforced by anything outside this document: the
`O <= 1,000` and 300-file ceilings, the `PS-01`–`PS-03` prospective gates, and the exception records
were this plan's own paperwork, not repository policy and not CI.

What still binds is CI, and none of it is negotiable:

| Gate                                                                          | Enforced by              |
| ----------------------------------------------------------------------------- | ------------------------ |
| PR required; direct push to `main` blocked                                    | GitHub branch protection |
| `typecheck`, `lint`, `test:quick`, `specs:behavior:coverage`                  | `.NET quality gate`      |
| `test:coverage` at the 90% line threshold                                     | `.NET quality gate`      |
| `specs:structure-validation`                                                  | its own job              |
| governance, harness, markdown, specs, shell-docker-actions, formatting-verify | registry CI gate groups  |
| `parity-manifest.sha256` current                                              | pre-push gate and CI     |

Gherkin and specs work therefore cannot be skipped — `specs:behavior:coverage` is a CI job, and
`test:coverage` demands 90% line coverage. TDD stays for the same reason it was always here: this
plan's deliverable _is_ the test automation.

### Scope of this simplification

This withdrawal is scoped to **this plan's own delivery ledger and nothing else**. It amends no
repository rule. Every governance requirement in `AGENTS.md` and `repo-governance/` continues to
bind this plan exactly as it binds every other change in the repository — in particular the TDD
requirement, the Specs/Gherkin requirement for code changes, and the regression-test requirement for
bug fixes. Those are repository policy, enforced in CI; what was removed here was this document's
own bookkeeping about how to ship, which nothing outside this document ever read.

Read no precedent into this for any other plan. It is a one-off, granted by the user for this plan
on the basis that the ledger's cost had outgrown its value.

### Per-PR process

1. Implement.
2. `rtk nx affected -t build,typecheck,lint,test:quick,test:integration,test:e2e` — every applicable
   task exits 0.
3. `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push` — exit 0. Read the final
   PASS/FAIL summary line, not per-check text.
4. Push the delivery branch; open one PR to `main` with a short body stating scope and recovery.
5. One authenticated `pr-leak-review` against the exact head/base. A changed head — including one
   caused by a rebase — invalidates the record and requires exactly one replacement pass.
6. CI green on that same head.
7. Merge.

If a rebase is needed because `origin/main` moved, rerun steps 2, 3, 5, and 6 against the new head.

## Execution Table

Fifty-six public and twenty-one private leaves remain, batched into ten PRs. The two repositories
run as independent streams with their own worktrees, branches, and CI.

### Public stream — the critical path

| PR      | Scope                                | Leaves                                                                                                                       |
| ------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| `PUB-1` | Phase 4 remainder                    | `D-P4-PUB-LAYOUT-MANIFEST`, `D-P4-PUB-FIXTURES-A/B/C`, `D-P4-PUB-GOVERNANCE` (5)                                             |
| `PUB-2` | Phases 5, 6, 8A, 8B, 9, 10A          | `D-P5-PUB`, `D-O-PUB-CRANE`, `D-O-PUB-FS-CORE`, `D-O-PUB-FS-ENV`, `D-O-PUB-TS-ENV`, `D-O-PUB-WEB-TOKEN` (6)                  |
| `PUB-3` | Phase 7 shared Rhino                 | the ten `D-O-PUB-RHINO-*` leaves (10)                                                                                        |
| `PUB-4` | Phase 11A web-ui                     | the six `D-O-PUB-WEB-UI-*` leaves (6)                                                                                        |
| `PUB-5` | Phase 12 AyoKoding                   | the twenty-one `D-O-PUB-AYO-*` leaves (21)                                                                                   |
| `PUB-6` | Phases 14–19 and the public closeout | `D-O-PUB-OL-WEB`, `D-O-PUB-OL-BE`, `D-O-PUB-OL-WWW`, `D-O-PUB-OSE-WEB`, `D-O-PUB-OSE-BE`, `D-O-PUB-OSE-WWW`, `D-P20-PUB` (7) |

`PUB-5` carries twenty-one leaves and is the one unit at real risk of choking review or CI. Split it
first if anything strains; leave the others whole.

### Private stream

| PR      | Scope                                    | Leaves                                                                                               | Depends on       |
| ------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------------- |
| `PRI-1` | Phase 4 parity                           | `D-P4-PRI-REGISTRY-PARITY`, `D-P4-PRI-POLICY-PARITY`, `D-P4-PRI-FIXTURES`, `D-P4-PRI-GOVERNANCE` (4) | `PUB-1`          |
| `PRI-2` | Phase 5 and Phase 10B                    | `D-P5-PRI`, `D-O-PRI-TS-TOKEN` (2)                                                                   | `PRI-1`          |
| `PRI-3` | Phase 7 Rhino parity                     | the ten `D-O-PRI-RHINO-*` leaves (10)                                                                | `PUB-3`, `PRI-1` |
| `PRI-4` | Phase 11B ts-ui and the private closeout | the four `D-O-PRI-TS-UI-*` leaves, `D-P20-PRI` (5)                                                   | `PRI-1`          |

### What actually runs in parallel

No private unit can start before `PRI-1`. Every private owner migration is accepted against
`AC-TEST-*` and `AC-COVERAGE-*`, and the validators that enforce those criteria are built in
Phase 4 and reach `ose-private` only when `PRI-1` mirrors them. Until then a private migration
cannot be verified against the contract at all.

Once `PRI-1` has landed the two streams do run concurrently. `PRI-2` and `PRI-4` touch `ts-token`
and `ts-ui`, private-only projects with no public counterpart, so they proceed alongside `PUB-3`
through `PUB-6` without contending for a single path. `PRI-3` additionally waits for `PUB-3`,
because it mirrors it.

`PRI-1` and `PRI-3` are parity mirrors rather than fresh work: `apps/rhino-cli/` and
`specs/apps/rhino/` are byte-identical across the two repositories, so propagation is minutes.

Never mirror the whole tree. Sixteen files legitimately differ between the repositories, and
`ose-private` carries a GPG check that `ose-public` does not.

## Completed

| Binding             | PR           | Merge commit |
| ------------------- | ------------ | ------------ |
| `D-P1-PUB`          | —            | landed       |
| `D-P2-PUB`          | #408         | landed       |
| `D-P3-PUB`          | #420         | landed       |
| `D-P3-PRI`          | private #138 | landed       |
| `D-P4-PUB-REGISTRY` | #421         | landed       |
| `D-P4-PUB-BDD`      | #424         | `3b9caedd5`  |
| `D-P4-PUB-COVERAGE` | #425         | `6475963ad`  |

`D-O-PUB-WAHID` (Phase 13) is descoped: `apps/wahidyankf-www` was removed from the repository by a
separate workstream in PR #423. Its phase section is retained below for the record only.

### Evidence

Evidence is now the CI run itself plus one leak-review record per PR. Raw command output stays in
`local-tmp/adopt-beavernest-test-automation/` and is ignored on both sides; nothing under it is
tracked. `implementation-notes.md` remains the single tracked ledger — one sanitized line per merged
PR — and `learnings.md` changes only for a genuine learning. Private evidence never crosses into the
public repository except as sanitized aggregate facts.

The per-leaf evidence directories, control files, prospective manifests, and the
`EVIDENCE<TAB>...` row format the previous ledger required are all withdrawn.

## Executor Reading Contract

The intended executor is a junior engineer fresh from a bootcamp, with no professional work
experience and no repository or stack context, including no prior OSE, Nx, Rhino, or native-runner
knowledge.

- Perform actions in order. A later green aggregate does not prove an earlier checkbox.
- A valid `RED` fails for the named missing behavior. A crash or unrelated failure is invalid.
- `GREEN` adds only enough behavior to pass. `REFACTOR` changes structure without changing accepted
  behavior or diagnostics.
- Record every unexpected failure with command, exit code, first relevant error, root-cause fix, and
  successful rerun. Never weaken a gate.
- Use a Phase 0 ledger row only when it has exact paths, symbols, commands, expected output, and
  evidence location. Repair an incomplete row; never guess.
- Canonical Gherkin remains in [prd.md](./prd.md#acceptance-criteria); do not copy scenarios here.

## Phase 0: Provision, Align to Latest Main, and Freeze Evidence

### Outcome 0A — Safe matching worktrees exist

- **Input:** the two primary repository checkouts and pending paths.
- **Outcome:** both worktrees use latest fetched `origin/main`; primary checkouts remain untouched.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-08, AC-TEST-09, AC-TEST-10, AC-TEST-11, AC-REPO-01, and AC-DDD-01](./prd.md#acceptance-criteria).

### Outcome 0B — Baselines and conditional capabilities are explicit

- **Input:** initialized worktrees.
- **Outcome:** preexisting failures and conditional tools are known before implementation.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-08, AC-TEST-09, AC-TEST-10, AC-TEST-11, AC-REPO-01, and AC-DDD-01](./prd.md#acceptance-criteria).

### Outcome 0C — Stable owner rows remove later guesswork

- **Input:** stable IDs and current repository contents.
- **Outcome:** each later action has exact path/symbol/command/result/evidence.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-08, AC-TEST-09, AC-TEST-10, AC-TEST-11, AC-REPO-01, and AC-DDD-01](./prd.md#acceptance-criteria).

#### Controlled owner-row packet

Every `Freeze <owner-id>` checkbox below uses this packet; the checkbox is incomplete until all
nine fields are populated. Use only the finite assignments below—never infer a sibling.

| Owner             | Project                | Root                        | Corpus root                    | Owner file under repository evidence `phase-0/owners/` |
| ----------------- | ---------------------- | --------------------------- | ------------------------------ | ------------------------------------------------------ |
| `O-PUB-CRANE`     | `crane-cli`            | `apps/crane-cli`            | `specs/apps/crane`             | `O-PUB-CRANE.md`                                       |
| `O-PUB-RHINO`     | `rhino-cli`            | `apps/rhino-cli`            | `specs/apps/rhino`             | `O-PUB-RHINO.md`                                       |
| `O-PUB-FS-CORE`   | `fsharp-crane-core`    | `libs/fsharp-crane-core`    | `specs/libs/fsharp-crane-core` | `O-PUB-FS-CORE.md`                                     |
| `O-PUB-FS-ENV`    | `fsharp-env-loader`    | `libs/fsharp-env-loader`    | `specs/libs/fsharp-env-loader` | `O-PUB-FS-ENV.md`                                      |
| `O-PUB-TS-ENV`    | `ts-env-loader`        | `libs/ts-env-loader`        | `specs/libs/ts-env-loader`     | `O-PUB-TS-ENV.md`                                      |
| `O-PUB-WEB-TOKEN` | `web-ui-token`         | `libs/web-ui-token`         | `specs/libs/web-ui-token`      | `O-PUB-WEB-TOKEN.md`                                   |
| `O-PUB-WEB-UI`    | `web-ui`               | `libs/web-ui`               | `specs/libs/web-ui`            | `O-PUB-WEB-UI.md`                                      |
| `O-PUB-AYO`       | `ayokoding-www`        | `apps/ayokoding-www`        | `specs/apps/ayokoding`         | `O-PUB-AYO.md`                                         |
| `O-PUB-WAHID`     | `wahidyankf-www`       | `apps/wahidyankf-www`       | `specs/apps/wahidyankf`        | `O-PUB-WAHID.md`                                       |
| `O-PUB-OL-WEB`    | `organiclever-app-web` | `apps/organiclever-app-web` | `specs/apps/organiclever`      | `O-PUB-OL-WEB.md`                                      |
| `O-PUB-OL-BE`     | `organiclever-be`      | `apps/organiclever-be`      | `specs/apps/organiclever`      | `O-PUB-OL-BE.md`                                       |
| `O-PUB-OL-WWW`    | `organiclever-www`     | `apps/organiclever-www`     | `specs/apps/organiclever`      | `O-PUB-OL-WWW.md`                                      |
| `O-PUB-OSE-WEB`   | `ose-app-web`          | `apps/ose-app-web`          | `specs/apps/ose`               | `O-PUB-OSE-WEB.md`                                     |
| `O-PUB-OSE-BE`    | `ose-be`               | `apps/ose-be`               | `specs/apps/ose`               | `O-PUB-OSE-BE.md`                                      |
| `O-PUB-OSE-WWW`   | `ose-www`              | `apps/ose-www`              | `specs/apps/ose`               | `O-PUB-OSE-WWW.md`                                     |
| `O-PRI-RHINO`     | `rhino-cli`            | `apps/rhino-cli`            | `specs/apps/rhino`             | `O-PRI-RHINO.md`                                       |
| `O-PRI-TS-TOKEN`  | `ts-ui-tokens`         | `libs/ts-ui-tokens`         | `specs/libs/ts-ui-tokens`      | `O-PRI-TS-TOKEN.md`                                    |
| `O-PRI-TS-UI`     | `ts-ui`                | `libs/ts-ui`                | `specs/libs/ts-ui`             | `O-PRI-TS-UI.md`                                       |

Public owner files use
`local-tmp/adopt-beavernest-test-automation/evidence/runtime/public/phase-0/owners/`; private owner files
use `local-tmp/adopt-beavernest-test-automation/evidence/runtime/private/phase-0/owners/`. First capture the
machine-readable inputs with this command, substituting only the one selected table row and its
repository-specific owner-file prefix:

```bash
rtk bash -lc 'owner="<owner-id>"; project="<project>"; root="<root>"; corpus="<corpus-root>"; out="<owner-file>"; raw="${out%.md}.inputs"; rtk mkdir -p "$raw"; rtk nx show project "$project" --json > "$raw/project.json"; test "$(rtk jq -r .root "$raw/project.json")" = "$root"; rtk rg --files "$root" > "$raw/root-files.txt"; if test -d "$corpus"; then rtk rg --files "$corpus" > "$raw/corpus-files.txt"; else printf "_absent on execution base_\n" > "$raw/corpus-files.txt"; fi; { rtk rg -n "coverage|threshold|lcov|cobertura" "$root/project.json" "$root" --glob "!**/node_modules/**" || true; } > "$raw/coverage.txt"; { rtk rg -n "package.json|npm --prefix|publish|workspace" "$root/project.json" package.json nx.json "$root" --glob "!**/node_modules/**" || true; } > "$raw/manifest-consumers.txt"; { rtk rg -n "architecture.md|C4Context|C4Container|C4Component|flowchart|graph" "$corpus" 2>/dev/null || true; } > "$raw/c4.txt"; test -s "$raw/project.json"; test -s "$raw/root-files.txt"'
```

For redirected machine-readable inputs, execute the `npx nx` and `rg` capture legs natively inside
the outer `rtk bash -lc` command. Do not redirect the human-reporting `rtk` wrapper output into an
owner input file: the captured file must contain only project JSON or repository-relative paths.
Perform the public rows in the public execution worktree and the private rows in the private
execution worktree; an execution worktree never reads the other repository's ignored evidence.

Then write exactly this schema to the checkbox's owner file. Each value must cite one captured
input line or an explicit `_absent on execution base_`; `pending`, a blank value, and prose such as
“inspect later” are invalid.

```text
Project: <exact Nx name from project.json>
Root: <exact .root from project.json>
Targets: <exact target names and copyable commands from project.json>
Coverage: <native command, threshold, exclusions, outputs, or explicit absent result>
Corpus: <exact corpus paths/globs from corpus-files.txt, or explicit absent result>
C4: <exact README/architecture/Mermaid paths, or explicit absent result>
Manifest: <exact package.json plus named direct consumer, or delete with no-consumer proof>
Recovery: rtk git restore --source=origin/main -- <exact root and corpus paths>
Size: rtk git diff --numstat origin/main...HEAD -- <exact root and corpus paths>
```

Validate the row immediately with
`rtk bash -lc 'f="<owner-file>"; for label in Project Root Targets Coverage Corpus C4 Manifest Recovery Size; do test "$(rtk rg -c "^${label}: .+" "$f")" -eq 1 || { printf "invalid %s in %s\n" "$label" "$f" >&2; exit 1; }; done; ! rtk rg -n "(:[[:space:]]*$|pending|inspect later|unknown)" "$f"'`.
If coverage, manifest ownership, or C4 classification is not yet provable from the captured files,
stop that owner row and complete its bounded discovery; do not let the later aggregate ledger hide
the missing field.

- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.
>
> **Pause Safety:** Phase 0 is coherent at a natural pause only after every gate above passes. Safe
> to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`:
> `rtk bash -lc 'set -o pipefail; rtk git status --porcelain=v1 --untracked-files=all | while IFS= read -r row; do path="${row#???}"; case "$path" in plans/in-progress/adopt-beavernest-test-automation/delivery.md|plans/in-progress/adopt-beavernest-test-automation/implementation-notes.md|plans/in-progress/adopt-beavernest-test-automation/learnings.md) ;; *) printf "unexpected Phase 0 path: %s\n" "$path" >&2; exit 1 ;; esac; done'`.

## Phase 1: Retire OrganicLever DDD Engineering Surfaces

- **Input:** Phase 0 OrganicLever DDD delete/preserve rows in `R-PUB`.
- **Outcome:** no OrganicLever DDD spec/enforcement remains; preserved behavior stays green.
- **Acceptance criteria:** [AC-TEST-07, AC-TEST-08, AC-DDD-01, and AC-RULES-01](./prd.md#acceptance-criteria).

> **Execution state:** the 69 allocated implementation paths and their exact-head PR lifecycle are
> complete. The runtime ledger remains the authoritative Phase 1 validation record.

- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### `RP-P1-PUB`

### Phase 1 Gate

> All checks below must pass before starting Phase 2.
>
> **Pause Safety:** Phase 1 is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx affected -t build,test:quick,lint`.

### `D-P1-PUB` delivery lifecycle

## Phase 2: Retire OSE DDD Engineering Surfaces

- **Input:** Phase 0 OSE DDD delete/preserve rows in `R-PUB`.
- **Outcome:** no OSE DDD spec/enforcement remains; generic machinery waits for Phase 3.
- **Acceptance criteria:** [AC-TEST-07, AC-TEST-08, AC-DDD-01, and AC-RULES-01](./prd.md#acceptance-criteria).

> **Execution state:** the 24 allocated implementation paths are prepared after the enforced
> `repo-config.yml` closure. The runtime ledger records the finite classification, prospective
> validation, and later exact-head delivery checks.

- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### `RP-P2-PUB`

### Phase 2 Gate

> All checks below must pass before starting Phase 3.
>
> **Pause Safety:** Phase 2 is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx affected -t build,test:quick,lint`.

### `D-P2-PUB` delivery lifecycle

## Phase 3: Retire Rhino and Generic DDD Machinery

- **Input:** both DDD rows and shared Rhino parity paths.
- **Outcome:** DDD tooling/specs/tests are absent in both repos; shared Rhino stays byte-identical.
- **Acceptance criteria:** [AC-TEST-07, AC-TEST-08, AC-REPO-01, AC-DDD-01, and AC-RULES-01](./prd.md#acceptance-criteria).

> **Execution state:** `D-P3-PUB` and `D-P3-PRI` deliver together. `RhinoCli.Application/src/Ddd.fs`
> and `Glossary.fs`, their step files, the `specs domain-coverage validate` route, the
> `repo-config.yml` `specs:` section, and the `specs:domain:coverage` Nx targets are removed in both
> repositories; `specs validate-adoption` now reports a surviving retired `ddd/` tree instead of a
> missing `bounded-contexts.yaml`. `apps/rhino-cli` and `specs/apps/rhino` stay byte-identical across
> the two repositories, verified by index-blob comparison and a regenerated
> `apps/rhino-cli/parity-manifest.sha256`. Deletions carry the retired surface out of `docs/`,
> `repo-governance/`, and the `.claude/` skill and agent sources; the `docs/reference` triage record
> keeps its history behind a retirement note.

- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### `RP-P3-PUB`

### `RP-P3-PRI`

### Phase 3 Gate

> All checks below must pass before starting Phase 4.
>
> **Pause Safety:** Phase 3 is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run rhino-cli:test:quick`.

### `D-P3-PUB` delivery lifecycle

### `D-P3-PRI` delivery lifecycle

## Phase 4: Build the Enforcement Foundation

- **Input:** the initialized and populated public/private
  `evidence/phase-0/rules-subject-ledger.md` files, target contract, Rhino grammar, and runner
  fixtures.
- **Outcome:** registry, exact BDD, 99%, layout, and manifest invalid states fail clearly.

- **Acceptance criteria:** [AC-TEST-01, AC-TEST-03, AC-TEST-04, AC-TEST-10, AC-TEST-11, AC-TEST-12, AC-COVERAGE-01, AC-COVERAGE-02, AC-COVERAGE-03, AC-REPO-01, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### Outcome 4A — Registry and migration schema

- **Input:** `repo-config.yml`, `apps/rhino-cli/src/RhinoCli.Application/src/RepoConfig.fs`, and the
  current project set from `rtk nx show projects --json` in each worktree.
- **Outcome:** every Nx project has exactly one typed owner/profile/migration-state registry row,
  one immutable-legacy-to-canonical compatibility map, and a valid behavior lifecycle state.
- **Acceptance criteria:** [AC-TEST-01 and AC-REPO-01](./prd.md#acceptance-criteria).

#### `D-P4-PUB-REGISTRY` leaf delivery

### Outcome 4B — Exact Gherkin/BDD

- **Input:** `TestContract.fs`, recursive `specs/apps/**` and `specs/libs/**` discovery, and current
  `specs:behavior:coverage` behavior.
- **Outcome:** one missing feature, expanded example, scenario, step, binding, or applicable adapter
  fails by exact integer identity; rounded display never controls the gate.
- **Acceptance criteria:** [AC-TEST-02, AC-TEST-03, AC-TEST-04, and AC-TEST-12](./prd.md#acceptance-criteria).

#### `D-P4-PUB-BDD` leaf delivery

### Outcome 4C — Native 99% enforcement

- **Input:** native coverage targets in every `apps/**/project.json` and `libs/**/project.json`, plus
  registry layer applicability.
- **Outcome:** each governed numeric slice enforces native line coverage at least 99%, and policy
  rejects every weaker/missing/fake declaration.
- **Acceptance criteria:** [AC-COVERAGE-01, AC-COVERAGE-02, and AC-COVERAGE-03](./prd.md#acceptance-criteria).

#### `D-P4-PUB-COVERAGE` leaf delivery

### Outcome 4D — Physical roots and manifest ownership

- **Input:** current test paths, runner globs, project-local manifests, and direct consumers.
- **Outcome:** executable tests have one physical layer and every project manifest is either a real
  direct boundary or absent with commands owned by `project.json`.
- **Acceptance criteria:** [AC-TEST-10 and AC-TEST-11](./prd.md#acceptance-criteria).

#### `D-P4-PUB-LAYOUT-MANIFEST` leaf delivery

#### Outcome 4D.1 — Public owner fixture leaves

Each fixture leaf uses only its frozen allocation. These are executable test slices, so each keeps
the RED/GREEN/REFACTOR learning signal before its own PR lifecycle.

#### `D-P4-PUB-FIXTURES-A` leaf delivery

#### `D-P4-PUB-FIXTURES-B` leaf delivery

#### `D-P4-PUB-FIXTURES-C` leaf delivery

### Outcome 4E — Same contract in both repositories

- **Input:** the green public Rhino foundation and the current shared-path parity manifest.
- **Outcome:** private Rhino implements the identical testing contract without a second design.
- **Acceptance criteria:** [AC-REPO-01 and AC-RULES-01](./prd.md#acceptance-criteria).

#### `D-P4-PRI-REGISTRY-PARITY` leaf delivery

#### `D-P4-PRI-POLICY-PARITY` leaf delivery

#### `D-P4-PRI-FIXTURES` leaf delivery

### `RP-P4-PUB`

#### `D-P4-PUB-GOVERNANCE` leaf delivery

### `RP-P4-PRI`

#### `D-P4-PRI-GOVERNANCE` leaf delivery

### Phase 4 Gate

> All checks below must pass before starting Phase 5.
>
> **Pause Safety:** Phase 4 is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run rhino-cli:test:unit`.

#### `D-P4-PUB` prospective closeout gate

#### `D-P4-PRI` prospective closeout gate

## Phase 5: Build the Specs/C4 Logical-Corpus Foundation

- **Input:** Phase 0 specs/C4 map and [specs contract](./tech-docs/specs-structure-and-c4.md).
- **Outcome:** one README, as-built `architecture.md`, and recursive `behaviors/` per owner.
- **Acceptance criteria:** [AC-TEST-02, AC-SPECS-01, AC-C4-01, AC-C4-02, and AC-RULES-01](./prd.md#acceptance-criteria).

- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### `RP-P5-PUB`

### `RP-P5-PRI`

### Phase 5 Gate

> All checks below must pass before starting Phase 6.
>
> **Pause Safety:** Phase 5 is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run rhino-cli:specs:structure-validation`.

### `D-P5-PUB` delivery lifecycle

> **Execution state:** Phase 4 landed as `ose-public#428`, `ose-public#429`, and `ose-private#140`;
> the two repositories carry a byte-identical 226-entry parity manifest.
>
> Phase 5 does not fit one delivery unit. The corpus move touches roughly 200 specification files
> and 641 files that reference their paths, so a single PR would break both the 20-file review
> budget and rule 1. The [Atomicity Exception](../../../repo-governance/conventions/structure/plans/prs-open-at-delivery-boundaries-pr-size-atomicity.md)
> does not apply, because smaller build-valid seams exist: one per product family. The phase
> therefore ships as a sequence, each unit independently green on `main`:
>
> 1. the validator learns the logical owner-corpus shape and keeps accepting the legacy five-folder
>    tree, so no family is broken by the rule change alone;
> 2. one unit per family — `rhino` with `crane`, `libs`, `ose`, `organiclever`, `ayokoding` —
>    moving that family's corpus and every reference to it; and
> 3. the validator drops legacy support once no family declares it.
>
> Detection is positive rather than negative: a product is measured against the new shape as soon as
> one of its immediate subdirectories carries an `architecture.md`. That is what makes a per-family
> sequence safe — an unmigrated family keeps its old rules until its own unit lands.
>
> Step 1 landed as `ose-public#430`. The two CLI families move together because they are the only
> two products the legacy `CLI-only` convention row names as its example: migrating one alone would
> leave that row describing a shape no product uses while still claiming one does. `rhino` is a
> parity path, so its move carries an identical `ose-private` landing; `crane` exists only here.
>
> Step 1 and the two CLI families landed as `ose-public#430` and `ose-public#431`, mirrored into
> `ose-private#141`, which restored the byte-identical parity boundary. The remaining families
> followed: `ayokoding` (`ose-public#432`), `libs` (`ose-public#433`), `organiclever`
> (`ose-public#434`), `ose` (`ose-public#435`). Step 3 — dropping legacy five-folder-tree support
> once no family declared it — landed as `ose-public#436`, with the documentation-surface retirement
> as `ose-public#437`. Phase 5 is fully complete: every family carries the logical owner-corpus
> shape and the validator no longer accepts the legacy tree.

### `D-P5-PRI` delivery lifecycle

> **Execution state:** Landed as `ose-private#141` (Rhino corpus, mirroring `D-P5-PUB` step 1/CLI
> families) and `ose-private#142` (the remaining `libs` family — `ts-ui`, `ts-ui-tokens`). All three
> private owners (`specs/apps/rhino/cli`, `specs/libs/ts-ui`, `specs/libs/ts-ui-tokens`) now carry
> the logical owner-corpus shape (one README, an as-built `architecture.md`, recursive `behaviors/`)
> and each independently passes `specs counts validate` with 0 findings. `ose-private` never carries
> the `crane`/`ayokoding`/`organiclever`/`ose` families `D-P5-PUB` migrated, since those projects
> exist only in `ose-public`; the private mirror's scope is exactly the private project inventory.
> No separate validator change was needed here: `rhino-cli` is the shared, parity-mirrored binary,
> so `D-P5-PUB` step 3 (dropping legacy five-folder-tree support) already governs both repositories
> the moment it landed in `ose-public`.

## Phase 6: Migrate `O-PUB-CRANE`

- **Input:** complete `O-PUB-CRANE` Phase 0 row and merged foundations.
- **Outcome:** Crane satisfies physical layers, native 99%, exact BDD, specs/C4, and direct targets.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-03, AC-TEST-04, AC-TEST-05, AC-TEST-06, AC-TEST-08, AC-TEST-10, AC-TEST-11, AC-TEST-12, AC-SPECS-01, AC-C4-01, AC-C4-02, AC-COVERAGE-01, AC-COVERAGE-02, AC-COVERAGE-03, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### `RP-OWNER-O-PUB-CRANE`

### Phase 6 Gate

> All checks below must pass before starting Phase 7.
>
> **Pause Safety:** Phase 6 is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --projects=crane-cli`.

### `D-O-PUB-CRANE` delivery lifecycle

> **Execution state:** Landed on `phase8-10-owners` alongside 8A/8B/9/10A. The registry already
> carried `crane-cli` as `active`/`verified` with a real corpus and driver from the separately
> merged `ose-public#438`/`#439` (Gherkin restoration and integration-tier retirement); this closed
> the remaining gap — `project.json` had no `test:layout:validation`/`coverage:policy:validation`/
> `package-manifest:policy:validation` targets and was still at the pre-migration 95% coverage
> threshold. Moved to 99% (100% actual, 135 tests) and added the three targets, all green against
> the real project. PR: [wahidyankf/ose-public#440](https://github.com/wahidyankf/ose-public/pull/440).

## Phase 7: Migrate Shared Rhino

- **Input:** complete public/private Rhino rows and the parity command.
- **Outcome:** both Rhino owners satisfy the contract with byte-identical shared paths.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-03, AC-TEST-04, AC-TEST-05, AC-TEST-06, AC-TEST-08, AC-TEST-10, AC-TEST-11, AC-TEST-12, AC-SPECS-01, AC-C4-01, AC-C4-02, AC-COVERAGE-01, AC-COVERAGE-02, AC-COVERAGE-03, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

Execute the public and private actions independently; one checkbox is one repository action.

### `D-O-PUB-RHINO` owner actions

#### `D-O-PUB-RHINO-UNIT` leaf delivery

#### `D-O-PUB-RHINO-INTEGRATION-E2E` leaf delivery

#### `D-O-PUB-RHINO-CONTRACT` leaf delivery

#### `D-O-PUB-RHINO-CORPUS-METADATA` leaf delivery

#### `D-O-PUB-RHINO-CORPUS-HARNESS` leaf delivery

#### `D-O-PUB-RHINO-CORPUS-SPECS` leaf delivery

#### `D-O-PUB-RHINO-CORPUS-DOCUMENTS` leaf delivery

#### `D-O-PUB-RHINO-CORPUS-GOVERNANCE` leaf delivery

#### `D-O-PUB-RHINO-CORPUS-GATES-SYSTEM` leaf delivery

#### `D-O-PUB-RHINO-CORPUS-COVERAGE-ENV` leaf delivery

### `D-O-PRI-RHINO` owner actions

#### `D-O-PRI-RHINO-UNIT` leaf delivery

#### `D-O-PRI-RHINO-INTEGRATION-E2E` leaf delivery

#### `D-O-PRI-RHINO-CONTRACT` leaf delivery

#### `D-O-PRI-RHINO-CORPUS-METADATA` leaf delivery

#### `D-O-PRI-RHINO-CORPUS-HARNESS` leaf delivery

#### `D-O-PRI-RHINO-CORPUS-SPECS` leaf delivery

#### `D-O-PRI-RHINO-CORPUS-DOCUMENTS` leaf delivery

#### `D-O-PRI-RHINO-CORPUS-GOVERNANCE` leaf delivery

#### `D-O-PRI-RHINO-CORPUS-GATES-SYSTEM` leaf delivery

#### `D-O-PRI-RHINO-CORPUS-COVERAGE-ENV` leaf delivery

Run parity in both repositories before merging either side; a non-zero
difference blocks both merges.

### `RP-OWNER-O-PUB-RHINO`

### `RP-OWNER-O-PRI-RHINO`

### Phase 7 Gate

> All checks below must pass before starting Phase 8A.
>
> **Pause Safety:** Phase 7 is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --projects=rhino-cli`.

### `D-O-PUB-RHINO` delivery lifecycle

> **Execution state:** Landed on `phase7-shared-rhino`. Relocated `apps/rhino-cli/src/tests` to
> `apps/rhino-cli/tests` (unit + integration), wired the three new Nx targets
> (`test:layout:validation`, `coverage:policy:validation`, `package-manifest:policy:validation`),
> and raised per-assembly line coverage to 99% across all four modules (`RhinoCli.Application`,
> `RhinoCli.Cli`, `RhinoCli.Infrastructure`, `RhinoCli.Domain`). Closing the coverage gap surfaced
> and fixed several real production bugs: an unhandled crash in the three-level runtime cross-check
> on a malformed `--unit-report` file, two unhandled-exception paths in `Harness.fs` (unwritable
> `.codex/agents`, unreadable `.claude/skills`), and a `Dispatch.fs` flag parser silently swallowing
> `--max-label-len`/`--max-width`/`--max-depth`/`--max-subgraph-nodes` values as bogus positional
> paths. `parity-manifest.sha256` regenerated and verified byte-identical against the companion
> `ose-private` PR. CI (ubuntu-latest) caught one macOS-only test — a `doctor --fix` assertion
> hardcoded the darwin `xcode-select --install` remediation string, never exercising the linux
> `sudo apt-get install -y git` branch it also covers; fixed by branching the expectation on
> `RuntimeInformation.IsOSPlatform`, matching the file's existing Playwright-cache-dir pattern.
> Two clean current-head `ose-pr-leak-review:v1` passes (0 findings each) precede the final merge.
> PR: [wahidyankf/ose-public#442](https://github.com/wahidyankf/ose-public/pull/442).

### `D-O-PRI-RHINO` delivery lifecycle

> **Execution state:** Landed on `phase7-rhino-parity`, mirroring `D-O-PUB-RHINO`'s relocation and
> Nx-target wiring (`test:layout:validation`, `coverage:policy:validation`,
> `package-manifest:policy:validation`); `parity-manifest.sha256` regenerated and confirmed
> byte-identical against the companion `ose-public` PR via a full cross-repo `diff -rq`. The
> mandatory `pr-leak-review` pass on the initial head found a real finding —
> `apps/rhino-cli/tests/unit/coverage.json`, newly tracked by the relocation, embeds the committing
> machine's absolute worktree path as coverlet's JSON dictionary keys (`machine_specific_absolute_path:
1`), matching a defect class already fixed for `fsharp-crane-core`/`fsharp-env-loader` on the
> `ose-public` side. The actual untrack took three attempts: the first two used
> `git commit --only -- ... coverage.json`, and `--only` re-includes a named path's current
> working-tree content when building its temporary commit index regardless of a preceding
> `git rm --cached` (which only clears the index entry, never the disk file) — so both silently
> re-committed the same leaking blob. The real fix staged the deletion and committed with no
> `--only` pathspec at all, confirmed via `git ls-tree` and the GitHub trees API showing the path
> genuinely absent. `coverage.json` is now gitignored to prevent recurrence. A third
> `pr-leak-review` pass came back fully clean (0 findings) on the corrected head. CI then failed a
> second, different test — `pruneOrphans tolerates a crate whose target symlink has a malformed
(empty-string) raw target` — a genuine kernel-level OS difference rather than a flaky test:
> macOS/BSD's `symlink(2)` accepts an empty-string target at the syscall level, but Linux's rejects
> it outright (`ENOENT`), so the on-disk artifact the test needs cannot be constructed there at all;
> branched the malformed-target assertions on `RuntimeInformation.IsOSPlatform(OSX)`, keeping the OS
> refusal and ordinary orphan-pruning assertions on every platform. A fourth `pr-leak-review` pass
> came back fully clean (0 findings) on the corrected head. Merged: `ose-public#442` (`666211904`)
> and `ose-private#143` (`16ef644507`).
> PR: [wahidyankf/ose-private#143](https://github.com/wahidyankf/ose-private/pull/143).

## Phase 8A: Migrate `O-PUB-FS-CORE`

- **Input:** complete `O-PUB-FS-CORE` row and integration applicability evidence.
- **Outcome:** the core library satisfies every applicable layer and delegated boundary.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-03, AC-TEST-04, AC-TEST-05, AC-TEST-06, AC-TEST-08, AC-TEST-10, AC-TEST-11, AC-TEST-12, AC-SPECS-01, AC-C4-01, AC-C4-02, AC-COVERAGE-01, AC-COVERAGE-02, AC-COVERAGE-03, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### `RP-OWNER-O-PUB-FS-CORE`

### Phase 8A Gate

> All checks below must pass before starting Phase 8B.
>
> **Pause Safety:** Phase 8A is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --projects=fsharp-crane-core`.

### `D-O-PUB-FS-CORE` delivery lifecycle

> **Execution state:** Landed on `phase8-10-owners` alongside 8B/9/10A. `fsharp-crane-core`'s
> `test:coverage` threshold moved 95% to 99% (`/p:Include=[crane]*`, 99.83% actual, 104 tests);
> `test:layout:validation`, `coverage:policy:validation`, and `package-manifest:policy:validation`
> targets added and green (`native-layout-valid ... executable=13`, `coverage-policy-valid ...
threshold=99`, `manifest-not-present`). A real production bug surfaced during this work —
> `PdfExtractionCache.fs`'s `CachedExtraction` record was `type private`, capping property
> visibility below what `System.Text.Json`'s reflection converter needs, so every cache write
> serialized as `{}` and every read silently fell through to the inner port; fixed by dropping
> `private`, with two permanent call-counting regression tests replacing the diagnostic spike.
> PR: [wahidyankf/ose-public#440](https://github.com/wahidyankf/ose-public/pull/440).

## Phase 8B: Migrate `O-PUB-FS-ENV`

- **Input:** complete `O-PUB-FS-ENV` row, its Phase-4 `bootstrap` seed contract, compatibility map,
  and integration applicability evidence.
- **Outcome:** the env library first activates a real corpus/driver without behavior loss, then
  satisfies every applicable layer and delegated boundary.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-03, AC-TEST-04, AC-TEST-05, AC-TEST-06, AC-TEST-08, AC-TEST-10, AC-TEST-11, AC-TEST-12, AC-SPECS-01, AC-C4-01, AC-C4-02, AC-COVERAGE-01, AC-COVERAGE-02, AC-COVERAGE-03, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.
  evidence.

For this 17-path implementation unit, every owner/rules evidence pathname below is a logical label resolved to the
ignored runtime roots
`local-tmp/adopt-beavernest-test-automation/evidence/runtime/public/{owners/D-O-PUB-FS-ENV,rules/RP-OWNER-O-PUB-FS-ENV}/`.
Do not create those literal `plans/in-progress/.../evidence/owners` or `evidence/rules` paths. Append
only their sanitized terminal rows to the allocated `implementation-notes.md`; `delivery.md` carries
checklist state, `learnings.md` changes only for a genuine learning, and raw outputs remain ignored.

### `RP-OWNER-O-PUB-FS-ENV`

The foundation deliveries already established the applicable canonical rules and enforcement. This
owner packet is therefore a no-change propagation verification: inventory and disposition evidence
remain required, but this packet may not edit governance or binding sources, generated-binding
commands must produce no diff, and the final manifest records `verified unchanged`. If the inventory
finds a real rule change, stop this 17-path implementation allocation and plan a separate finite rules unit; do not
widen the owner allocation.

### Phase 8B Gate

> All checks below must pass before starting Phase 9.
>
> **Pause Safety:** Phase 8B is coherent at a natural pause only after every gate above passes. Safe
> to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk
apps/rhino-cli/scripts/rhino-bin.sh test-contract registry validate --require-behavior-state
active`, `rtk apps/rhino-cli/scripts/rhino-bin.sh test-contract registry validate-mapping --all`,
> and `rtk nx run-many -t
test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation
--projects=fsharp-env-loader`. (The original `test:behavior:seed`-then-activate two-step never
> shipped a `test:behavior:seed` target — see the Execution state below — so `registry
validate`/`validate-mapping` take no `--project` filter; both are whole-registry commands.)

### `D-O-PUB-FS-ENV` delivery lifecycle

> **Execution state:** Landed on `phase8-10-owners` alongside 8A/9/10A. `fsharp-env-loader` was the
> registry's only remaining `bootstrap` row (`corpus: []`, a `seed:` block, no `specs/libs/`
> tree) — this phase activated it directly to `active` in one step rather than the two-step
> seed-then-activate the plan envisioned, since a real corpus and driver could be authored in the
> same delivery: `specs/libs/fsharp-env-loader/behaviors/{env-tier,port-resolver}/*.feature` (36
> scenarios, port-resolver mirroring `ts-env-loader`'s canonical corpus 1:1 since `PortResolver.fs`
> already documented itself as a byte-for-byte behavioral mirror) plus a single TickSpec driver,
> `tests/unit/Behavior/FsharpEnvLoaderBehaviorDriver.fs`, executing every scenario for real rather
> than binding no-op steps. `test:coverage` threshold moved 95% to 99% (100% actual after changing
> `PortResolver.fs`'s `minPort`/`maxPort` from plain `let` bindings to `[<Literal>]` — a plain
> `let`'s module `.cctor` line is coverlet-invisible even though every port-bound test forces it to
> run, while a true compile-time constant has no `.cctor` to miscount). `registry validate
--require-behavior-state active` now reports `bootstrap:0,active:24` — no bootstrap owner remains
> anywhere in the registry. One real concurrency bug surfaced and was fixed during this work: the
> env-tier scenarios mutate real process environment variables (`APP_ENV` and friends), which raced
> under xunit's default one-collection-per-module parallelism exactly as
> `apps/rhino-cli/src/tests/unit/Steps/GitRootUnitTests.fs` already documents; fixed with the same
> assembly-wide `[<assembly: CollectionBehavior(DisableTestParallelization = true)>]` opt-out.
> PR: [wahidyankf/ose-public#440](https://github.com/wahidyankf/ose-public/pull/440).

## Phase 9: Migrate `O-PUB-TS-ENV`

- **Input:** complete `O-PUB-TS-ENV` row and integration applicability evidence.
- **Outcome:** TypeScript env loading satisfies every applicable layer and delegated boundary.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-03, AC-TEST-04, AC-TEST-05, AC-TEST-06, AC-TEST-08, AC-TEST-10, AC-TEST-11, AC-TEST-12, AC-SPECS-01, AC-C4-01, AC-C4-02, AC-COVERAGE-01, AC-COVERAGE-02, AC-COVERAGE-03, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### `RP-OWNER-O-PUB-TS-ENV`

### Phase 9 Gate

> All checks below must pass before starting Phase 10A.
>
> **Pause Safety:** Phase 9 is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --projects=ts-env-loader`.

### `D-O-PUB-TS-ENV` delivery lifecycle

> **Execution state:** Landed on `phase8-10-owners` alongside 8A/8B/10A. `ts-env-loader`'s coverage
> threshold moved 90% to 99% (108 tests, 100% lines); its three `*.unit.test.ts` files and
> `tokens-export.steps.ts`'s TS sibling moved from `src/` into `tests/unit/` (import paths fixed:
> `./index` to `../../src/index`), and `vitest.config.ts`'s `include` moved from `src/**` to
> `tests/unit/**`. `test:layout:validation`, `coverage:policy:validation`, and
> `package-manifest:policy:validation` targets added and green (`native-layout-valid ...
executable=3`, `coverage-policy-valid ... threshold=99`, `manifest-consumer-verified`).
> PR: [wahidyankf/ose-public#440](https://github.com/wahidyankf/ose-public/pull/440).

## Phase 10A: Migrate `O-PUB-WEB-TOKEN`

- **Input:** complete public token row and delegated-boundary evidence.
- **Outcome:** public tokens satisfy unit, specs, exact BDD, 99%, and direct-target rules.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-03, AC-TEST-04, AC-TEST-05, AC-TEST-06, AC-TEST-08, AC-TEST-10, AC-TEST-11, AC-TEST-12, AC-SPECS-01, AC-C4-01, AC-C4-02, AC-COVERAGE-01, AC-COVERAGE-02, AC-COVERAGE-03, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### `RP-OWNER-O-PUB-WEB-TOKEN`

### Phase 10A Gate

> All checks below must pass before starting Phase 10B.
>
> **Pause Safety:** Phase 10A is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --projects=web-ui-token`.

### `D-O-PUB-WEB-TOKEN` delivery lifecycle

> **Execution state:** Landed on `phase8-10-owners` alongside 8A/8B/9. `web-ui-token`'s
> `test:coverage` target was an echo placeholder (`AC-COVERAGE`-vacuous); replaced with a real `npx
vitest run --coverage --coverage.thresholds.lines=99` (6 tests, 100% lines).
> `test:layout:validation`, `coverage:policy:validation`, and `package-manifest:policy:validation`
> targets added and green (`native-layout-valid ... executable=1`, `coverage-policy-valid ...
threshold=99`, `manifest-consumer-verified`).
> PR: [wahidyankf/ose-public#440](https://github.com/wahidyankf/ose-public/pull/440).

## Phase 10B: Migrate `O-PRI-TS-TOKEN`

- **Input:** complete private token row and delegated-boundary evidence.
- **Outcome:** private tokens satisfy unit, specs, exact BDD, 99%, and direct-target rules.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-03, AC-TEST-04, AC-TEST-05, AC-TEST-06, AC-TEST-08, AC-TEST-10, AC-TEST-11, AC-TEST-12, AC-SPECS-01, AC-C4-01, AC-C4-02, AC-COVERAGE-01, AC-COVERAGE-02, AC-COVERAGE-03, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### `RP-OWNER-O-PRI-TS-TOKEN`

### Phase 10B Gate

> All checks below must pass before starting Phase 11A.
>
> **Pause Safety:** Phase 10B is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PRI:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --projects=ts-ui-tokens`.

### `D-O-PRI-TS-TOKEN` delivery lifecycle

> **Execution state:** `ts-ui-tokens` moved from a `src`-colocated echo-stub test contract to the
> target shape following the `web-ui-token` pattern: tests relocated to `tests/unit/`,
> `test:coverage` raised to a 99% line floor, and `test:layout:validation`/
> `coverage:policy:validation`/`package-manifest:policy:validation` added. Leak-review clean, CI
> green. PR: [wahidyankf/ose-private#144](https://github.com/wahidyankf/ose-private/pull/144),
> merge commit `b79ec552a14a244a85f5cc77d511ae09287ae6cf`.

## Phase 11A: Migrate `O-PUB-WEB-UI`

- **Input:** complete public UI row and component/delegated-boundary evidence.
- **Outcome:** public UI satisfies every applicable layer and direct-target rule.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-03, AC-TEST-04, AC-TEST-05, AC-TEST-06, AC-TEST-08, AC-TEST-10, AC-TEST-11, AC-TEST-12, AC-SPECS-01, AC-C4-01, AC-C4-02, AC-COVERAGE-01, AC-COVERAGE-02, AC-COVERAGE-03, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### Leaf deliveries

#### `D-O-PUB-WEB-UI-UNIT` leaf delivery

#### `D-O-PUB-WEB-UI-INTEGRATION-E2E` leaf delivery

#### `D-O-PUB-WEB-UI-CONTRACT` leaf delivery

#### `D-O-PUB-WEB-UI-CORPUS-METADATA` leaf delivery

#### `D-O-PUB-WEB-UI-CORPUS-CONTROLS` leaf delivery

#### `D-O-PUB-WEB-UI-CORPUS-COMPOSITION` leaf delivery

### `RP-OWNER-O-PUB-WEB-UI`

### Phase 11A Gate

> All checks below must pass before starting Phase 11B.
>
> **Pause Safety:** Phase 11A is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --projects=web-ui`.

### `D-O-PUB-WEB-UI` delivery lifecycle

> **Execution state:** `web-ui` moved from a `src`-colocated 70%-floor test contract to the target
> shape: unit tests relocated to `tests/unit/`, the `e2e/` visual-regression Playwright suite
> relocated to `tests/integration/` and wired to a real `test:integration` target (previously a
> no-op), `test:coverage` raised to a 99% line floor, the three policy-validation targets added, and
> `repo-config.yml` registered for both unit and integration runtimes. Also fixed a dangling
> `wahidyankf.css` import/theme entry in `.storybook/preview.ts`, broken by an unrelated in-flight
> `wahidyankf-www` removal elsewhere in the org. Leak-review clean (0 findings). CI green (575
> passed, 3 skipped — a pre-existing `@visual`-tagged Gherkin scenario excluded via
> `describeFeature`'s `excludeTags`, not a banned skip pattern; verified pre-existing on
> `origin/main` before this migration). PR:
> [wahidyankf/ose-public#443](https://github.com/wahidyankf/ose-public/pull/443), merge commit
> `dabe37a9a73abf435984180c1bf6339bf901f8fc`.

## Phase 11B: Migrate `O-PRI-TS-UI`

- **Input:** complete private UI row and component/delegated-boundary evidence.
- **Outcome:** private UI satisfies every applicable layer and direct-target rule.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-03, AC-TEST-04, AC-TEST-05, AC-TEST-06, AC-TEST-08, AC-TEST-10, AC-TEST-11, AC-TEST-12, AC-SPECS-01, AC-C4-01, AC-C4-02, AC-COVERAGE-01, AC-COVERAGE-02, AC-COVERAGE-03, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### Leaf deliveries

#### `D-O-PRI-TS-UI-UNIT` leaf delivery

#### `D-O-PRI-TS-UI-INTEGRATION-E2E` leaf delivery

#### `D-O-PRI-TS-UI-CONTRACT` leaf delivery

#### `D-O-PRI-TS-UI-CORPUS` leaf delivery

### `RP-OWNER-O-PRI-TS-UI`

### Phase 11B Gate

> All checks below must pass before starting Phase 12.
>
> **Pause Safety:** Phase 11B is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PRI:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --projects=ts-ui`.

### `D-O-PRI-TS-UI` delivery lifecycle

> **Execution state:** `ts-ui` moved from a `src`-colocated 70%-floor test contract to the target
> shape, mirroring `web-ui`'s pattern: unit tests relocated to `tests/unit/`, the `e2e/`
> visual-regression Playwright suite relocated to `tests/integration/` and wired to a real
> `test:integration` target (previously a no-op), `test:coverage` raised to a 99% line floor (100%
> achieved), the three policy-validation targets added, and `repo-config.yml` registered for both
> unit and integration runtimes. Along the way found and fixed an untested `DialogClose` export (a
> real coverage gap, same fix `web-ui` needed for the same component) and missing
> `animations: "disabled"` on visual-regression screenshots (pre-existing flakiness, matching
> `web-ui`'s fix); also corrected three stale `README.md` references left by the target rename.
> Leak-review clean (0 findings, PNG-chunk-level check on all screenshot baselines). CI green
> (103/103 unit tests, 100% coverage; 21/22 integration visual tests — the one failure is
> pre-existing, environment-specific headless-Chromium pixel nondeterminism confirmed not to gate
> CI, since `test:integration` is excluded from `pr-quality-gate.yml`'s `nx affected` target list
> per AC-TEST-05/FR-07). PR: [wahidyankf/ose-private#145](https://github.com/wahidyankf/ose-private/pull/145),
> merge commit `f5a457be1cdad02b951580db326391ee288c069d`.

## Phase 12: Migrate `O-PUB-AYO`

- **Input:** complete Ayo owner and two-harness rows.
- **Outcome:** one corpus has non-overlapping unit/integration/frontend-E2E/backend-E2E proof.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-03, AC-TEST-04, AC-TEST-05, AC-TEST-06, AC-TEST-08, AC-TEST-10, AC-TEST-11, AC-TEST-12, AC-SPECS-01, AC-C4-01, AC-C4-02, AC-COVERAGE-01, AC-COVERAGE-02, AC-COVERAGE-03, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### Ayo unit split prospective lifecycle

The following eight natural seams replace the retired oversized unit binding. Each has an exact frozen allocation, its own guarded PR lifecycle, and no cross-leaf source overlap.

### Leaf deliveries

#### Ayo unit split leaf deliveries

#### `D-O-PUB-AYO-UNIT-LEGACY-BACKEND-STEPS` leaf delivery

#### `D-O-PUB-AYO-UNIT-LEGACY-FRONTEND-STEPS` leaf delivery

#### `D-O-PUB-AYO-UNIT-APPLICATION-PLATFORM` leaf delivery

#### `D-O-PUB-AYO-UNIT-AI-BENCHMARK` leaf delivery

#### `D-O-PUB-AYO-UNIT-APP-SHELL-NAVIGATION` leaf delivery

#### `D-O-PUB-AYO-UNIT-CONTENT-I18N-SEARCH` leaf delivery

#### `D-O-PUB-AYO-UNIT-COST-OF-LIVING` leaf delivery

#### `D-O-PUB-AYO-UNIT-COURSE-PATHS` leaf delivery

### Ayo integration split prospective lifecycle

The following three project-bound seams replace the retired oversized integration binding.

#### Ayo integration split leaf deliveries

#### `D-O-PUB-AYO-INTEGRATION-APP` leaf delivery

#### `D-O-PUB-AYO-INTEGRATION-BACKEND-E2E` leaf delivery

#### `D-O-PUB-AYO-INTEGRATION-FRONTEND-E2E` leaf delivery

#### `D-O-PUB-AYO-CONTRACT` leaf delivery

#### `D-O-PUB-AYO-CORPUS-METADATA` leaf delivery

#### `D-O-PUB-AYO-CORPUS-BACKEND` leaf delivery

#### `D-O-PUB-AYO-CORPUS-BUILD-TOOLS` leaf delivery

#### `D-O-PUB-AYO-CORPUS-WEB-SHELL-CONTENT` leaf delivery

#### Ayo corpus navigation/tools split prospective lifecycle

The following three exact corpus seams replace the retired mixed navigation/tools binding.

#### Ayo corpus navigation/tools split leaf deliveries

#### `D-O-PUB-AYO-CORPUS-WEB-NAVIGATION` leaf delivery

#### `D-O-PUB-AYO-CORPUS-WEB-TOOLS` leaf delivery

#### `D-O-PUB-AYO-CORPUS-WEB-TOOLS-COST-OF-LIVING` leaf delivery

#### `D-O-PUB-AYO-CORPUS-COURSE-DISCOVERY` leaf delivery

#### `D-O-PUB-AYO-CORPUS-COURSE-FLOW` leaf delivery

### `RP-OWNER-O-PUB-AYO`

#### Ayo navigation/tools resolution and additional leaves

The earlier `D-O-PUB-AYO-CORPUS-WEB-NAVIGATION-TOOLS` checklist is retained as the exhaustive
delivery-lifecycle template for the renamed `D-O-PUB-AYO-CORPUS-WEB-NAVIGATION` binding. Its
preflight, branch, runtime, PR-body, exact-head, and merge evidence use the canonical navigation
binding name and the navigation-only finite allocation. It must not admit any `tools/**` path.

### Phase 12 Gate

> All checks below must pass before starting Phase 13.
>
> **Pause Safety:** Phase 12 is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --projects=ayokoding-www`.

### `D-O-PUB-AYO` delivery lifecycle

## Phase 13: Migrate `O-PUB-WAHID`

> **DESCOPED — do not execute.** On 2026-09-01 the user recorded that a separate workstream is
> removing `wahidyankf-www` (wahidyankf.com) together with `wahidyankf-www-fe-e2e`,
> `specs/apps/wahidyankf/**`, and everything tied to them. No action in this phase had begun, so
> nothing is unwound. The whole of Phase 13 — `D-O-PUB-WAHID`, `RP-OWNER-O-PUB-WAHID`, and the
> Phase 13 Gate — is dropped, and the plan's public PR total falls by this delivery's count.
>
> Two conditional rules survive the drop:
>
> 1. **Registry rows are removed with the project, never before it.** `testing.projects[]` and
>    `testing.compatibility.mappings[]` are a bijection with `rtk nx show projects --json`, so
>    deleting the `wahidyankf-www` and `wahidyankf-www-fe-e2e` rows while the projects still exist
>    fails `test-contract registry validate`. Whichever change removes the projects removes the two
>    project rows, the two mappings, and the two frozen `coverage.projects` entries in that same
>    change. If a rebase lands the removal without touching the registry, the next delivery in this
>    plan repairs it before any other edit and reruns
>    `test-contract registry validate` plus `validate-mapping --all --require-count <nx-count>`.
> 2. **Every frozen count that named these two projects moves to the new Nx total.** The Phase 0
>    closure, the `--require-count` arguments, and the Phase 20 contraction counts follow
>    `rtk nx show projects --json` at the time they run, not the number frozen while the projects
>    still existed.
>
> If the removal has not landed by the time this plan reaches Phase 13, this phase stays blocked
> and the user decides whether to reinstate it — it is never resumed by default.

- **Input:** complete site and frontend-harness rows.
- **Outcome:** the site has non-overlapping runtime/static proof and direct targets.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-03, AC-TEST-04, AC-TEST-05, AC-TEST-06, AC-TEST-08, AC-TEST-10, AC-TEST-11, AC-TEST-12, AC-SPECS-01, AC-C4-01, AC-C4-02, AC-COVERAGE-01, AC-COVERAGE-02, AC-COVERAGE-03, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### `RP-OWNER-O-PUB-WAHID`

### Phase 13 Gate

> All checks below must pass before starting Phase 14.
>
> **Pause Safety:** Phase 13 is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --projects=wahidyankf-www`.

### `D-O-PUB-WAHID` delivery lifecycle

## Phase 14: Migrate `O-PUB-OL-WEB`

- **Input:** complete app-web/harness rows and post-DDD specs map.
- **Outcome:** OrganicLever web satisfies the contract without DDD reintroduction.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-03, AC-TEST-04, AC-TEST-05, AC-TEST-06, AC-TEST-08, AC-TEST-10, AC-TEST-11, AC-TEST-12, AC-SPECS-01, AC-C4-01, AC-C4-02, AC-COVERAGE-01, AC-COVERAGE-02, AC-COVERAGE-03, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### `RP-OWNER-O-PUB-OL-WEB`

### Phase 14 Gate

> All checks below must pass before starting Phase 15.
>
> **Pause Safety:** Phase 14 is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --projects=organiclever-app-web`.

### `D-O-PUB-OL-WEB` delivery lifecycle

## Phase 15: Migrate `O-PUB-OL-BE`

- **Input:** complete backend/contracts/API-harness rows and schema boundaries.
- **Outcome:** backend, contracts, and API E2E satisfy one exact corpus contract.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-03, AC-TEST-04, AC-TEST-05, AC-TEST-06, AC-TEST-08, AC-TEST-10, AC-TEST-11, AC-TEST-12, AC-SPECS-01, AC-C4-01, AC-C4-02, AC-COVERAGE-01, AC-COVERAGE-02, AC-COVERAGE-03, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### `RP-OWNER-O-PUB-OL-BE`

### Phase 15 Gate

> All checks below must pass before starting Phase 16.
>
> **Pause Safety:** Phase 15 is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --projects=organiclever-be`.

### `D-O-PUB-OL-BE` delivery lifecycle

## Phase 16: Migrate `O-PUB-OL-WWW`

- **Input:** complete marketing owner and both harness rows.
- **Outcome:** OrganicLever marketing has complete non-overlapping surface proof.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-03, AC-TEST-04, AC-TEST-05, AC-TEST-06, AC-TEST-08, AC-TEST-10, AC-TEST-11, AC-TEST-12, AC-SPECS-01, AC-C4-01, AC-C4-02, AC-COVERAGE-01, AC-COVERAGE-02, AC-COVERAGE-03, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### `RP-OWNER-O-PUB-OL-WWW`

### Phase 16 Gate

> All checks below must pass before starting Phase 17.
>
> **Pause Safety:** Phase 16 is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --projects=organiclever-www`.

### `D-O-PUB-OL-WWW` delivery lifecycle

## Phase 17: Migrate `O-PUB-OSE-WEB`

- **Input:** complete app-web/harness rows and post-DDD specs map.
- **Outcome:** OSE web satisfies the contract without DDD reintroduction.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-03, AC-TEST-04, AC-TEST-05, AC-TEST-06, AC-TEST-08, AC-TEST-10, AC-TEST-11, AC-TEST-12, AC-SPECS-01, AC-C4-01, AC-C4-02, AC-COVERAGE-01, AC-COVERAGE-02, AC-COVERAGE-03, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### `RP-OWNER-O-PUB-OSE-WEB`

### Phase 17 Gate

> All checks below must pass before starting Phase 18.
>
> **Pause Safety:** Phase 17 is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --projects=ose-app-web`.

### `D-O-PUB-OSE-WEB` delivery lifecycle

## Phase 18: Migrate `O-PUB-OSE-BE`

- **Input:** complete backend/contracts/API-harness rows and schema boundaries.
- **Outcome:** backend, contracts, and API E2E satisfy one exact corpus contract.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-03, AC-TEST-04, AC-TEST-05, AC-TEST-06, AC-TEST-08, AC-TEST-10, AC-TEST-11, AC-TEST-12, AC-SPECS-01, AC-C4-01, AC-C4-02, AC-COVERAGE-01, AC-COVERAGE-02, AC-COVERAGE-03, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### `RP-OWNER-O-PUB-OSE-BE`

### Phase 18 Gate

> All checks below must pass before starting Phase 19.
>
> **Pause Safety:** Phase 18 is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --projects=ose-be`.

### `D-O-PUB-OSE-BE` delivery lifecycle

## Phase 19: Migrate `O-PUB-OSE-WWW`

- **Input:** complete marketing owner and both harness rows.
- **Outcome:** OSE marketing has complete non-overlapping surface proof.
- **Acceptance criteria:** [AC-TEST-01, AC-TEST-02, AC-TEST-03, AC-TEST-04, AC-TEST-05, AC-TEST-06, AC-TEST-08, AC-TEST-10, AC-TEST-11, AC-TEST-12, AC-SPECS-01, AC-C4-01, AC-C4-02, AC-COVERAGE-01, AC-COVERAGE-02, AC-COVERAGE-03, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### `RP-OWNER-O-PUB-OSE-WWW`

### Phase 19 Gate

> All checks below must pass before starting Phase 20A.
>
> **Pause Safety:** Phase 19 is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --projects=ose-www`.

### `D-O-PUB-OSE-WWW` delivery lifecycle

## Phase 20A: Close the Private Rollout

- **Input:** every private owner PR and rules manifest.
- **Outcome:** no private transition, old root, proxy, lower threshold, or BDD gap remains.
- **Acceptance criteria:** [AC-TEST-01 through AC-TEST-12, AC-REPO-01, AC-RULES-01, AC-DDD-01, AC-SPECS-01, AC-C4-01, AC-C4-02, and AC-COVERAGE-01 through AC-COVERAGE-03](./prd.md#acceptance-criteria).

- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### `RP-P20-PRI`

### Phase 20A Gate

> All checks below must pass before starting Phase 20B.
>
> **Pause Safety:** Phase 20A is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PRI:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --all`.

### `D-P20-PRI` delivery lifecycle

## Phase 20B: Close the Public Rollout

- **Input:** every public owner PR, private terminal proof, registries, and manifests.
- **Outcome:** public closure is green on the final branch used for Knowledge Capture and archival.
- **Acceptance criteria:** [AC-TEST-01 through AC-TEST-12, AC-REPO-01, AC-RULES-01, AC-DDD-01, AC-SPECS-01, AC-C4-01, AC-C4-02, and AC-COVERAGE-01 through AC-COVERAGE-03](./prd.md#acceptance-criteria).
- **Exact final-PR allocation:** 19 hand-authored paths: the 13 plan-document destinations listed by
  `rtk proxy find plans/in-progress/adopt-beavernest-test-automation -type f -print`, including
  `delivery.md`, `implementation-notes.md`, and reserved `learnings.md`; the two index edits
  `plans/in-progress/README.md` and `plans/done/README.md`; and exactly four closure paths: `repo-config.yml`,
  `apps/rhino-cli/src/RhinoCli.Application/src/TestContract.fs`,
  `apps/rhino-cli/tests/unit/TestContractClosureUnitTests.fs`, and
  `apps/rhino-cli/tests/unit/Fixtures/TestContract/Closure/closure.json`. The finite registry,
  lifecycle, corpus, layout, manifest, coverage, BDD, and target-composition negative cases are
  sections in that one fixture and assertions in that one test file. Prior unit evidence remains as
  binding rows in `implementation-notes.md`; that ordinary plan document moves exactly once and is
  never copied or re-added. `RP-P20-PUB`
  therefore verifies the already-delivered canonical rule surfaces unchanged; if it discovers a
  required governance edit, stop and amend an earlier natural rule-delivery unit before this branch.
  Do not add an optional runtime split or a twentieth hand-authored path.

- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### `RP-P20-PUB`

### Phase 20B Gate

> All checks below must pass before starting Phase 21.
>
> **Pause Safety:** Phase 20B is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --all`.

## Phase 21: Knowledge Capture on the Final Public Branch

- **Input:** terminal rollout evidence and the complete `learnings.md` log.
- **Outcome:** every learning is routed, reported, or discarded without unauthorized code/plan work.
- **Acceptance criteria:** [AC-TEST-08 and AC-TEST-09](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### Phase 21 Gate

> All checks below must pass before starting Phase 22.
>
> **Pause Safety:** Phase 21 is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk rg -n "TODO|TBD|open|pending" plans/in-progress/adopt-beavernest-test-automation/learnings.md local-tmp/adopt-beavernest-test-automation/evidence/runtime/public/phase-0/R-PUB/implementation-notes.md`.

## Phase 22: End-to-End Audit, Runtime-Dated Archive, and Final Public PR

- **Input:** both closure matrices, all merged delivery evidence, and terminal learnings.
- **Outcome:** no scope gap remains and the plan archives inside the final public delivery PR.
- **Acceptance criteria:** [AC-TEST-08, AC-TEST-09, AC-REPO-01, and AC-RULES-01](./prd.md#acceptance-criteria).
- **Proof:** CI green on the merged head, plus the PR's leak-review record. See the per-PR process above.

### Phase 22 Gate

> All checks below must pass before starting the final public delivery lifecycle; there is no later
> implementation phase.
>
> **Pause Safety:** Phase 22 is coherent at a natural pause only after every gate above passes. Safe to stop. To resume in `R-PUB:worktrees/adopt-beavernest-test-automation`: `rtk nx run-many -t test:quick,test:coverage,test:behavior:coverage,test:layout:validation,package-manifest:policy:validation,specs:structure-validation --all`.

### Runtime Archive Root for `D-P20-PUB`

The archival move changes the plan root before the final PR lifecycle. Before every
`D-P20-PUB-DB-*` checkbox, resolve the one actual moved root in the current shell with:

```bash
archive_root="$(rtk bash -lc 'set -- plans/done/*__adopt-beavernest-test-automation; test "$#" -eq 1; test -f "$1/delivery.md"; printf "%s" "$1"')"
```

Expect one non-empty `plans/done/YYYY-MM-DD__adopt-beavernest-test-automation` value. Stop if zero
or multiple paths match; never substitute today's date after archival. Every `${archive_root}` path
below means that validated value, so the lifecycle remains resumable across a local-date change.

### `D-P20-PUB` delivery lifecycle

### Terminal Worktree Cleanup

Cleanup runs from each validated primary checkout, never from the execution worktree being
removed. The context action emits the primary location only into ignored runtime evidence; select
that resolved runtime location as the next tool working directory because a subshell cannot change
the caller's working directory.
On a later fresh-shell resume, select the already verified `R-PUB:` or `R-PRI:` primary location
again; none of the removal/prune commands needs an inherited root variable or a surviving map.

The existing post-archive evidence family continues in each primary checkout's ignored
`local-tmp/adopt-beavernest-test-automation/evidence/runtime/<public|private>/post-archive/terminal-cleanup/`
directory, outside the execution tree. `before.json` is the immediate pre-removal inventory;
`after-removal.json` and `after-prune.json` prove exact preservation of every unrelated porcelain
record. Keep these raw local paths ignored. A `rules-update` tree is preserved if actually present
in `before.json`; an already-absent authoring tree is neither required nor recreated. If an unrelated
record changes, stop and investigate without deleting, restoring, or silently rebaselining it.
