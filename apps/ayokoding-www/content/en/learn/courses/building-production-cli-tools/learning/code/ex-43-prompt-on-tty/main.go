package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	info, _ := os.Stdin.Stat()
	if info.Mode()&os.ModeCharDevice == 0 {
		fmt.Println("refusing interactive prompt on piped input")
		return
	}
	fmt.Print("Publish? [y/N] ")
	answer, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	fmt.Printf("answer=%q\n", answer)
}
