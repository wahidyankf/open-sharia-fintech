package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
)

type report struct {
	Release string `json:"release"`
	Region  string `json:"region"`
	Status  string `json:"status"`
}

func main() {
	jsonOutput := flag.Bool("json", false, "emit JSON")
	region := flag.String("region", "", "release region")
	flag.Parse()
	chosenRegion := *region
	if chosenRegion == "" {
		chosenRegion = os.Getenv("SHIP_REGION")
	}
	if chosenRegion == "" {
		chosenRegion = "local"
	}
	if flag.NArg() != 1 {
		fmt.Fprintln(os.Stderr, "usage: ship [--json] [--region REGION] RELEASE")
		os.Exit(2)
	}
	r := report{Release: flag.Arg(0), Region: chosenRegion, Status: "ready"}
	if *jsonOutput {
		_ = json.NewEncoder(os.Stdout).Encode(r)
		return
	}
	fmt.Printf("release %s is %s in %s\n", r.Release, r.Status, r.Region)
}
