import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from math import *

from Ray import Ray
from Cell import Cell
from Grid import Grid

rng = np.random.default_rng()

# Load the image and convert to greyscale
image = Image.open('a.png')
image = np.asarray(image)
image = np.dot(image[...,:3], [0.299, 0.587, 0.114])

# Grid variables
Nx, Ny = image.shape
Lx = 1
Ly = 1

# Create Grid object
grid = Grid(Nx, Ny, Lx, Ly, image)

# Ray variables
nb_rays = 10000

# Create rays
rays = []

for i in range(nb_rays):
	direction = (2*rng.random()-1, 2*rng.random()-1)
	origin = (Lx*rng.random(), Ly*rng.random())
	rays.append( Ray(origin, direction, id=i) )

# G matrix
G = np.zeros((len(rays), Nx*Ny))

# Fill in G matrix
for ray in rays:
	intersections = grid.getDistances(ray)
	for cell, dist in intersections.items():
		G[ray.id][cell.id] = dist

np.savetxt("G.dat", G, fmt='%f', delimiter=' ', newline='\n')

# G = np.genfromtxt("G.dat")

d = []
for ray in rays:
	d.append(ray.value)
d = np.array(d)

Ginv = np.linalg.pinv(G)
Msol = Ginv@d

# Reshape m
imagesol = Msol.reshape(image.shape)

plt.matshow(image)
plt.show()

plt.matshow(imagesol)
plt.show()
