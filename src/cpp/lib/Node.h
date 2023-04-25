#ifndef NODE_H
#define NODE_H

#include "pos.h"

class Node
{
private:
    Pos pos;
    Node *parent;
    int gScore;
    int hScore;
    int fScore;
    
public:
    Node(Pos pos, Node *parent);
    ~Node();
};

Node::Node(Pos pos, Node *parent)
{
    this->pos = pos;
    this->parent = parent;
    this->gScore = 0;
    this->hScore = 0;
    this->fScore = 0;
}

Node::~Node()
{
    delete this;
}


#endif