#ifndef POS_H
#define POS_H

class Pos
{
public:
    Pos(int x, int y);
    ~Pos();

    int x;
    int y;
};

Pos::Pos(int x, int y)
{
    this->x = x;
    this->y = y;
}

Pos::~Pos()
{
    delete this;
}


#endif