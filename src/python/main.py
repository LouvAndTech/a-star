import cv2 as cv
import json
import sys
import os

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
            '''current_node = openSet[0]
            index = 0
            for index in range(len(openSet)):
                if openSet[index].fScore < current_node.fScore:
                    index = index

            #pull the current node from the openSet
            current_node = openSet.pop(index)'''
            # Get the current node with the lower cost 
            current_node = openSet[0]
            current_index = 0
            for index, item in enumerate(openSet):
                if item.fScore < current_node.fScore:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            openSet.pop(current_index)


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
            for moves in self.allowed_direction:

                child_pos = (current_node.pos[0] + moves[0], current_node.pos[1] + moves[1])

                #Check if it's within the maze 
                if (child_pos[0] > (self.map.shape[0] - 1) or child_pos[0] < 0 or child_pos[1] > (self.map.shape[1] - 1) or child_pos[1] < 0):
                    continue
                #Check if it's a wall
                if (self.map[child_pos[1], child_pos[0]] == self.wall_identifier):
                    continue

                # Create the node
                child = Node(child_pos, current_node)

                #Add the child to the children list
                children.append(child)

            #Loop through all the children
            for child in children:
                #Check if the child is already in the closed list
                #TODO: Check if it's valid (thanks to the __eq__ function) or if i need to implement it my self
                if child in closedSet:
                    continue
                
                child.gScore = current_node.gScore + 1
                child.hScore = self.hFunction(child.pos, self.goal.pos)
                child.fScore = child.gScore + child.hScore

                # Child is already in the open list and has a lower cost
                # FIXME Not sure this is working
                for node in openSet:
                    if child == node and child.gScore > node.gScore:
                        continue

                openSet.append(child)

            #add the current node to the closed list
            closedSet.append(current_node)



# Write result to a json
def write(mazePath, mazeFileName , path, start, goal, heuristic):
    #Create an folder to store the paths
    if not os.path.exists("out"):
        os.makedirs("out")
    if not os.path.exists("out/"+mazeFileName):
        os.makedirs("out/"+mazeFileName)
    #Create a json file to store the path the start and the goal
    data = {}
    data["mazePath"] = mazePath
    data['start'] = start
    data["goal"] = goal
    data["path"] = path
    filename = "paths_%s_%s-%s_%s-%s.json" % (heuristic, start[0], start[1], goal[0],goal[1])
    with open("out/"+mazeFileName+"/"+filename, 'w') as outfile:
        json.dump(data, outfile , indent = 4)




# Heuristic functions 

def euclidean(a, b):
    return ((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2)

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def chebyshev(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

def plain(a, b):
    return 1


if (__name__ == "__main__"):

    if (len(sys.argv) != 2):
        print("Usage: python3 main.py <image_path>")
        sys.exit(1)

    # Read the image with the map
    maze = cv.imread(sys.argv[1], cv.IMREAD_GRAYSCALE)
    # Switch to a ones and zeros map
    maze = maze / 255
    mazeName = sys.argv[1].split('/').pop().split('.')[0]

    #Params
    start = (0, 0)
    goal = (maze.shape[0]-1 ,maze.shape[1]-1)
    allowed_direction = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    wallidentifier = 0
    heuristic_functions = [euclidean]

    for h in heuristic_functions:
        algo = AStar(maze, start, goal,allowed_direction, h, wallidentifier)
        path = algo.compute()

        # Write the result to a json
        write(sys.argv[1],mazeName, path, start, goal, h.__name__)