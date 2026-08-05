package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, os.Interrupt, syscall.SIGTERM)
	fmt.Println("working; press Ctrl-C")
	<-stop
	fmt.Fprintln(os.Stderr, "cleaning up")
}
