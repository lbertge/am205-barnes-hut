import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime

G = 6.67408e-11 




def step(x,v,m,dt, d=3):
	for i in range(len(x)):
		dv = np.zeros(d)
		for j in range(len(x)):
			if i != j:
				dv += -G * m[j] * (x[i] - x[j]) / (np.linalg.norm(x[i] - x[j]) ** 2) 
		x[i] += v[i] * dt
		v[i] += dv * dt




	return x,v

def writeOutput(result):
	today = datetime.now()
	dateString = today.strftime("%Y-%m-%d-%H-%M")
	print(result.shape)
	result = result.reshape((result.shape[0], result.shape[1] * result.shape[2]))
	np.savetxt(f'output/result-{dateString}.csv', result, delimiter=',')

def main():
	n = 2
	dt = 1e6
	d = 2

	m  = np.random.rand(n) * 1e12
	x0 = np.random.rand(n, d) * 1e13
	# v0 = np.random.rand(n, d) * 1

	x0 = np.array([[1e5, 1e5], [0, 0]], dtype = np.float64)
	v0 = np.zeros((n,d))
	x = x0
	v = v0
	result = [x]
	T = [0]
	t = 0

	for i in range(100000):
		x, v = step(x, v,m, dt, d)
		t += dt
		result.append(x.copy())
		T.append(t)
		if i % 10000 == 0:
			print(i / 100000.0)
	result = np.array(result)
	fig = plt.figure()
	plt.scatter(result[:, 0, 0], result[:, 0, 1])
	plt.scatter(result[:, 1, 0], result[:, 1, 1])
	# ax = fig.add_subplot(projection='3d')

	# ax.scatter(result[10000:,0, 0], result[10000:,0, 1], result[10000:,0, 2])
	# ax.scatter(result[10000:,1, 0], result[10000:,1, 1], result[10000:,0, 2])
	# ax.scatter(result[10000:,2, 0], result[10000:,2, 1], result[10000:,0, 2])

	# print(min(result[:,0, 2])/ 1e11, max(result[:,0, 2])/ 1e11)
	writeOutput(result)
	# plt.scatter(result[:,2, 0], result[:,2, 1])

	plt.show()



if __name__ == '__main__':
	main()