from Cell import Cell
import numpy as np

class Ray(object):
	points = {}

	def __init__(self, origin, dir):
		self.origin = np.array(origin)
		self.direction = np.array(dir)
		
		# Avoid printing error when infinity encoutered
		with np.errstate(divide='ignore'):
			self.invDirection = np.divide(1.0, self.direction)
		
		self.sign = np.array([inv < 0 for inv in self.invDirection])
		print(self.sign)

		# Signal along which axis the line is constant
		self.constantAxis = (self.direction == 0)

		print("constant axis: ", self.constantAxis)

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
			print("geo")
			self.points[cell] = [pa, pb]
		
		elif( self.constantAxis[0] ):
			pa = (self.origin[0] + self.direction[0], self.origin[1] + self.direction[1]*tymin)
			pb = (self.origin[0] + self.direction[0], self.origin[1] + self.direction[1]*tymax)
			print("heo")
			self.points[cell] = [pa, pb]
		else:
			print(self.origin)
			print(self.direction)
			print("txmin:", txmin)
			print("txmax:", txmax)
			print("tymin:", tymin)
			print("tymax:", tymax)

			if( tymin < txmin ):
				print("xmin big a")
				pax = bounds[0][0]
				pay = self.origin[1] + self.direction[1]*txmin
			
			else:
				print("tymin big a")
				pax = self.origin[0] + self.direction[0]*tymin
				pay = bounds[0][1]
			
			if( txmax < tymax ):
				print("tymax big b")
				pbx = bounds[1][0]
				pby = self.origin[1] + self.direction[1]*txmax
			
			else:
				pbx = self.origin[0] + self.direction[0]*tymax
				print("txmax big b")
				pby = bounds[1][1]
			
		pa = (pax, pay)
		pb = (pbx, pby)

		self.points[cell] = [pa, pb]
		return True
	
	# def getIntersection(self, cell):
		