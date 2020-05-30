
Brute force solution to [Matt Parker's Maths Puzzle 7: Unique Distance](https://think-maths.co.uk/uniquedistance) accounting for symmetry.

1. Grab all possible combinations of points in the square.
2. For each combination, hash it and all its possible rotations/reflections to skip equivalents.
3. Compute pairwise distances between each of the points. Using squared-distances is sufficient to find duplicate distances, no need for square root.
4. Pop the distances into a set to find duplicates.
5. Print the squares that don't have duplicate distances.

Next refinement I may get to eventually:
- Use some sort of memoization or culling approach to quickly short-circuit failed squares (i.e. squares that gave it a go)

Here's both solutions for 6 coins on a 6x6 square:
```
> python .\uniquedistance.py 6 6
Computing 6 coin placements for a 6x6 square...
[O][ ][ ][ ][ ][ ]
[O][ ][ ][ ][ ][ ]
[ ][ ][ ][ ][ ][O]
[ ][O][ ][ ][ ][ ]
[ ][ ][ ][ ][ ][ ]
[ ][ ][ ][O][ ][O]

[O][ ][ ][ ][ ][ ]
[ ][ ][ ][ ][ ][ ]
[O][ ][ ][ ][ ][ ]
[ ][ ][ ][O][ ][ ]
[ ][ ][ ][ ][O][O]
[O][ ][ ][ ][ ][ ]
```
