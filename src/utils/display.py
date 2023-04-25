import cv2 as cv
import numpy as np
import sys
import json
import os

def display(maze, path):
    # Draw the path
    scale_ratio = 50
    resizedMap = cv.resize(maze, None, fx=scale_ratio, fy=scale_ratio, interpolation=cv.INTER_NEAREST)
    display = cv.cvtColor(np.float32(resizedMap),cv.COLOR_GRAY2RGB)
    for i in range(len(path)-2):
        cv.line(display,(path[i][0]*scale_ratio+25,path[i][1]*scale_ratio+25),(path[i+1][0]*scale_ratio+25,path[i+1][1]*scale_ratio+25),(0, 255, 0),5)

    cv.imshow("map", display)
    cv.waitKey(0)
    cv.destroyAllWindows()

if (__name__ == "__main__"):
    if (len(sys.argv) != 2):
        print("Usage: python3 main.py <path_path>")
        sys.exit(1)

    #Read from json
    if os.path.exists(sys.argv[1]):
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
    # Read the image with the map
    maze = cv.imread(data["mazePath"], cv.IMREAD_GRAYSCALE)
    # Switch to a ones and zeros map
    maze = maze / 255
    
    display(maze, data["path"])