from Cell import Cell
import numpy as np

class Ray(object):
	

	def __init__(self, origin, dir):
		self.origin = np.array(origin)
		self.direction = np.array(dir)
		
		# Avoid printing error when infinity encoutered
		with np.errstate(divide='ignore'):
			self.invDirection = np.divide(1.0, self.direction)
		
		self.sign = np.array([inv < 0 for inv in self.invDirection])

		# Signal along which axis the line is constant
		self.constantAxis = (self.direction == 0)
		self.points = {}


	def intersects(self, cell):
		bounds = cell.bounds

		for i, constant in enumerate(self.constantAxis):
			if( constant ):
				if( not (bounds[0][i] <= self.origin[i] <= bounds[1][i]) ):
					return False

		if( self.constantAxis[0] ):
			txmin = -np.inf
			txmax = +np.inf
		else:
			txmin = (bounds[self.sign[0]][0] - self.origin[0]) * self.invDirection[0]
			txmax = (bounds[1-self.sign[0]][0] - self.origin[0]) * self.invDirection[0]

		if( self.constantAxis[1] ):
			tymin = -np.inf
			tymax = +np.inf
		else:
			tymin = (bounds[self.sign[1]][1] - self.origin[1]) * self.invDirection[1]
			tymax = (bounds[1-self.sign[1]][1] - self.origin[1]) * self.invDirection[1]

		if( (tymax <= txmin ) or (txmax <= tymin) ):
			return False

		if( self.constantAxis[1] ):
			pa = (self.origin[0] + self.direction[0]*txmin, self.origin[1] )
			pb = (self.origin[0] + self.direction[0]*txmax, self.origin[1] )
			self.points[cell] = [pa, pb]
		
		elif( self.constantAxis[0] ):
			pa = (self.origin[0] + self.direction[0], self.origin[1] + self.direction[1]*tymin)
			pb = (self.origin[0] + self.direction[0], self.origin[1] + self.direction[1]*tymax)
			self.points[cell] = [pa, pb]
		else:

			if( tymin < txmin ):
				pax = bounds[self.sign[0]][0]
				pay = self.origin[1] + self.direction[1]*txmin
			
			else:
				pax = self.origin[0] + self.direction[0]*tymin
				pay = bounds[self.sign[1]][1]
			
			if( txmax < tymax ):
				pbx = bounds[1-self.sign[0]][0]
				pby = self.origin[1] + self.direction[1]*txmax
			
			else:
				pbx = self.origin[0] + self.direction[0]*tymax
				pby = bounds[1-self.sign[1]][1]
			
			pa = (pax, pay)
			pb = (pbx, pby)

			self.points[cell] = [pa, pb]
		return True
	
	# def getIntersection(self, cell):
		