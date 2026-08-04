package main

import (
	// fan out workers: this step makes data flow and termination explicit.
	"fmt"
	// fan out workers: this step makes data flow and termination explicit.
	"sync"
)

// fan out workers: this step makes data flow and termination explicit.
func worker(id int, jobs <-chan int, results chan<- string, group *sync.WaitGroup) {
	// fan out workers: this step makes data flow and termination explicit.
	defer group.Done()
	// fan out workers: this step makes data flow and termination explicit.
	for job := range jobs {
		// fan out workers: this step makes data flow and termination explicit.
		results <- fmt.Sprintf("worker-%d processed %d", id, job)
	}
}

// fan out workers: this step makes data flow and termination explicit.
func main() {
	// fan out workers: this step makes data flow and termination explicit.
	jobs := make(chan int)
	// fan out workers: this step makes data flow and termination explicit.
	results := make(chan string, 4)
	// fan out workers: this step makes data flow and termination explicit.
	var group sync.WaitGroup
	// fan out workers: this step makes data flow and termination explicit.
	for id := 1; id <= 2; id++ {
		// fan out workers: this step makes data flow and termination explicit.
		group.Add(1)
		// fan out workers: this step makes data flow and termination explicit.
		go worker(id, jobs, results, &group)
	}
	// fan out workers: this step makes data flow and termination explicit.
	go func() {
		// fan out workers: this step makes data flow and termination explicit.
		for _, job := range []int{10, 20, 30, 40} {
			// fan out workers: this step makes data flow and termination explicit.
			jobs <- job
		}
		// fan out workers: this step makes data flow and termination explicit.
		close(jobs)
		// fan out workers: this step makes data flow and termination explicit.
		group.Wait()
		// fan out workers: this step makes data flow and termination explicit.
		close(results)
		// fan out workers: this step makes data flow and termination explicit.
	}()
	// fan out workers: this step makes data flow and termination explicit.
	for result := range results {
		// fan out workers: this step makes data flow and termination explicit.
		fmt.Println(result)
	}
}
