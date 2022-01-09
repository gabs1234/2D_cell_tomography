class Ray(object):
	def __init__(self, origin, dir):
		self.origin = np.array(origin)
		self.direction = np.array(dir)