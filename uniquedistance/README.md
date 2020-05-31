Depth-first search solution to
[Matt Parker's Maths Puzzle 7: Unique Distance](https://think-maths.co.uk/uniquedistance),
accounting for symmetry.

## Algorithm

1. Start with an empty grid.
2. Perform a depth-first search:
3. Choose an available point and add it to the grid.
4. Encode the grid state and all its symmetric equivalents with a unique binary representation.
5. Calculate the (squared) distances from the existing points in the grid to the new point.
6. Remove the coin if the resulting grid has been seen before or if there are any duplicate distances.
7. If the desired number of coins has been reached, print the grid.
8. Go back and pick a new point.

The number of coins is arbitrary and independent of the size of the square.  
Currently the code assumes square grids, but could be easily adapted for arbitrary rectangles.

We also keep track of the performance in terms of the number of grids generated
(and thereby the number of times we measure distances).  
We compare this to the expected number of combinations of C coins on an LxL grid (LxL choose C).

Interestingly for a 3x3 square, we generate more grids than the total (90/84).  
This is because we include all the intermediate grids with 0, 1, or 2 coins.  
Ultimately this tradeoff scales hugely for larger grids,
because it prunes the whole branch as soon as we hit a duplicate distance.

## Results
- 3 in a 3x3: 5 solutions
- 4 in a 4x4: 23 solutions
- 5 in a 5x5: 35 solutions
- 6 in a 6x6: 2 solutions
- 7 in a 7x7: 1 solution
- 8 in an 8x8: 0 solutions

Here's both solutions for 6 coins on a 6x6 square:
```
> python .\uniquedistance.py 6 6
Computing 6 coin placements for a 6x6 square...

Generated 164623/1947792 grids...

Found 2 unique solutions!

[O][ ][ ][ ][ ][ ]
[ ][ ][ ][ ][ ][ ]
[O][ ][ ][ ][ ][ ]
[ ][ ][ ][O][ ][ ]
[ ][ ][ ][ ][O][O]
[O][ ][ ][ ][ ][ ]

[O][ ][ ][O][ ][ ]
[ ][ ][ ][ ][ ][ ]
[O][ ][ ][ ][ ][ ]
[ ][ ][ ][ ][ ][ ]
[ ][ ][O][ ][ ][ ]
[ ][ ][ ][ ][O][O]
```

And the single solution for 7 coins on a 7x7 square:
```
> python .\uniquedistance.py 7 7
Computing 7 coin placements for a 7x7 square...

Generated 1678910/85900584 grids...

Found 1 unique solutions!

[O][ ][ ][ ][ ][ ][ ]
[ ][O][ ][ ][ ][ ][ ]
[ ][ ][ ][ ][ ][ ][ ]
[ ][ ][ ][ ][ ][ ][O]
[O][ ][ ][ ][ ][ ][ ]
[ ][ ][ ][ ][O][ ][ ]
[ ][ ][ ][ ][O][ ][O]
```

And just for completeness... 8x8:
```
> python .\uniquedistance.py 8 8
Computing 8 coin placements for a 8x8 square...

Generated 17143985/4426165368 grids...

Found 0 unique solutions!
```

## Conjecture
I don't think there are any solutions past 8x8.

I suspect there exists a proof by induction that goes something like this:  
*If you cannot fit N coins in an N x N grid (i.e. starting at 8), then you cannot fit N+1 coins in an N+1 x N+1 grid.*

My guess is it has something to do with having to fit two more coins in the final row and column.

```
The N+1 x N+1 square:
.  .  .  .  .  .  [ ]
.  .  .  .  .  .  [ ]
. Only up to N-1  [ ]
.  coins may go   [ ] <---
.  .   here!   .  [ ]     |
.  .  .  .  .  .  [ ]     |
.  .  .  .  .  .  [ ]     |
[ ][ ][ ][ ][ ][ ][ ] <---Two coins have to go somewhere here
```

There's some pattern with the smaller squares.  
For one, every solution so far from sizes 3 to 7 leaves at least one row or one column empty.  
This screams "pigeonhole principle" to me.

This is probably as far as I'll get this week. I look forward to Matt's video :)
