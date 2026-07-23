# Capstone keystroke transcript

Every keystroke below was replayed against a fresh copy of `before/` and produced `after/` exactly
(verified against real Neovim, not simulated). Follow it in order, in one continuous Neovim session,
starting from a working copy of `before/`. Nothing here uses a plugin, the mouse, or an arrow key.

## Step 1 -- seed check (shell)

```text
$ ls
calc.py  main.py  tasks.txt
```

## Step 2 -- rename `oldName` to `newName` everywhere

```text
$ nvim calc.py                          " => opens calc.py; main.py and tasks.txt stay on disk
:vimgrep /oldName/ **/*<CR>             " => recursively globs the directory and searches every file for 'oldName'
                                        " => populates the quickfix list with 3 entries: calc.py:1, main.py:1, main.py:5
:copen<CR>                              " => opens the quickfix window listing all 3 matches
:cnext<CR>                              " => jumps to a listed match
:cnext<CR>                              " => jumps to the next listed match
:cdo s/oldName/newName/g | update<CR>   " => runs the substitution on every quickfix entry, then writes each file if changed
:cclose<CR>                             " => closes the quickfix window
```

## Step 3 -- reformat and enrich the task list

```text
:e tasks.txt<CR>                        " => opens tasks.txt in the same session; calc.py/main.py stay open as buffers
gg                                      " => moves to line 1, 'buy milk'
qa                                      " => starts recording into register a
I- [ ] <Esc>j                           " => inserts the checkbox prefix, returns to Normal mode, moves down one line
q                                       " => stops recording; register a now holds 'I- [ ] <Esc>j'
10@a                                    " => replays the macro 10 more times, checkbox-prefixing lines 2-11
/bob<CR>                                " => searches forward for 'bob' on line 3
ciwcarol<Esc>                           " => `c` + the `iw` text object replaces only that word
gg                                      " => returns to line 1
"ayy                                    " => yanks line 1 into named register a
G                                       " => jumps to the last line
"ap                                     " => pastes register a below it, duplicating the first task as line 12
:%s/^\(- \[ \] \)\(.*\)$/\1TODO: \2/<CR>  " => capture-group substitution: group 1 keeps the checkbox, group 2 is the task text
:w<CR>                                  " => saves tasks.txt
```

## Step 4 -- run the project check from `:terminal`

```text
:terminal python3 -m py_compile *.py && echo OK<CR>   " => syntax-checks both renamed Python files, then echoes a marker
<C-\><C-n>                                            " => escapes Terminal mode back to Normal mode
gg                                                    " => jumps to the first line of the terminal output
G                                                      " => jumps to the last line, where 'OK' is printed
```

## Step 5 -- this file

This transcript, concatenated in the order shown above, is the artifact saved at
`learning/capstone/code/transcript.md`. `calc.py` and `main.py` were already saved by Step 2's
`| update`; `tasks.txt` was saved explicitly by Step 3's `:w`. Exit however you like -- `:q` per
window or `ZZ`, both already covered earlier in this primer.

## Verify against `after/`

```text
$ diff -r --exclude=__pycache__ . ../after
(no output -- diff exits 0 when the two trees match exactly)
```

An empty result confirms the working copy matches `after/` exactly.
