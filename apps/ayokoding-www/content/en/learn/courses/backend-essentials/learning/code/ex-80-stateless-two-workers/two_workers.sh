#!/usr/bin/env bash
# Example 80: two INDEPENDENT uvicorn processes sharing only the SQLite file (co-05, co-24).
# Worker A serves port 8003, Worker B serves port 8004 -- separate OS processes, no shared memory.
set -euo pipefail # => co-22: abort immediately on any failing command, unset var, or pipe error

cd "$(dirname "$0")" # => ensures the relative paths below resolve from this script's own directory
rm -f tasks.db       # => co-05: start from a clean, deterministic file both workers will share

VENV_PY="../../../.venv/bin/python" # => the shared venv's interpreter, three levels up from this dir

echo "== starting worker A on :8003 =="                                                   # => co-05: the FIRST of two separate OS processes
WORKER_PORT=8003 "$VENV_PY" -m uvicorn app:app --port 8003 >/tmp/ex80_worker_a.log 2>&1 & # => backgrounds worker A, its own env var, its own log file
WORKER_A_PID=$!                                                                           # => co-05: captures worker A's OS process id for later confirmation and cleanup
echo "== starting worker B on :8004 =="                                                   # => co-05: the SECOND, entirely separate OS process
WORKER_PORT=8004 "$VENV_PY" -m uvicorn app:app --port 8004 >/tmp/ex80_worker_b.log 2>&1 & # => backgrounds worker B, a DIFFERENT env var, its own log file
WORKER_B_PID=$!                                                                           # => co-05: captures worker B's OS process id for later confirmation and cleanup

sleep 2 # => gives both uvicorn processes time to finish starting before the curl calls below

echo "== confirm TWO distinct OS processes are running ==" # => co-05: proof this is genuinely two processes
ps -p "$WORKER_A_PID" -o pid,command | tail -1             # => co-05: shows worker A's real OS pid and command line
ps -p "$WORKER_B_PID" -o pid,command | tail -1             # => co-05: shows worker B's real OS pid -- DIFFERENT from A's

echo "== worker A identifies itself ==" # => co-05: /whoami reports which PROCESS answered this request
curl -s http://localhost:8003/whoami    # => co-05: hits worker A directly by its own port
echo                                    # => a blank line separator between this step's output and the next
echo "== worker B identifies itself ==" # => co-05: the SAME /whoami route, now against the OTHER process
curl -s http://localhost:8004/whoami    # => co-05: hits worker B directly by its own port
echo                                    # => a blank line separator between this step's output and the next

echo "== create a task on WORKER A (:8003) ==" # => co-05, co-24: the WRITE happens through worker A only
# => captures the FULL response body so task_id can be extracted below
create_response=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"title":"created on worker A"}' http://localhost:8003/tasks)                                  # => co-24: routed to worker A's port
echo "$create_response"                                                                              # => prints the raw JSON body so the created task's id is visible
task_id=$(echo "$create_response" | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])') # => extracts "id"

echo "== read the SAME task from WORKER B (:8004) -- proves the file, not memory, is the source of truth ==" # => co-05: the READ happens through a DIFFERENT process
curl -s http://localhost:8004/tasks/"$task_id"                                                               # => co-05: worker B never saw the write -- only the shared file did
echo                                                                                                         # => a blank line separator before the cleanup step below

kill "$WORKER_A_PID" "$WORKER_B_PID" 2>/dev/null || true # => co-05: stops both background processes; || true tolerates an already-exited pid
echo "== workers stopped =="                             # => confirms cleanup ran to completion
