-- NOTE: .setup() is deliberately never called -- a caller who only wants to `require`
-- a library function should never get a side-effecting global command for free
require("myplugin")
