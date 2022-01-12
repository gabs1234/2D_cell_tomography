from Ray import Ray
from Cell import Cell

import numpy as np

class Grid(object):
	def __init__(self, Nx, Ny, Lx, Ly, image=None):
		self.Nx = Nx
		self.Ny = Ny
		self.Lx = Lx
		self.Ly = Ly

		self._initBuild()

	def _initBuild(self):
		n = self.Nx*self.Ny
		self.grid = [0]*n

		Cx = self.Lx/self.Nx
		Cy = self.Ly/self.Ny

		counter = 0

		for iy in range(self.Ny):
			for ix in range(self.Nx):
				self.grid[counter] = Cell(ix*Cx, (ix+1)*Cx, iy*Cy, (iy+1)*Cy, counter)
				counter += 1

	def _findIntersectingPoints(self, ray):
		#TODO: test if grid exists
		for cell in self.grid:
			ray.intersects(cell)

		return ray.points
	
	def _calcDistance(self, points):

		points = np.array(points)
		vec = points[1] - points[0]
		return (vec[0]**2 + vec[1]**2)**.5

	def getDistances(self, ray):
		intersections = self._findIntersectingPoints(ray)

		distances = {}
		for cell_id, points in intersections.items():
			distances[cell_id] = self._calcDistance(points)
		
		return distances
	
	def disp(self):
		for cell in self.grid:
			cell.disp()