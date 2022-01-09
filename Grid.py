from Ray import Ray
from Cell import Cell

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
		Cy= self.Ly/self.Ny

		counter = 0

		for iy in range(self.Ny):
			for ix in range(self.Nx):
				self.grid[counter] = Cell(ix*Cx, (ix+1)*Cx, iy*Cy, (iy+1)*Cy, counter)
				counter += 1
	
		
	def _findIntersectingPoints(self, ray):
		intersections = {}

		#TODO: test if grid exists
		for cell in self.grid:
			if( ray.intersects(cell) ):
				# intersections[cell] = self.getIntersection(ray, cell)
				intersections[cell] = cell

		return intersections

	# def getDistances(self, ray):
	# 	intersections = self._findIntersectingPoints(ray)

	# 	distances = {}
	# 	for cell_id, points in intersections.items():
	# 		distances[cell_id] = self.getDistance(points)
		
	# 	return 0
	
	def disp(self):
		for cell in self.grid:
			cell.disp()