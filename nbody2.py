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
				dv += -G * m[j] * (x[i] - x[j]) / (np.linalg.norm(x[i] - x[j]) ** d) 
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
	n = 10
	dt = 1e9
	d = 2

	m  = np.random.rand(n) * 1e12
	x0 = np.random.rand(n, d) * 1e13
	v0 = np.random.rand(n, d) * 1
	# v0 = np.zeros((n,d))
	x = x0
	v = v0
	result = [x]
	T = [0]
	t = 0

	for i in range(1000000):
		x, v = step(x, v,m, dt, d = d)
		t += dt
		result.append(x.copy())
		T.append(t)
	result = np.array(result)

	plt.scatter(result[:,0, 0], result[:,0, 1])
	plt.scatter(result[:,1, 0], result[:,1, 1])

	writeOutput(result)
	# plt.scatter(result[:,2, 0], result[:,2, 1])

	plt.show()



if __name__ == '__main__':
	main()