Astar::Astar(int *maze, int mazeWidth, int mazeHeight, Pos startPos, Pos endPos, vector<Pos> allowedMoves, int wallIdentifier){

    //Check if the start and end positions are walls
    if(maze[startPos->x][startPos->y] == wallIdentifier || maze[endPos->x][endPos->y] == wallIdentifier){
        std::cout << "Start or end position is a wall" << std::endl;
        return;
    }
    //Check if the start and end positions are within the maze
    if(startPos->x < 0 || startPos->x >= mazeWidth || startPos->y < 0 || startPos->y >= mazeHeight){
        std::cout << "Start position is outside the maze" << std::endl;
        return;
    }

    this->maze = maze;
    this->mazeWidth = mazeWidth;
    this->mazeHeight = mazeHeight;
    this->startPos = startPos;
    this->endPos = endPos;
    this->allowedMoves = allowedMoves;
    this->wallIdentifier = wallIdentifier;
    return;
}

Astar::~Astar()
{
    delete this;
}
