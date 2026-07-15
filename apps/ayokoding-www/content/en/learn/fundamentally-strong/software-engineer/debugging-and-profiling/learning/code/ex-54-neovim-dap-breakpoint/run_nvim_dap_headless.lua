-- Example 54: drive a REAL nvim-dap + nvim-dap-python session headlessly, attach
-- debugpy to a launched target.py, stop at a breakpoint, and read a scope
-- variable -- exactly what the DAP UI shows a human, just scripted instead of
-- clicked, so the whole thing is scriptable and its output is real captured text.
vim.opt.rtp:prepend(os.getenv("DAP_CORE")) -- => co-06: vendors nvim-dap into THIS headless run only
vim.opt.rtp:prepend(os.getenv("DAP_PYTHON_PLUGIN")) -- => co-06: same trick for nvim-dap-python

local dap = require("dap") -- => co-06: the core plugin -- breakpoints, sessions, requests
local dap_python = require("dap-python") -- => co-06: the Python-specific adapter config on top of dap

dap_python.setup(os.getenv("DAP_PYTHON_EXE")) -- => co-06: points at venv54's python, where debugpy is installed

local target = os.getenv("DAP_TARGET") -- => co-01/co-06: the SAME target.py CLI pdb also debugs
local result_path = os.getenv("DAP_RESULT") -- => co-06: where this script writes its captured JSON result
local breakpoint_line = tonumber(os.getenv("DAP_LINE")) -- => co-01/co-06: the SAME line pdb's own `break` used

vim.cmd("edit " .. target) -- => co-06: opens target.py as a REAL buffer -- toggle_breakpoint needs one
vim.api.nvim_win_set_cursor(0, { breakpoint_line, 0 }) -- => co-06: moves the cursor to the target line first
dap.toggle_breakpoint() -- => co-06: sets a REAL breakpoint at the cursor's line, the DAP UI equivalent of pdb's `break`

local stopped_body = nil -- => co-06: filled in by the listener below once the session actually stops
dap.listeners.after.event_stopped["capture"] = function(_session, body) -- => co-06: fires on the DAP "stopped" event
	stopped_body = body -- => co-06: captures the event payload so the polling loop below can detect it
end -- => co-06: end of the event_stopped listener

local config = { -- => co-06: the SAME shape a human's launch.json would declare, built inline instead
	type = "python", -- => co-06: selects the python adapter dap_python.setup() registered above
	request = "launch", -- => co-06: starts a FRESH debugpy process, rather than attaching to one already running
	name = "Launch file (Example 54)", -- => co-06: a human-readable label -- cosmetic only
	program = target, -- => co-06: the SAME target.py path used for the breakpoint above
	console = "internalConsole", -- => co-06: keeps target.py's stdout inside this headless nvim, not a new terminal
} -- => co-06: end of the launch config table
dap.run(config) -- => co-06: launches debugpy against target.py and attaches -- the REAL session starts here

vim.wait(10000, function() -- => co-06: polls up to 10s for the stopped event -- debugpy startup is not instant
	return stopped_body ~= nil -- => co-06: the condition vim.wait polls -- true once the listener above fired
end, 50) -- => co-06: check every 50ms while waiting

if stopped_body == nil then -- => co-06: an honest failure path -- never silently reports a fake success
	local f = io.open(result_path, "w") -- => co-06: still writes a result file, so the caller never hangs on a missing file
	f:write('{"error": "never stopped"}') -- => co-06: a real, explicit failure marker
	f:close() -- => co-06: flushes the error result to disk
	vim.cmd("qa!") -- => co-06: exits headless nvim immediately -- nothing more to do on this path
	return -- => co-06: stops this script here -- the success path below never runs
end -- => co-06: end of the failure-path guard

vim.wait(5000, function() -- => co-06: waits for the session's current_frame to populate after stopping
	local s = dap.session() -- => co-06: the live DAP session object, once dap.run() has attached
	return s ~= nil and s.current_frame ~= nil -- => co-06: true once a frame is genuinely available to inspect
end, 20) -- => co-06: check every 20ms -- this settles fast once stopped_body is already set

local session = dap.session() -- => co-06: the SAME live session, read again now that current_frame is ready
local frame = session.current_frame -- => co-01/co-06: the frame the breakpoint actually stopped in

local scopes_result = nil -- => co-06: filled in by the async "scopes" DAP request below
session:request("scopes", { frameId = frame.id }, function(_err, resp) -- => co-06: the SAME DAP request the UI sends
	scopes_result = resp -- => co-06: captures the response -- Locals/Globals scope references live here
end) -- => co-06: end of the scopes request callback
vim.wait(5000, function() -- => co-06: polls until the async scopes response actually lands
	return scopes_result ~= nil -- => co-06: true once the callback above ran
end, 20) -- => co-06: check every 20ms

local locals_scope = nil -- => co-06: the ONE scope this example reads -- the DAP UI's own "Locals" panel
for _, scope in ipairs(scopes_result.scopes) do -- => co-06: scopes_result.scopes is typically [Locals, Globals]
	if scope.name == "Locals" then -- => co-06: filters out Globals -- only Locals is compared against pdb
		locals_scope = scope -- => co-06: keeps the matching scope's variablesReference for the next request
	end -- => co-06: end of the name check
end -- => co-06: end of the scopes loop

local variables_result = nil -- => co-06: filled in by the async "variables" DAP request below
session:request("variables", { variablesReference = locals_scope.variablesReference }, function(_err, resp) -- => co-06
	variables_result = resp -- => co-06: captures the response -- the actual name/value pairs the DAP UI would show
end) -- => co-06: end of the variables request callback
vim.wait(5000, function() -- => co-06: polls until the async variables response actually lands
	return variables_result ~= nil -- => co-06: true once the callback above ran
end, 20) -- => co-06: check every 20ms

local lines = {} -- => co-06: builds the result JSON by hand -- no JSON encoder dependency needed for this shape
table.insert(lines, string.format('"stopped_line": %d,', frame.line)) -- => co-01/co-06: compared against PDB_STOPPED_LINE
table.insert(lines, string.format('"stopped_source": %q,', frame.source.path or frame.source.name)) -- => co-06: path for context
table.insert(lines, '"locals": {') -- => co-06: opens the nested locals object
for i, var in ipairs(variables_result.variables) do -- => co-06: one entry per variable the DAP scope reported
	local comma = (i < #variables_result.variables) and "," or "" -- => co-06: valid JSON needs no trailing comma
	table.insert(lines, string.format("  %q: %q%s", var.name, var.value, comma)) -- => co-01/co-06: name/value, as strings
end -- => co-06: end of the variables loop
table.insert(lines, "}") -- => co-06: closes the nested locals object

local f = io.open(result_path, "w") -- => co-06: opens the SAME result_path compare_pdb_and_dap.py reads
f:write("{\n" .. table.concat(lines, "\n") .. "\n}\n") -- => co-06: writes the assembled JSON, one field per line
f:close() -- => co-06: flushes the real captured result to disk

dap.terminate() -- => co-06: cleanly ends the debugpy session rather than leaving it dangling
vim.wait(2000, function() -- => co-06: waits for the session to actually disappear before exiting nvim
	return dap.session() == nil -- => co-06: true once dap.terminate() has fully torn the session down
end, 50) -- => co-06: check every 50ms

vim.cmd("qa!") -- => co-06: exits headless nvim -- this script's whole job is now done
