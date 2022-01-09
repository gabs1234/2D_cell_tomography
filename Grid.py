class cell(object):
	def __init__(self, xmin, xmax, ymin, ymax, id):
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax
		self.id = id
	
	def getBounds(self):
		return ((self.xmin, self.ymin), (self.xman, self.ymax))

	def disp(self):
		print("{}: ".format(self.id), [self.xmin, self.xmax, self.ymin, self.ymax])

class Grid(object):
	def __init__(self, Nx, Ny, Lx, Ly):
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
				self.grid[counter] = cell(ix*Cx, (ix+1)*Cx, iy*Cy, (iy+1)*Cy, counter)
				counter += 1
	
	def _intersects(self, cell):
		bounds = cell.getBounds()

		for i in range(len(self.constantAxis)):
			if( self.constantAxis[i] ):
				if( not (cellBounds[2*i] <= self.startPoint[i] <= cellBounds[2*i+1]) ):
					return False

		if( self.constantAxis[0] ):
			tmin = -np.inf
			tmax = +np.inf
		else:
			tmin = (bounds[:, self.sign[0]][0] - self.startPoint[0]) * self.invDirection[0]
			tmax = (bounds[:, 1 - self.sign[0]][0] - self.startPoint[0]) * self.invDirection[0]

		if( self.constantAxis[1] ):
			tymin = -np.inf
			tymax = +np.inf
		else:
			tymin = (bounds[:, self.sign[1]][1] - self.startPoint[1]) * self.invDirection[1]
			tymax = (bounds[:, 1 - self.sign[1]][1] - self.startPoint[1]) * self.invDirection[1]

		if( (tmin >= tymax) or (tymin >= tmax) ):
			return False
		if( tymin > tmin ):
			tmin = tymin
		if( tymax < tmax ):
			tmax = tymax

		# Check that we are in the rectangular box defined by our segment
		return (0 <= tmin) and (tmax <= 1)

	def findIntersectingCells(self, ray):
		self.sign = np.where(ray.direction < 0, [1]*ray.direction, [0]*ray.direction)

		# Avoid printing error when infinity encoutered
		with np.errstate(divide='ignore'):
			self.invDirection = np.divide(1.0, ray.direction)

		# Signal along which axis the line is constant
		self.constantAxis = (ray.direction == 0)

		for cell in self.
		
		return 0
	
	def disp(self):
		for cell in self.grid:
			cell.disp()