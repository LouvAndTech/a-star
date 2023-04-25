import cv2 as cv
import json
import sys
import os

from lib.astar import *



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