package main

// happens before channel: this diagnostic keeps synchronization and cleanup observable.
import "fmt"

// happens before channel: this diagnostic keeps synchronization and cleanup observable.
type configuration struct {
	// happens before channel: this diagnostic keeps synchronization and cleanup observable.
	port int
}

// happens before channel: this diagnostic keeps synchronization and cleanup observable.
func main() {
	// happens before channel: this diagnostic keeps synchronization and cleanup observable.
	ready := make(chan configuration)
	// happens before channel: this diagnostic keeps synchronization and cleanup observable.
	go func() {
		// happens before channel: this diagnostic keeps synchronization and cleanup observable.
		config := configuration{port: 8080}
		// happens before channel: this diagnostic keeps synchronization and cleanup observable.
		ready <- config
		// happens before channel: this diagnostic keeps synchronization and cleanup observable.
	}()
	// happens before channel: this diagnostic keeps synchronization and cleanup observable.
	config := <-ready
	// happens before channel: this diagnostic keeps synchronization and cleanup observable.
	fmt.Println("published-port", config.port)
}
