package main

import "os"

func main() { os.WriteFile("/missing/path", nil, 0o600) }
