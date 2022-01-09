import numpy as np
from math import *
from Ray import Ray
from Cell import Cell
from Grid import Grid

grid = Grid(3, 3, 1, 1)

ray = Ray((0, 0), (-1, -1))

inter = grid._findIntersectingPoints(ray)

for cell in inter:
	cell.disp()

print("grid:")
grid.disp()