#!/usr/bin/env bash
# Example 78: a documented curl sequence exercising CRUD + auth end-to-end (co-22, co-18).
# Run against a live server: uvicorn app:app --port 8003 (from this directory).
set -euo pipefail # => co-22: abort immediately on any failing command, unset var, or pipe error

BASE_URL="http://localhost:8003" # => the target server this script drives end-to-end
TOKEN="s3cr3t-token-abc123"      # => matches app.py's VALID_TOKEN -- the SAME literal both sides expect

echo "== Step 1: create WITHOUT a token -- expect 401 ==" # => co-18: no Authorization header at all
# => captures ONLY the HTTP status code, discarding the response body via -o /dev/null
code=$(curl -s -o /dev/null -w '%{http_code}' -X POST -H "Content-Type: application/json" \
  -d '{"title":"write the report"}' "$BASE_URL/tasks") # => co-02: POST with no Authorization header
echo "status: $code"                                   # => prints the captured status code for a human reading the script's output
test "$code" = "401"                                   # => co-03: aborts the script (set -e) if this specific assertion fails

echo "== Step 2: create WITH a valid token -- expect 201 ==" # => co-18: the SAME create, now WITH a token
# => this time the FULL response body is captured, not just the status
create_response=$(curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" -d '{"title":"write the report"}' "$BASE_URL/tasks")             # => co-18
echo "$create_response"                                                                              # => prints the raw JSON body so the created task's id is visible
task_id=$(echo "$create_response" | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])') # => extracts "id"
echo "created task id: $task_id"                                                                     # => the id every remaining step below operates on

echo "== Step 3: read the created task (no token needed) -- expect 200 ==" # => co-02: reads stay OPEN
curl -s -i "$BASE_URL/tasks/$task_id"                                      # => -i prints response headers too, not just the body
echo                                                                       # => a blank line separator between this step's output and the next

echo "== Step 4: update WITH a valid token -- expect 200, status becomes done ==" # => co-02: PUT replaces
# => co-18: PUT is guarded the same way POST was in Step 2
curl -s -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"write the report","status":"done"}' "$BASE_URL/tasks/$task_id" # => full-body replace
echo                                                                           # => separates this step's raw JSON response from the next step's header

echo "== Step 5: delete WITH a valid token -- expect 204 ==" # => co-18: DELETE is guarded too
# => co-02: DELETE carries no body -- only the status code is captured
code=$(curl -s -o /dev/null -w '%{http_code}' -X DELETE -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/tasks/$task_id") # => co-02: same task_id created back in Step 2
echo "status: $code"          # => prints the captured DELETE status code
test "$code" = "204"          # => co-03: 204 means success with no response body

echo "== Step 6: read after delete -- expect 404 (genuinely gone) =="     # => proves the row is truly gone
code=$(curl -s -o /dev/null -w '%{http_code}' "$BASE_URL/tasks/$task_id") # => co-02: same unguarded GET
echo "status: $code"                                                      # => prints the captured final status code
test "$code" = "404"                                                      # => co-03: confirms the row is genuinely gone, not just soft-deleted

echo "== ALL STEPS PASSED ==" # => only reached if every test assertion above succeeded (set -e)
