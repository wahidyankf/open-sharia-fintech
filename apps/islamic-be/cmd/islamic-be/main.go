// Command islamic-be serves the Islamic tools backend.
//
// This file is deliberately thin and is excluded from the coverage denominator:
// everything it does is bind a socket and read the process environment, which
// are precisely the boundaries Unit proof may not touch. All decisions it makes
// live in internal/config and internal/router, which are covered at 100%.
package main

import (
	"flag"
	"fmt"
	"net"
	"os"
	"strconv"

	"github.com/wahidyankf/ose-public/apps/islamic-be/internal/config"
	"github.com/wahidyankf/ose-public/apps/islamic-be/internal/router"
)

func main() {
	portFlag := flag.String("port", "", "listener port; overrides "+config.PortVariable)
	flag.Parse()

	port, err := config.ResolvePort(*portFlag, os.LookupEnv)
	if err != nil {
		// Refuse to start rather than fall back to the default, so a typo'd port
		// surfaces immediately instead of as traffic arriving on the wrong one.
		fmt.Fprintf(os.Stderr, "islamic-be: %v\n", err)
		os.Exit(1)
	}

	address := net.JoinHostPort("", strconv.Itoa(port))
	if err := router.New().Run(address); err != nil {
		fmt.Fprintf(os.Stderr, "islamic-be: %v\n", err)
		os.Exit(1)
	}
}
