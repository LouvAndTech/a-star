package astar

import "fmt"

// Pos type with x and y
type Pos struct {
	X int
	Y int
}

func reversePath(arr []Pos) []Pos {
	for i, j := 0, len(arr)-1; i < j; i, j = i+1, j-1 {
		arr[i], arr[j] = arr[j], arr[i]
	}
	return arr
}

// Node struct to contain weight parent and pos
type node struct {
	pos    Pos
	parent *node
	gScore int
	hScore int
	fScore int
}

// Node Contructor
func newNode(pos Pos, parent *node) node {
	return node{
		pos:    pos,
		parent: parent,
		gScore: 0,
		hScore: 0,
		fScore: 0,
	}
}

// Check if equal function
func (a *node) equal(b node) bool {
	if a.pos.X == b.pos.X && a.pos.Y == b.pos.Y {
		return true
	}
	return false
}

// Check if the set already contain the node
func setContainNode(set []node, el node) bool {
	for _, item := range set {
		if el.equal(item) {
			return true
		}
	}
	return false
}

// Check if a node with a better score exist
func betterNodeExist(set []node, el node) bool {
	for _, item := range set {
		if el.equal(item) {
			if el.fScore > item.fScore {
				return true
			}
		}
	}
	return false
}

type AStar struct {
	maze            [][]int
	start           Pos
	end             Pos
	allowed_moves   []Pos
	heuristic       func(Pos, Pos) int
	wall_identifier int
}

func NewAstar(maze [][]int, start Pos, end Pos, allowed_moves []Pos, heuristic func(Pos, Pos) int, wall_identifier *int) (*AStar, error) {
	wall_ident := 0
	if wall_identifier != nil {
		wall_ident = *wall_identifier
	}
	//Check if the start and goal position are withtin the maze
	if start.X < 0 || start.X > len(maze) || start.Y < 0 || start.Y > len(maze[0]) || end.X < 0 || end.X > len(maze) || end.Y < 0 || end.Y > len(maze[0]) {
		return nil, fmt.Errorf("Start position is outside the maze")
	}
	// Check if the start and end position are walls
	if maze[start.X][start.Y] == wall_ident || maze[end.X][end.Y] == wall_ident {
		return nil, fmt.Errorf("Start or Goal position is a wall")
	}

	output := AStar{
		maze:            maze,
		start:           start,
		end:             end,
		allowed_moves:   allowed_moves,
		heuristic:       heuristic,
		wall_identifier: wall_ident,
	}

	return &output, nil
}

func (a *AStar) Solve() ([]Pos, error) {
	// Check if start is the same as Goal
	if a.start.X == a.end.X && a.start.Y == a.end.Y {
		return []Pos{}, nil
	}

	// Create the two first nodes
	startNode := newNode(a.start, nil)
	goalNode := newNode(a.end, nil)

	//create the Opened and closed set

	openSet := []node{}
	closeSet := []node{}

	//Add the start to the openSet
	openSet = append(openSet, startNode)

	// loop Until the open list is empty wich mean the goal is found
	for len(openSet) > 0 {
		// Get the node with the lower cost to process next
		currentNode := openSet[0]
		currentIndex := 0
		for index, item := range openSet {
			if item.fScore < currentNode.fScore {
				currentNode = item
				currentIndex = index
			}
		}
		// Remove the current node from the open set
		copy(openSet[currentIndex:], openSet[currentIndex+1:]) // Copy everything that was after the removed element to the left.
		openSet = openSet[:len(openSet)-1]                     // Truncate slice.

		//Check if you've reached the goal
		if currentNode.equal(goalNode) {
			// Return the path
			path := []Pos{}
			for currentNode.parent != nil { // While the current node has a parent (all nodes except the start node)
				path = append(path, currentNode.pos) // Add the current node to the path
				currentNode = *currentNode.parent    // Go to the parent node
			}
			path = reversePath(path)
			return path, nil
		}

		// Create the children nodes
		children := []node{}
		for _, move := range a.allowed_moves {
			// Get the new position
			child_pos := Pos{currentNode.pos.X + move.X, currentNode.pos.Y + move.Y}

			//Check if it's contained within the maze
			if child_pos.X > len(a.maze)-1 || child_pos.X < 0 || child_pos.Y > len(a.maze[0])-1 || child_pos.Y < 0 {
				continue
			}
			//Check if it's a wall
			if a.maze[child_pos.Y][child_pos.X] == a.wall_identifier {
				continue
			}

			//Create the child node itself
			children = append(children, newNode(child_pos, &currentNode))
		}

		//Loop throught all the childrens
		for _, child := range children {

			//if the child as already being checked
			if setContainNode(closeSet, child) {
				continue
			}

			//else compute it's score
			child.gScore = currentNode.gScore + 1
			child.hScore = a.heuristic(child.pos, a.end)
			child.fScore = child.gScore + child.hScore

			//If a better node already exist in the openset no need to add it
			// This is just to improve efficiency
			if betterNodeExist(openSet, child) {
				continue
			}

			openSet = append(openSet, child)
		}

		//Then add the current node to the closed list
		closeSet = append(closeSet, currentNode)

	}

	return nil, fmt.Errorf("could not find a path")
}

func Eucliendian_distance(a Pos, b Pos) int {
	return (a.X-b.X)*(a.X-b.X) + (a.Y-b.Y)*(a.Y-b.Y)
}
