# https://think-maths.co.uk/uniquedistance
import argparse
import functools
import itertools

# Cartesian 2D point.
class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def __lt__(self, other):
    return self.y < other.y or (self.y == other.y and self.x < other.x)

  def __repr__(self):
    return "({},{})".format(self.x, self.y)

# The squared Pythagorean distance between two points.
def distance_squared(point1, point2):
  return (point2.x - point1.x)**2 + (point2.y - point1.y)**2

# Generates all pairs between a list of points.
def all_pairs(points):
  return list(itertools.combinations(points, 2))

# Returns the unique pairwise squared distances between points.
def unique_distances_squared(point_pairs):
  return {distance_squared(pair[0], pair[1]) for pair in point_pairs}

# Determines whether all pairwise distances between points are unique.
def all_distances_unique(points):
  point_pairs = all_pairs(points)
  unique_distances = unique_distances_squared(point_pairs)
  return len(unique_distances) == len(point_pairs)

# Generates a string displaying a set of points marked in a square grid.
# Example output:
# [O][ ][ ]
# [ ][O][ ]
# [ ][ ][O]
def square_grid(points, side_length):
  grid = [['[ ]' for _ in range(side_length)] for _ in range(side_length)]
  for point in points:
    grid[point.y][point.x] = '[O]'
  return '\n'.join(''.join(row) for row in grid)

# Rotates a set of points clockwise 90 degrees.
def rotate(points, side_length):
  return [Point(side_length - point.y - 1, point.x) for point in points]

# Reflects a set of points vertically.
def reflect(points, side_length):
  return [Point(point.x, side_length - point.y - 1) for point in points]

# Encodes a set of points in an NxN grid as an integer.
#
# For example, a 3x3 grid corresponds to the 9 lowest bits of an integer as such:
# [0][1][2]
# [3][4][5]
# [6][7][8]
def encode(points, side_length):
  return functools.reduce(lambda enc, point: enc | 1 << (point.x + side_length * point.y),
                          points,
                          0)

# Encodes a set of points with the smallest of any of the possible encodings of any
# symmetrically equivalent set of points.
#
# The grid is rotated and flipped to all symmetric equivalents and reencoded, and the
# minimum encoding is chosen.
def min_encoding(points, side_length):
  # Get all 4 rotations.
  all_encodings = [encode(points, side_length)]
  for _ in range(3):
    points = rotate(points, side_length)
    all_encodings.append(encode(points,side_length))

  # Flip it over and get the other 4 rotations.
  points = reflect(points, side_length)
  all_encodings.append(encode(points,side_length))
  for _ in range(3):
    points = rotate(points, side_length)
    all_encodings.append(encode(points,side_length))

  return functools.reduce(lambda a,b: a if a < b else b, all_encodings)


def main():
  parser = argparse.ArgumentParser(description="Find all possible placements of coins in a square grid of side length 'size' such that all pairwise distances between coins are unique.")
  parser.add_argument("coins", type=int, help="Number of coins.")
  parser.add_argument("size", type=int, help="The side length of the square grid.")
  args = parser.parse_args()
  print("Computing {0} coin placements for a {1}x{1} square...".format(args.coins, args.size))

  possible_points = [Point(x, y) for x in range(args.size) for y in range(args.size)]
  possible_coin_placements = itertools.combinations(possible_points, args.coins)

  for coin_placement in possible_coin_placements:
    # We don't actually call all_distances_unique() to avoid duplicating work,
    # since we want to cache the distances themselves for debugging.
    point_pairs = all_pairs(coin_placement)
    unique_distances = unique_distances_squared(point_pairs)
    if len(unique_distances) == len(point_pairs):
      print(square_grid(coin_placement, args.size))
      print()
      print(unique_distances)
      print()

if __name__ == "__main__":
  main()

