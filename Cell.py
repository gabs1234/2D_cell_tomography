import numpy as np

class Cell(object):
	def __init__(self, xmin, xmax, ymin, ymax, id):
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax
		self.id = id

		self.bounds = np.array(((self.xmin, self.ymin), (self.xmax, self.ymax)))
	

	def disp(self):
		print("{}: ".format(self.id), self.bounds)