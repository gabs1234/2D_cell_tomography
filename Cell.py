import numpy as np

class Cell(object):
	def __init__(self, xmin, xmax, ymin, ymax, id):
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax
		self.id = id

		self.bounds = ((self.xmin, self.ymin), (self.xmax, self.ymax))
	

	def disp(self):
		# (xmin xmax) (ymin ymax)
		print("{}: ".format(self.id), (self.xmin, self.xmax), (self.ymin, self.ymax))