#ifndef ASTAR_H
#define ASTAR_H

#include <vector>

class Astar
{
private:
    int *maze;
    int mazeWidth;
    int mazeHeight;
    
    Pos *startPos;
    Pos *endPos;

    int heuristic(Pos *pos1, Pos *pos2);
    int wallIdentifier;

    vector<Pos> allowedMoves;
public:
    Astar(int*, int, int, Pos*, Pos*, vector<Pos>, int);
    ~Astar();
};



#endif