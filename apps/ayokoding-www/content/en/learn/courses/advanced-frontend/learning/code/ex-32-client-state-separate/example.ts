// Example 32: Client UI State Stays Separate from the Server Cache. (co-15)
//
// Client-only UI state (a dark-mode toggle, an expanded-panel flag) and server cache state live in
// DIFFERENT stores. They update independently: toggling the theme never refetches, and a refetch
// never resets the theme. Conflating them is a common source of redundant work and lost UI state.

// Two separate stores: client UI state vs. the server cache.
const clientUi = { theme: "light" as "light" | "dark" }; // => UI-only; never touches the network
// => putting UI state in the server cache would make every theme toggle risk a refetch
const serverCache = { user: "cached-user-42" }; // => server data; refetched independently

// toggleTheme changes ONLY the client UI store -- no refetch, no cache interaction.
function toggleTheme(): void {
  // => co-15: client UI state updates by itself, without involving server state
  clientUi.theme = clientUi.theme === "light" ? "dark" : "light"; // => a pure UI concern
}

// refetchUser changes ONLY the server cache -- the theme is untouched.
function refetchUser(): void {
  // => co-15: a server-state change does not reset client UI state
  serverCache.user = "cached-user-42-refreshed"; // => new server data
}

toggleTheme(); // => UI flips; the cache is unchanged
refetchUser(); // => cache refreshes; the theme is unchanged

console.log("theme after both updates:", clientUi.theme); // => Output: theme after both updates: dark
console.log("user after both updates:", serverCache.user); // => Output: user after both updates: cached-user-42-refreshed
