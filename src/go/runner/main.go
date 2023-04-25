package main

import (
	"fmt"
	"os"
)

func main() {
	fmt.Println("Starting Astart Algotithm in Go")
	//Open the image file and read it into a 2D array
	if len(os.Args) < 2 {
		fmt.Println("Error: Please provide a file")
		os.Exit(1)
	}
	maze, err := ReadBitmap(os.Args[1])
	if err != nil {
		fmt.Println("Error: File could not be opened")
		os.Exit(1)
	}

	//Params
	start := pos{0, 0}
	goal := pos{len(maze) - 1, len(maze[0]) - 1}
	allowed_moves := []pos{{1, 0}, {0, 1}, {-1, 0}, {0, -1}}
	heuristic := eucliendian_distance
	wall_identifier := 0

	//Create the Astar object
	Astar, err := NewAstar(maze, start, goal, allowed_moves, heuristic, &wall_identifier)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	//Solve the maze
	path, err := Astar.Solve()
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	//save into a json
	err = WriteOutput(os.Args[1], heuristic, start, goal, path)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
