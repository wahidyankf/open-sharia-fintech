package main

import "fmt"

func render(name string) string { return "release=" + name + "\nstatus=ready\n" }

func main() {
	const golden = "release=v1\nstatus=ready\n"
	got := render("v1")
	if got != golden {
		panic("golden output changed")
	}
	fmt.Print(got)
}
