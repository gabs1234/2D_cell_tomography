from Ray import Ray
from Cell import Cell

import numpy as np

class Grid(object):
	eps = np.finfo(np.float32).eps
	
	def __init__(self, Nx, Ny, Lx, Ly, image=None):
		self.Nx = Nx
		self.Ny = Ny
		self.Lx = Lx
		self.Ly = Ly

		self.maxLen = ((self.Lx/self.Nx)**2 + (self.Ly/self.Ny)**2)**.5

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
			tmp_dist = self._calcDistance(points)
			if( self.eps < tmp_dist <= self.maxLen+self.eps):
				distances[cell_id] = tmp_dist
		
		return distances
	
	def disp(self):
		for cell in self.grid:
			cell.disp()