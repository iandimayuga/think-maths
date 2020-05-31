# Tools to help solve MPMP7: https://think-maths.co.uk/uniquedistance
import argparse
import functools
import itertools
import math

# Encodes a point in an NxN grid as an integer with one set bit.
#
# For example, a 3x3 grid corresponds to the 9 lowest bits of an integer as such:
# [0][1][2]
# [3][4][5]
# [6][7][8]
def point_encoding(x, y, side_length):
  return 1 << (x + side_length * y)

# 2D point within a square grid of known size.
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

  def __hash__(self):
    return self.encoding()

  def __repr__(self):
    return "({},{})".format(self.x(), self.y())

  def x(self):
    return self._x

  def y(self):
    return self._y

  def side_length(self):
    return self._side_length

  def encoding(self):
    return self._encoding

  # Rotates the point clockwise 90 degrees within the grid.
  def rotate(self):
    return Point(self._side_length - self.y() - 1, self.x(), self._side_length)

  # Reflects a point vertically across the grid.
  def reflect(self):
    return Point(self.x(), self._side_length - self.y() - 1, self._side_length)

  def all_symmetric_points(self):
    # Get all 4 rotations.
    all_points = []
    next_point = self
    all_points.append(next_point)
    for _ in range(3):
      next_point = next_point.rotate()
      all_points.append(next_point)

    # Flip it over and get the other 4 rotations.
    next_point = next_point.reflect()
    all_points.append(next_point)
    for _ in range(3):
      next_point = next_point.rotate()
      all_points.append(next_point)

    return all_points

  # Finds all possible encodings for symmetrically equivalent points.
  def all_symmetric_encodings(self):
    return [point.encoding() for point in self.all_symmetric_points()]

# The squared Pythagorean distance between two points.
def distance_squared(point1, point2):
  return (point2.x() - point1.x())**2 + (point2.y() - point1.y())**2

# Square grid on which points can be marked one by one.
# Grid markings are considered equal if they are symmetrically equivalent.
# Markings can be removed from the grid one by one.
# Grid has "failed" and cannot be added to if there are any duplicate distances between points.
class Grid:
  def __init__(self, side_length):
    self._points = []
    self._unique_distances_squared = []
    self._all_distances_unique = True
    self._all_symmetric_encodings = [0]*8
    self._side_length = side_length

  def __bool__():
    return bool(self._points)

  def __len__(self):
    return len(self._points)

  # Generates a string displaying a set of points marked in a square grid.
  # Example output:
  # [O][ ][ ]
  # [ ][O][ ]
  # [ ][ ][O]
  def __repr__(self):
    grid = [['[ ]' for _ in range(self._side_length)] for _ in range(self._side_length)]
    for point in self._points:
      grid[point.y()][point.x()] = '[O]'
    return '\n'.join(''.join(row) for row in grid)

  def add(self, new_point):
    if new_point.side_length() != self._side_length:
      raise ValueError("Grid of side length {} cannot accept point for different side length {}"
        .format(self._side_length, new_point.side_length()))

    # This allows us to enforce the invariant that _all_distances_unique is True after popping,
    # so we do not have to recalculate all the distances when popping a coin.
    if not self._all_distances_unique:
      raise ValueError("Cannot add new point to failed grid.")

    if new_point in self._points:
      raise ValueError("Point {} already in grid.".format(new_point))

    new_pairs = {(point, new_point) for point in self._points}

    new_distances_squared = [distance_squared(pair[0], pair[1]) for pair in new_pairs]

    # Check if any of the new distances are the same as each other.
    new_distances_set = set(new_distances_squared)
    if (len(new_distances_set) < len(new_distances_squared)):
      self._all_distances_unique = False

    # Check if any of the new distances are the same as any of the existing distances.
    if set(self._unique_distances_squared).intersection(new_distances_set):
      self._all_distances_unique = False

    self._unique_distances_squared.extend(new_distances_squared)

    self._points.append(new_point)

    # OR the new point's symmetric encodings in with the grid's encodings.
    self._all_symmetric_encodings = [
      enc[0] | enc[1] for enc in
      zip(self._all_symmetric_encodings, new_point.all_symmetric_encodings())]

  def pop(self):
    old_point = self._points.pop()

    # Remove the last N distances added.
    for _ in range(len(self._points)):
      self._unique_distances_squared.pop()

    # Invariant as long as add() is disallowed for non-unique-distance grids.
    self._all_distances_unique = True

    # XOR the old point's symmetric encodings out of the grid's encodings.
    self._all_symmetric_encodings = [
      enc[0] ^ enc[1] for enc in
      zip(self._all_symmetric_encodings, old_point.all_symmetric_encodings())]

    return old_point

  # Determines whether all pairwise distances between points are unique.
  def all_distances_unique(self):
    return self._all_distances_unique

  # Encodes the set of points in the grid as an integer.
  #
  # For example, a 3x3 grid corresponds to the 9 lowest bits of an integer as such:
  # [0][1][2]
  # [3][4][5]
  # [6][7][8]
  def encoding(self):
    return self._all_symmetric_encodings[0]

  # Finds all possible encodings for symmetrically equivalent grids.
  def all_symmetric_encodings(self):
    return self._all_symmetric_encodings

progress = 0

# Depth-first search through possible grids by adding remaining points.
# Returns list of all uniquely distanced grids.
def find_unique_grids(grid, max_points, remaining_points, seen_encodings, total_combos):
  global progress
  progress += 1
  print("Generated {}/{} grids...".format(progress, total_combos), end='\r', flush=True)

  # Base case: Grid has already been seen.
  if grid.encoding() in seen_encodings:
    return []

  seen_encodings.update(grid.all_symmetric_encodings())

  # Base case: Grid does not have all unique distances.
  if not grid.all_distances_unique():
    return []

  # Base case: Success! Grid has max points and all distances are unique.
  if len(grid) >= max_points:
    return [str(grid)]

  successful_grids = []

  # Try adding each of the remaining points to the grid one by one.
  for point in remaining_points:
    grid.add(point)
    successful_grids.extend(find_unique_grids(grid,
                                              max_points,
                                              remaining_points - {point},
                                              seen_encodings,
                                              total_combos))
    removed = grid.pop()

  return successful_grids

def main():
  parser = argparse.ArgumentParser(description="Find all possible placements of coins in a square grid of side length 'size' such that all pairwise distances between coins are unique.")
  parser.add_argument("coins", type=int, help="Number of coins.")
  parser.add_argument("size", type=int, help="The side length of the square grid.")
  args = parser.parse_args()
  print("Computing {0} coin placements for a {1}x{1} square...".format(args.coins, args.size))
  print()

  grid = Grid(args.size)
  possible_points = frozenset({Point(x, y, args.size) for x in range(args.size) for y in range(args.size)})

  seen_encodings = set()

  # Find the theoretical maximum number of grids for printing progress.
  total_combos = math.comb(args.size**2, args.coins)

  # Do the depth-first boogie.
  successful_grids = find_unique_grids(grid, args.coins, possible_points, seen_encodings, total_combos)

  print()
  print()
  print("Found {} unique solutions!".format(len(successful_grids)))
  print()

  for grid in successful_grids:
    print(grid)
    print()

if __name__ == "__main__":
  main()

