# Summary

This week's puzzle is pathfinding.

Given a maze, and 2 points in that maze, find the length of the
shortest path between those points.

# Input

An integer, h
0 <= h <= 10

h strings, all of the same length (w)

Each string will be made of these characters:
'#'  -> Wall tile
'_'  -> Floor tile
'.'  -> Path terminus point, exactly 2 of this tile will exist among all lines

Input will be provided on the stdin stream

# Output

A single integer, the shortest path between the two path terminus tiles, in # of tiles.
The terminus points should be included in the path length. Paths must not use diagonal movements.

Output should be provided on the stdout stream, with a single integer on each line.

# Example

## Input:

3
.___
###_
.___

## Output:

9
