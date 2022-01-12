import numpy as np
from math import *
from Ray import Ray
from Cell import Cell
from Grid import Grid

grid = Grid(2,2, 1, 1)

ray = Ray((1, 0), (-1, 1))

inter = grid._findIntersectingPoints(ray)

print("inter points:", inter.values())

for cell in inter:
	cell.disp()

print("grid:")
grid.disp()