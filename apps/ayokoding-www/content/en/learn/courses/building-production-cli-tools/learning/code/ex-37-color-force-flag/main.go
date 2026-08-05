package main

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	color := flag.String("color", "auto", "auto, always, or never")
	flag.Parse()
	tty, _ := os.Stdout.Stat()
	if *color != "auto" && *color != "always" && *color != "never" {
		fmt.Fprintln(os.Stderr, "--color must be auto, always, or never")
		os.Exit(2)
	}
	if *color == "always" || (*color == "auto" && tty.Mode()&os.ModeCharDevice != 0) {
		fmt.Println("\033[32mready\033[0m")
	} else {
		fmt.Println("ready")
	}
}
