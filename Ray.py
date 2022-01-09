from Cell import Cell
import numpy as np

class Ray(object):
	def __init__(self, origin, dir):
		self.origin = np.array(origin)
		self.direction = np.array(dir)
		
		# Avoid printing error when infinity encoutered
		with np.errstate(divide='ignore'):
			self.invDirection = np.divide(1.0, self.direction)

		# Signal along which axis the line is constant
		self.constantAxis = (self.direction == 0)

	def intersects(self, cell):
		bounds = cell.bounds

		for i, constant in enumerate(self.constantAxis):
			if( constant ):
				if( not (bounds[i][0] <= self.origin[i] <= bounds[i][1]) ):
					return False

		if( self.constantAxis[0] ):
			txmin = -np.inf
			txmax = +np.inf
		else:
			txmin = (bounds[0][0] - self.origin[0]) * self.invDirection[0]
			txmax = (bounds[1][0] - self.origin[0]) * self.invDirection[0]

		if( self.constantAxis[1] ):
			tymin = -np.inf
			tymax = +np.inf
		else:
			tymin = (bounds[0][1] - self.origin[1]) * self.invDirection[1]
			tymax = (bounds[1][1] - self.origin[1]) * self.invDirection[1]

		if( (tymax <= txmin ) or (txmax <= tymin) ):
			return False
		
		return True