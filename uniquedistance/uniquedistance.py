# https://think-maths.co.uk/uniquedistance
import itertools

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

def distance_squared(point1, point2):
  return (point2.x - point1.x)**2 + (point2.y - point1.y)**2

def all_distances_squared(points):
  pairs = list(itertools.combinations(points, 2))
  return [distance_squared(pair[0], pair[1]) for pair in pairs]

def all_distances_unique(points):
  pairs = list(itertools.combinations(points, 2))
  unique_distances = {distance_squared(pair[0], pair[1]) for pair in pairs}
  return len(unique_distances) == len(pairs)

def print_square_grid(points, side_length):
  grid = [["[ ]" for _ in range(side_length)] for _ in range(side_length)]
  for point in points:
    grid[point.x][point.y] = "[O]"
  return '\n'.join(''.join(row) for row in grid)
