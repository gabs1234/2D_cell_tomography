from Cell import Cell
import numpy as np

class Ray(object):
	def __init__(self, origin, dir):
		self.origin = np.array(origin)
		self.direction = np.array(dir)
		
		self.sign = np.where(self.direction < 0, [1]*len(self.direction), [0]*len(self.direction))

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
			tmin = -np.inf
			tmax = +np.inf
		else:
			tmin = (bounds[:, self.sign[0]][0] - self.origin[0]) * self.invDirection[0]
			tmax = (bounds[:, 1 - self.sign[0]][0] - self.origin[0]) * self.invDirection[0]

		if( self.constantAxis[1] ):
			tymin = -np.inf
			tymax = +np.inf
		else:
			tymin = (bounds[:, self.sign[1]][1] - self.origin[1]) * self.invDirection[1]
			tymax = (bounds[:, 1 - self.sign[1]][1] - self.origin[1]) * self.invDirection[1]

		if( (tmin >= tymax) or (tymin >= tmax) ):
			return False
		
		return True