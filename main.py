import numpy as np
from math import *
from Ray import Ray
from Cell import Cell
from Grid import Grid

# Grid variables
Nx = 3
Ny = 3
Lx = 1
Ly = 1

# Ray variables
nb_rays = 3

# Create rays
rays = []
# Horizontal rays
direction = (1, 0)
for i in range(nb_rays):
	origin = (0, (2*i+1)/6)
	rays.append( Ray(origin, direction) )

# Vertical rays
direction =  (0, 1)
for i in range(nb_rays):
	origin = ((2*i+1)/6, 0)
	rays.append( Ray(origin, direction) )

# Diag up rays
direction =  (1, 1)
for i in range(nb_rays):
	origin = (0, i/3)
	rays.append( Ray(origin, direction) )
for i in range(1, nb_rays):
	origin = (i/3, 0)
	rays.append( Ray(origin, direction) )

# Diag down rays
direction =  (1, -1)
for i in range(nb_rays):
	origin = (i/3, Ly)
	rays.append( Ray(origin, direction) )
for i in range(1, nb_rays):
	origin = (0, i/3)
	rays.append( Ray(origin, direction) )

# G matrix
G = np.zeros((len(rays), Nx*Ny))

# Create Grid object
grid = Grid(Nx,Ny, Lx, Ly)

# Create rays and fill in G matrix
for i, ray in enumerate(rays):
	print("ray:", i)
	intersections = grid.getDistances(ray)
	ray.disp()
	for cell, dist in intersections.items():
		G[i][cell.id] = dist
		

np.savetxt("G.dat", G, delimiter=' ', newline='\n')