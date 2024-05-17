package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"
	"sync" // Import sync package for WaitGroup
)

func main() {
	data, err := os.ReadFile("./input.txt")
	if err != nil {
		log.Fatal(err)
	}

	lines := strings.Split(string(data), "\n")
	var wg sync.WaitGroup // Create a WaitGroup to manage goroutines
	wg.Add(len(lines))

	for _, line := range lines {
		go func(line string) {
			defer wg.Done() // Signal completion after processing the line

			data, err := getData(line)
			if err != nil {
				log.Printf("unable to get status: %v", err)
				return
			}
			if data == "foo" {
				fmt.Printf("data found: %s", data)
				os.Exit(0) // Exit only the current goroutine
			}
		}(line)
	}

	wg.Wait() // Wait for all goroutines to finish before exiting main
}

func getData(line string) (string, error) {
	var location struct {
		URL string `json:"location"`
	}
	if err := json.Unmarshal([]byte(line), &location); err != nil {
		return "", err
	}

	req, err := http.NewRequestWithContext(context.Background(), http.MethodGet, location.URL, nil)
	if err != nil {
		return "", err
	}

	c := &http.Client{}
	res, err := c.Do(req)
	if err != nil {
		return "", err
	}
	defer res.Body.Close() // Ensure proper closing of response body

	var payload map[string]interface{} // Use map for flexible response data
	if err := json.NewDecoder(res.Body).Decode(&payload); err != nil {
		return "", err
	}

	data, ok := payload["data"].(string) // Check if "data" key exists and is string
	if !ok {
		return "", fmt.Errorf("data key not found or not a string")
	}
	return data, nil
}
