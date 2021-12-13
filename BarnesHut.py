import numpy as np
import matplotlib.pyplot as plt

G = 6.67408e-11 
G = 0.04
dt = 1e8
dt = 1e-3

class Rect:
	def __init__(self, left, top, right, bottom):

		assert right > left
		assert top < bottom
		self.left = left
		self.top = top
		self.right = right
		self.bottom = bottom

		self.width = self.right - self.left
		self.cx = (self.right + self.left) / 2.0
		self.cy = (self.bottom + self.top) / 2.0

	def topLeft(self):
		return Rect(self.left, self.top, self.cx, self.cy)

	def topRight(self):
		return Rect(self.cx, self.top, self.right, self.cy)

	def bottomLeft(self):
		return Rect(self.left, self.cy, self.cx, self.bottom)

	def bottomRight(self):
		return Rect(self.cx, self.cy, self.right, self.bottom)




class Body:
	def __init__(self, mass, px, py, vx = 0, vy = 0):
		self.m = mass
		self.px = px
		self.py = py

		#force acting on body from all other bodies
		self.fx = 0
		self.fy = 0

		self.vx = 0
		self.vy = 0

	def __str__(self):
		return f"m={self.m:.2f} x={self.px:.2f} y={self.py:.2f}"

	def inRect(self, rect):
		return self.px >= rect.left and self.px < rect.right and self.py >= rect.top and self.py < rect.bottom  		

	def add(self, body):

		m = self.m + body.m
		x = (self.px * self.m + body.px * self.m) / (m)
		y = (self.py * self.m + body.py * self.m) / (m)
		
		return Body(m,x,y)

	def distanceTo(self, body):
		return ((self.px - body.px)** 2 + (self.py - body.py) **2) ** 0.5

	def resetForce(self):
		self.fx = 0
		self.fy = 0


	def calculateForce(self, body):

		#TODO Placeholder (fix this)
		f = G * self.m * body.m / self.distanceTo(body)
		return f * (self.px - body.px), f* (self.py - body.py)


class BHTree:

	theta = 0.5
	def __init__(self, rect):

		self.rect = rect
		self.body = None
		self.topLeft = None
		self.topRight = None
		self.bottomLeft = None
		self.bottomRight = None

	@property
	def isInternal(self):
		return self.topLeft or self.topRight or self.bottomLeft or self.bottomRight

	def findQuad(self,body):
		if(body.inRect(self.rect.topLeft())):
			return self.topLeft
		if(body.inRect(self.rect.topRight())):
			return self.topRight
		if(body.inRect(self.rect.bottomLeft())):
			return self.bottomLeft
		if(body.inRect(self.rect.bottomRight())):
			return self.bottomRight


	def insert(self, body):

		#insert if body empty
		if self.body is None:
			self.body = body
		elif(self.isInternal):
			# add to some subtree
			merged = self.body.add(body) 
			self.body = merged
			self.place(body)
		else:
			#create subtrees and place current and new body into them 
			self.topLeft = BHTree(self.rect.topLeft())
			self.topRight = BHTree(self.rect.topRight())
			self.bottomLeft = BHTree(self.rect.bottomLeft())
			self.bottomRight = BHTree(self.rect.bottomRight())

			self.place(body)
			self.place(self.body)
			self.body = self.body.add(body)



	def place(self,body):
		if(body.inRect(self.rect.topLeft())):
			self.topLeft.insert(body)
		elif(body.inRect(self.rect.topRight())):
			self.topRight.insert(body)
		elif(body.inRect(self.rect.bottomLeft())):
			self.bottomLeft.insert(body)
		elif(body.inRect(self.rect.bottomRight())):
			self.bottomRight.insert(body)

	def updateForce(self, body):

		body.resetForce()

		def _updateForce(root, body):
			if root is None or body is root:
				return 0

			if(root.body is None or root.body.distanceTo(body) / root.rect.width > BHTree.theta):
				_updateForce(root.topLeft, body)
				_updateForce(root.topRight, body)
				_updateForce(root.bottomLeft, body)
				_updateForce(root.bottomRight, body)
			else:
				fx, fy = root.body.calculateForce(body)

				body.fx +=fx
				body.fy +=fy


		_updateForce(self, body)
		#print(body.fx, body.fy)


	def __str__(self):

		if(self.body is None):
			return "[]"
		res = f"b[{self.body}]"

		if(self.topLeft):
			res += f" tl={self.topLeft}"

		if(self.topRight):
			res += f" tr={self.topRight}"

		if(self.bottomLeft):
			res += f" bl={self.bottomLeft}"
			
		if(self.bottomRight):
			res += f" br={self.bottomRight}"
			

		return res


def step(bodies):

	tree = BHTree(Rect(0, 0, 1, 1))
	for body in bodies:
		tree.insert(body)

	for body in bodies:
		tree.updateForce(body)

	for body in bodies:
		body.vx += body.fx/ body.m * dt
		body.vy += body.fy/ body.m * dt

		body.px += body.vx * dt
		body.py += body.vy * dt 




def createBodies(n):
	bodies = []

	# m  = np.random.rand(n) * 1e12
	# x0 = np.random.rand(n, d) * 1e13
	# v0 = np.random.rand(n, d) * 1

	for i in range(n):
		x0 = np.random.uniform(0, 1, 4)
		bodies.append(Body(1, x0[0],x0[1], x0[2], x0[3]))

	return bodies


def main():
	n = 3
	itters = 20000
	bodies = createBodies(n)
	
	result = np.zeros((itters,n,2))
	for i in range(itters):
		for j, body in enumerate(bodies):
			result[i, j, :] = [body.px, body.py]
			step(bodies)
	for i in range(n):
		plt.scatter(result[:, i, 0], result[:, i, 1])

	print(result)

	plt.show()


def testTree():

	tree = BHTree(Rect(0,0, 1, 1))
	assert BHTree.isInternal 
	tree.insert(Body(1,0,0))
	assert BHTree.isInternal 
	tree.insert(Body(2,0.0,0.10))
	assert tree.topLeft.body.m == 3


if __name__ == '__main__':

	# testTree()

	main()

