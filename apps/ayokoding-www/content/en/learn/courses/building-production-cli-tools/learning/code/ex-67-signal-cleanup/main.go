package main

import (
	"fmt"
	"os"
	"os/signal"
)

func main() {
	done := make(chan os.Signal, 1)
	signal.Notify(done, os.Interrupt)
	fmt.Println("temporary file created")
	<-done
	fmt.Println("temporary file removed")
}
