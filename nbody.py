import numpy as np
import matplotlib.pyplot as plt
from random import sample
from time import time
G = 6.67408e-11 




def step(x,v,m,dt, d=3):
    for i in range(len(x)):
        dv = np.zeros(d)
        for j in range(len(x)):
            if i != j:
                dv += -G * m[j] * (x[i] - x[j]) / (np.linalg.norm(x[i] - x[j]) ** 3) 
        x[i] += v[i] * dt
        v[i] += dv * dt


    return x,v


def runNBody(itters, n, d=2):
    dt = 1e8
    d = 3

    m  = np.random.rand(n) * 1e12
    x0 = np.random.rand(n, d) * 1e13
    v0 = np.random.rand(n, d) * 1
    # v0 = np.zeros((n,d))
    x = x0
    v = v0

    for i in range(itters):
        x, v = step(x, v,m, dt, d = d)

def timeit(params=((10, 2), (10, 3), (10, 5), (10, 10), (10, 20), (10, 50), (10, 75), (10, 100)), n_average=5):
    elapsed = []
    for itters, n in params:
        timeaccum = 0
        for k in range(n_average):
            start = time()
            merged = runNBody(itters, n)
            end   = time()
            timeaccum += end-start
            print("finished ", k , itters, n)
        elapsed.append(timeaccum / n_average)

    return elapsed

plt.rcParams.update({'font.size': 24})
def main():



    results = timeit()
    x2 = [2,3,5,10,20,50, 75,100]
   

    Y = np.log(results)
    X = np.asarray([(np.log(item), 1) for item in x2])

    b, a = np.linalg.lstsq(X, Y, rcond = None)[0]
    fn = lambda n : np.exp(a) * n ** b
    x = np.linspace(0, 100, 100)
    plt.plot(x, fn(x), label = f"{np.exp(a):.5f}n^{b:.2f}")
    plt.scatter(x2, results, label = "Nieve Run Time")
    plt.title("N-body Scaling with N (10 itterations)")
    plt.xlabel("Bodies")
    plt.ylabel("Run Time (s)")
    plt.legend()
    plt.show()
    # n = 2
    # dt = 1e8
    # d = 3

    # m  = np.random.rand(n) * 1e12
    # x0 = np.random.rand(n, d) * 1e13
    # v0 = np.random.rand(n, d) * 1
    # # v0 = np.zeros((n,d))
    # x = x0
    # v = v0
    # result = [x]
    # T = [0]
    # t = 0

    # for i in range(1000000):
    #   x, v = step(x, v,m, dt, d = d)
    #   t += dt
    #   result.append(x.copy())
    #   T.append(t)
    # result = np.array(result)

    # plt.scatter(result[:,0, 0], result[:,0, 1])
    # plt.scatter(result[:,1, 0], result[:,1, 1])
    # # plt.scatter(result[:,2, 0], result[:,2, 1])

    # plt.show()



if __name__ == '__main__':
    main()