#!/bin/bash
echo "Run an A* algorithm on a given map with a given binary"

MAZEPATH=''

# check if arguments are given
if [ $# -lt '2' ];
then
    echo ">>>No Argument specified !!"
    exit 1
else
    MAZEPATH=$1
    echo "Map path: $MAZEPATH"
fi

if [ $2 = '-p' ];
then
    echo "Running python version"
    python3 ./src/python/main.py $MAZEPATH
elif [ $2 = '-g' ];
then
    echo "Running go version"
    ./src/go/bin/output $MAZEPATH
fi

if [ $3 = '-v' ];
then
    search_dir=./out
    name=$(echo $(echo $MAZEPATH | tr "/" "\n" | tail -1) | tr "." "\n" | head -1)
    echo "Name: $name"

    for entry in `ls "$search_dir/$name"/*.json`
    do
        echo "$entry"
    done
    echo "Visualizing"
    python3 ./src/utils/display.py $entry
fi