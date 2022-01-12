import numpy as np
from math import *
from Ray import Ray
from Cell import Cell
from Grid import Grid

grid = Grid(2,2, 1, 1)

ray = Ray((.4, 0), (1, 1))

inter = grid.getDistances(ray)

print("inter points:", inter)

for cell in inter:
	cell.disp()

print("grid:")
grid.disp()