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

# Square grid with a set of marked points.
# Grid markings are considered equal if they are symmetrically equivalent.
class Grid:
  def __init__(self, points, side_length):
    self.points = points
    self.side_length = side_length

  # Generates a string displaying a set of points marked in a square grid.
  # Example output:
  # [O][ ][ ]
  # [ ][O][ ]
  # [ ][ ][O]
  def __repr__(self):
    grid = [['[ ]' for _ in range(self.side_length)] for _ in range(self.side_length)]
    for point in self.points:
      grid[point.y][point.x] = '[O]'
    return '\n'.join(''.join(row) for row in grid)

  # Generates all pairs between a list of points.
  def all_pairs(self):
    return list(itertools.combinations(self.points, 2))

  # Determines whether all pairwise distances between points are unique.
  def all_distances_unique(self):
    point_pairs = self.all_pairs()
    unique_distances = {distance_squared(pair[0], pair[1]) for pair in point_pairs}
    return len(unique_distances) == len(point_pairs)

  # Rotates the grid clockwise 90 degrees.
  def rotate(self):
    return Grid([Point(self.side_length - point.y - 1, point.x) for point in self.points],
                self.side_length)

  # Reflects a set of points vertically.
  def reflect(self):
    return Grid([Point(point.x, self.side_length - point.y - 1) for point in self.points],
                self.side_length)

  # Encodes the set of points in the grid as an integer.
  #
  # For example, a 3x3 grid corresponds to the 9 lowest bits of an integer as such:
  # [0][1][2]
  # [3][4][5]
  # [6][7][8]
  def encoding(self):
    return functools.reduce(
      lambda enc, point:
        enc | 1 << (point.x + self.side_length * point.y),
      self.points,
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

