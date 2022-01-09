import numpy as np
from math import *
from Grid import Grid

## PARAMETERS ##
# Cells
x_len = 1
y_len = 1
nb_x_cells = 3
nb_y_cells = nb_x_cells

nb_cells = nb_x_cells*nb_y_cells

len_x_cell = x_len/nb_x_cells
len_y_cell = y_len/nb_y_cells
diag_cell = sqrt(len_x_cell**2 + len_y_cell**2)

# Rays
nb_rays = nb_x_cells + nb_y_cells + 2*(nb_x_cells - 1 + nb_y_cells)

# Init G matrix
N, K = nb_rays, nb_x_cells*nb_y_cells
G = np.zeros([N, K])

grid = Grid(3, 3, 1, 1)
grid.disp()