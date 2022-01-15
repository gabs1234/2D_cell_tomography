from Ray import Ray
from Cell import Cell

import numpy as np

class Grid(object):
	eps = np.finfo(np.float32).eps
	
	def __init__(self, Nx, Ny, Lx, Ly, image=None):
		if( isinstance(image, type(None)) ):
			self.Nx = Nx
			self.Ny = Ny
		else:
			self.Nx = image.shape[1]
			self.Ny = image.shape[0]

		self.Lx = Lx
		self.Ly = Ly

		self.maxLen = ((self.Lx/self.Nx)**2 + (self.Ly/self.Ny)**2)**.5

		if( isinstance(image, type(None)) ):
			self._initBuild()
		else:
			self._initBuild(image)

	def _initBuild(self, image=None):
		n = self.Nx*self.Ny
		self.grid = [0]*n

		Cx = self.Lx/self.Nx
		Cy = self.Ly/self.Ny

		counter = 0

		if( isinstance(image, type(None)) ):
			for iy in range(self.Ny):
				for ix in range(self.Nx):
					self.grid[counter] = Cell(ix*Cx, (ix+1)*Cx, iy*Cy, (iy+1)*Cy, counter)
					counter += 1
		else:
			for iy, col in enumerate(image):
				for ix, val in enumerate(col):
					self.grid[counter] = Cell(ix*Cx, (ix+1)*Cx, iy*Cy, (iy+1)*Cy, counter, val)
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
		print("  (xmin xmax) (ymin ymax)")
		for cell in self.grid:
			cell.disp()