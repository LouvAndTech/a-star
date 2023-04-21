import numpy as np
import cv2 as cv
import sys

class Node ():
    def __init__(self, pos, parent):
        self.pos = pos
        self.parent = parent

        self.gScore = 0
        self.hScore = 0
        self.fScore = 0

    def __eq__(self, other):
        return self.pos == other.pos

class AStar:
    def __init__(self, maze, start, goal, allowed_direction, heuractic_function , wall_identifier=0):
        #Mandatory
        self.map = maze
        self.start = start
        self.goal = goal
        self.allowed_direction = allowed_direction
        #TODO : Implement the heuristic function as a parameter
        self.hFunction = heuractic_function

        #optional
        self.wall_identifier = wall_identifier
        
        # Check for valid start
        if (self.start[0] < 0 or self.start[0] >= self.map.shape[0] or self.start[1] < 0 or self.start[1] >= self.map.shape[1] or self.map[self.start[0], self.start[1]] == 0):
            raise ValueError("Invalid start position")
        # Check for valid goal
        if (self.goal[0] < 0 or self.goal[0] >= self.map.shape[0] or self.goal[1] < 0 or self.goal[1] >= self.map.shape[1] or self.map[self.goal[0], self.goal[1]] == 0):
            raise ValueError("Invalid start position")

    def compute(self):
        # Check if start is equal to goal
        if(self.start == self.goal):
            return []
        self.start= Node(self.start, None)
        self.goal = Node(self.goal, None)

        # Create open and closed list
        openSet = []
        closedSet = []

        # Add the start node to the open list
        openSet.append(self.start)

        # Loop until the open list is empty wich mean that the goal is found
        while (len(openSet)>0):
            #retireve the node with the lowest cost
            current_node = openSet[0]
            index = 0
            for index in range(len(openSet)):
                if openSet[index].fScore < current_node.fScore:
                    index = index

            #pull the current node from the openSet
            current_node = openSet.pop(index)


            #Check if you've reached the goal
            if current_node == self.goal:
                #Start an empty list
                path = []
                #While we've not reached the start
                while current_node is not None:
                    #Add the current node to the path
                    path.append(current_node.pos)
                    #retieve to the parent node
                    current_node = current_node.parent
                # return the path but reversed from start to goal
                return path[::-1]
            
            #Create all children for the current node
            children = []
            print(self.allowed_direction)
            for moves in self.allowed_direction:

                child_pos = (current_node.pos[0] + moves[0], current_node.pos[1] + moves[1])

                #Check if it's within the maze 
                if (child_pos[0] > (self.map.shape[0] - 1) or child_pos[0] < 0 or child_pos[1] > (self.map.shape[1] - 1) or child_pos[1] < 0):
                    continue
                #Check if it's a wall
                if (self.map[child_pos[0], child_pos[1]] == self.wall_identifier):
                    continue

                # Create the node
                child = Node(child_pos, current_node)

                #Check if the child is already in the closed list
                #TODO: Check if it's valid (thanks to the __eq__ function) or if i need to implement it my self
                if child in closedSet:
                    continue
                
                child.gScore = current_node.gScore + 1
                child.hScore = self.hFunction(child.pos, self.goal.pos)
                child.fScore = child.gScore + child.hScore

                # Child is already in the open list and has a lower cost
                for node in openSet:
                    if child == node and child.gScore > node.gScore:
                        continue

                openSet.append(child)

            #add the current node to the closed list
            closedSet.append(current_node)

def heuracticFunction1(actual,goal):
    return ((actual[0] - goal[0]) ** 2) + ((actual[1] - goal[1]) ** 2)


if (__name__ == "__main__"):
    # Read the image with the map
    maze = cv.imread(sys.argv[1], cv.IMREAD_GRAYSCALE)
    # Switch to a ones and zeros map
    maze = maze / 255

    # Implement the algorithm here
    #algo = aStar(maze, (0, 0), (maze.shape[0] - 1, maze.shape[1] - 1))

    #Params 

    algo = AStar(maze, (0, 0), (maze.shape[0]-1 ,maze.shape[1]-1),[(0, -1), (0, 1), (-1, 0), (1, 0)], heuracticFunction1)
    path = algo.compute()
    print(maze)
    print(path)

