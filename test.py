import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime

G = 6.67e-11

epsilon = 0##1e0


def step(x,v,m,dt, d=3):
	for i in range(len(x)):
		dv = np.zeros(d)
		for j in range(len(x)):
			if i != j:
				if(np.linalg.norm(x[i]- x[j]) < 1e-4):
					print("SMALL")
				dv += -G * m[j] * (x[i] - x[j]) / ((np.linalg.norm(x[i] - x[j]) + epsilon) ** 3) 
		v[i] += dv * dt
		x[i] += v[i] * dt






	return x,v

def writeOutput(result):
	today = datetime.now()
	dateString = today.strftime("%Y-%m-%d-%H-%M")
	print(result.shape)
	result = result.reshape((result.shape[0], result.shape[1] * result.shape[2]))
	np.savetxt(f'output/result-{dateString}.csv', result, delimiter=',')

def main():
	n = 6
	dt = 1e2
	d = 3

	m  = np.ones(n) * 10

	m = np.array([1.9891e30, 3.285e23, 4.867e24, 5.972e24, 7.34767e22 , 6.39e23])
	x= np.array([[0,0,0], [41.5e6,0,0], [67e6,0,0], [91e6,0,0], [91e6 +238900,0,0], [145e6,0,0]]) * 1609.34
	v = np.array([[0,0,0], [0, 47.36,0], [0, 35.26,0], [0, 30,0],[0, 30 + 0.97, 0], [0, 24,0]]) * 1000
	# # m[0] = 1e3
	# x0 = np.random.rand(n, d) * 1e4

	# # x0 = np.asarray([[ 4.63772946,  5.16567956],
	# #  [63.6040603,  70.1627337 ],
	# #  [ 2.81171087, 27.34820463],
	# #  [62.83904221,  6.26262792],
	# #  [ 3.05373204, 66.76371405],
	# #  [61.77563378, 29.89072936],
	# #  [12.216713,   68.92160222],
	# #  [92.62424607, 37.9619841 ],
	# #  [43.60678416, 46.57771535],
	# #  [88.53211592, 87.47930081]])

	# # x0 = x0[:4]
	# v0 = np.random.rand(n, d) * 1000
	# # v0[0,:] = [0,0]
	# # v0[0,:] = [1000,1000]
	# print(x0)
	# # print(v0)

	# # x0 = np.array([[1e5, 1e5], [0, 0]], dtype = np.float64)
	# # v0 = np.zeros((n,d))
	# x = x0
	# v = v0
	result = [x]
	T = [0]
	t = 0

	for i in range(1000000):
		x, v = step(x, v, m, dt, d)
		t += dt
		result.append(x.copy())
		T.append(t)
		if i % 10000 == 0:
			print(i / 100000.0)
	result = np.array(result)
	fig = plt.figure()
	plt.scatter(result[:, 0, 0], result[:, 0, 1])
	plt.scatter(result[:, 1, 0], result[:, 1, 1])
	plt.scatter(result[:, 2, 0], result[:, 2, 1])
	plt.scatter(result[:, 3, 0], result[:, 3, 1])
	plt.scatter(result[:, 4, 0], result[:, 4, 1])
	plt.scatter(result[:, 5, 0], result[:, 5, 1])
	#plt.scatter(result[:, 4, 0], result[:, 4, 1])
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