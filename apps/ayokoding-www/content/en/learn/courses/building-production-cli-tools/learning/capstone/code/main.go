package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"strings"
)

const version = "1.0.0"

type report struct {
	Release string `json:"release"`
	Region  string `json:"region"`
	Status  string `json:"status"`
}

func regionFor(flagValue string) string {
	if flagValue != "" {
		return flagValue
	}
	if value := os.Getenv("SHIP_REGION"); value != "" {
		return value
	}
	if data, err := os.ReadFile("ship.conf"); err == nil && strings.TrimSpace(string(data)) != "" {
		return strings.TrimSpace(string(data))
	}
	return "local"
}

func usage() { fmt.Fprintln(os.Stderr, "usage: ship [--version] <status|completion> [options]") }

func isTerminal(file *os.File) bool {
	info, err := file.Stat()
	return err == nil && info.Mode()&os.ModeCharDevice != 0
}

func progress(message string, interactive bool) {
	if interactive {
		fmt.Fprintf(os.Stderr, "\r\033[36m%s\033[0m\n", message)
	}
}

func main() {
	if len(os.Args) == 2 && (os.Args[1] == "--help" || os.Args[1] == "-h") {
		usage()
		return
	}
	if len(os.Args) == 2 && os.Args[1] == "--version" {
		fmt.Println(version)
		return
	}
	if len(os.Args) < 2 {
		usage()
		os.Exit(2)
	}
	switch os.Args[1] {
	case "completion":
		if len(os.Args) == 3 && os.Args[2] == "bash" {
			fmt.Println("complete -W 'status completion' ship")
			return
		}
		usage()
		os.Exit(2)
	case "status":
		fs := flag.NewFlagSet("status", flag.ContinueOnError)
		fs.SetOutput(os.Stderr)
		jsonMode := fs.Bool("json", false, "emit JSON")
		region := fs.String("region", "", "release region")
		if len(os.Args) == 3 && (os.Args[2] == "--help" || os.Args[2] == "-h") {
			fmt.Println("usage: ship status [--json] [--region REGION] RELEASE")
			return
		}
		if fs.Parse(os.Args[2:]) != nil || fs.NArg() != 1 {
			fmt.Fprintln(os.Stderr, "usage: ship status [--json] [--region REGION] RELEASE")
			os.Exit(2)
		}
		r := report{Release: fs.Arg(0), Region: regionFor(*region), Status: "ready"}
		if *jsonMode {
			_ = json.NewEncoder(os.Stdout).Encode(r)
			return
		}
		progress("progress: checked release metadata", isTerminal(os.Stderr))
		fmt.Printf("release %s is %s in %s\n", r.Release, r.Status, r.Region)
	default:
		fmt.Fprintf(os.Stderr, "error: unknown command %q\n", os.Args[1])
		usage()
		os.Exit(2)
	}
}
