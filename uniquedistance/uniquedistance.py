# https://think-maths.co.uk/uniquedistance
class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def __lt__(self, other):
    return self.y < other.y or (self.y == other.y and self.x < other.x)

def distance_squared(point1, point2):
  return (point2.x - point1.x)**2 + (point2.y - point1.y)**2

