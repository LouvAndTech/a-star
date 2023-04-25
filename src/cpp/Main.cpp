#include <iostream>
#include "lib/Pos.h"
#include "lib/Astar.h"
int main(void){
    //Read the bitmap file as a 2D array
    int maze[10][10] = {
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 1, 1, 1, 1, 1, 1, 1, 1, 0},
        {0, 1, 1, 1, 1, 1, 1, 1, 1, 0},
        {0, 1, 1, 1, 1, 1, 1, 1, 1, 0},
        {0, 1, 1, 1, 1, 1, 1, 1, 1, 0},
        {0, 1, 1, 1, 1, 1, 1, 1, 1, 0},
        {0, 1, 1, 1, 1, 1, 1, 1, 1, 0},
        {0, 1, 1, 1, 1, 1, 1, 1, 1, 0},
        {0, 1, 1, 1, 1, 1, 1, 1, 1, 0}
    };

    //Params 
    Pos *startPos = new Pos(0, 0);
    Pos *endPos = new Pos(9, 9);
    vector<Pos> allowedMoves = {new Pos(0, 1), new Pos(1, 0), new Pos(0, -1), new Pos(-1, 0)};
    int wallIdentifier = 1;
    
    Astar a = new Astar(maze, 10, 10, startPos, endPos, allowedMoves, wallIdentifier);
    return 0;
}