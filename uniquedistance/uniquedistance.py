# https://think-maths.co.uk/uniquedistance
import argparse
import functools
import itertools

# Encodes a point in an NxN grid as an integer with one set bit.
#
# For example, a 3x3 grid corresponds to the 9 lowest bits of an integer as such:
# [0][1][2]
# [3][4][5]
# [6][7][8]
def point_encoding(x, y, side_length):
  return 1 << (x + side_length * y)

# Cartesian 2D point within a square grid of known size.
class Point:
  def __init__(self, x, y, side_length):
    self._encoding = point_encoding(x, y, side_length)
    self._side_length = side_length
    self._x = x
    self._y = y

  def __eq__(self, other):
    return self._encoding == other._encoding

  def __lt__(self, other):
    return self._encoding < other._encoding

  def encoding(self):
    return self._encoding

  def x(self):
    return self._x

  def y(self):
    return self._y

  def __repr__(self):
    return "({},{})".format(self.x(), self.y())

# The squared Pythagorean distance between two points.
def distance_squared(point1, point2):
  return (point2.x() - point1.x())**2 + (point2.y() - point1.y())**2

# Square grid on which points can be marked one by one.
# Grid markings are considered equal if they are symmetrically equivalent.
class Grid:
  def __init__(self, side_length):
    self._all_pairs = set()
    self._points = set()
    self._unique_distances_squared = set()
    self._all_distances_unique = True
    self._side_length = side_length

  # Generates a string displaying a set of points marked in a square grid.
  # Example output:
  # [O][ ][ ]
  # [ ][O][ ]
  # [ ][ ][O]
  def __repr__(self):
    grid = [['[ ]' for _ in range(self._side_length)] for _ in range(self._side_length)]
    for point in self._points:
      grid[point.y][point.x] = '[O]'
    return '\n'.join(''.join(row) for row in grid)

  def add(self, new_point):
    new_pairs = {(point, new_point) for point in self._points}
    new_distances_squared = {distance_squared(pair[0], pair[1]) for pair in new_pairs}
    if self._unique_distances_squared.intersection(new_distances_squared):
      self._all_distances_unique = False
    self._all_pairs.update(new_pairs)
    self._points.add(new_point)
    self._unique_distances_squared.update(new_distances_squared)

  # Generates all pairs between a list of points.
  def all_pairs(self):
    return self._all_pairs

  # Determines whether all pairwise distances between points are unique.
  def all_distances_unique(self):
    return _all_distances_unique

  # Rotates the grid clockwise 90 degrees.
  def rotate(self):
    return Grid([Point(self._side_length - point.y - 1, point.x) for point in self._points],
                self._side_length)

  # Reflects a set of points vertically.
  def reflect(self):
    return Grid([Point(point.x, self._side_length - point.y - 1) for point in self._points],
                self._side_length)

  # Encodes the set of points in the grid as an integer.
  #
  # For example, a 3x3 grid corresponds to the 9 lowest bits of an integer as such:
  # [0][1][2]
  # [3][4][5]
  # [6][7][8]
  def encoding(self):
    return functools.reduce(
      lambda enc, point:
        enc | 1 << (point.x + self._side_length * point.y),
      self._points,
      0)

  def all_symmetric_grids(self):
    # Get all 4 rotations.
    all_grids = []
    next_grid = self
    all_grids.append(next_grid)
    for _ in range(3):
      next_grid = next_grid.rotate()
      all_grids.append(next_grid)

    # Flip it over and get the other 4 rotations.
    next_grid = next_grid.reflect()
    all_grids.append(next_grid)
    for _ in range(3):
      next_grid = next_grid.rotate()
      all_grids.append(next_grid)

    return all_grids

  # Finds all possible encodings for symmetrically equivalent grids.
  def all_symmetric_encodings(self):
    return [grid.encoding() for grid in self.all_symmetric_grids()]

def main():
  parser = argparse.ArgumentParser(description="Find all possible placements of coins in a square grid of side length 'size' such that all pairwise distances between coins are unique.")
  parser.add_argument("coins", type=int, help="Number of coins.")
  parser.add_argument("size", type=int, help="The side length of the square grid.")
  args = parser.parse_args()
  print("Computing {0} coin placements for a {1}x{1} square...".format(args.coins, args.size))

  possible_points = [Point(x, y) for x in range(args.size) for y in range(args.size)]
  possible_coin_placements = [
    Grid(placement, args.size)
    for placement in itertools.combinations(possible_points, args.coins)]

  seen_encodings = set()
  for coin_placement in possible_coin_placements:
    if coin_placement.encoding() in seen_encodings:
      continue

    seen_encodings.update(coin_placement.all_symmetric_encodings())

    if coin_placement.all_distances_unique():
      print(coin_placement)
      print()

if __name__ == "__main__":
  main()

