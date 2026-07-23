-- store.lua -- a tiny closure-backed config-value store with metatable-defaulted lookups.
-- The whole contract of a Lua module: this file RETURNS a table (Example 57's pattern),
-- here holding exactly one field, `new`, the store's constructor.

local defaults = { -- record-shaped table: baked-in defaults for known config keys
	theme = "default",
	timeout = 30,
}

local M = {} -- the module table this file returns to every require("store") caller

function M.new()
	local store = setmetatable({}, { __index = defaults })
	-- store starts EMPTY; every field access that misses store falls through to defaults (Example 54's pattern)

	local function get(key)
		return store[key] -- ordinary table read -- __index fires automatically on a miss
	end

	local function set(key, value)
		store[key] = value -- ordinary table write -- always lands in store itself, never in defaults
	end

	local function get_required(key)
		local value = get(key)
		if value == nil then
			error("missing required key: " .. key, 0)
			-- level 0 (Example 62's pattern) suppresses the "file:line:" prefix -- a clean message for pcall's err
		end
		return value
	end

	local function keys()
		local list = {}
		for k in pairs(store) do -- pairs walks store's OWN keys only -- __index never affects iteration
			list[#list + 1] = k
		end
		table.sort(list) -- deterministic order regardless of hash-table iteration order
		return list
	end

	return { get = get, set = set, get_required = get_required, keys = keys }
	-- get/set/get_required/keys are all closures sharing the ONE `store` upvalue above --
	-- each call to M.new() creates a fresh, independent store (Example 48's pattern)
end

return M
