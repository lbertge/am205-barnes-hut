import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
import argparse

obj1 = {
    "m": 1,
    "p": (-5,0),
    "v": (0,-0.22)
}
obj2 = {
    "m": 1,
    "p": (5,0),
    "v": (0,0.22)
}
init = [obj1,obj2]

G = 1
n = len(init)
def x_accel(s,i,j):
    m2 = init[j]['m']
    x1 = s[i]
    y1 = s[i+n]
    x2 = s[j]
    y2 = s[j+n]
    return m2*(x2-x1)/((x2-x1)**2 + (y2-y1)**2)**(3/2)

def y_accel(s,i,j):
    m2 = init[j]['m']
    x1 = s[i]
    y1 = s[i+n]
    x2 = s[j]
    y2 = s[j+n]
    return m2*(y2-y1)/((x2-x1)**2 + (y2-y1)**2)**(3/2)

def xpp(s,i):
    other_indices = list(range(n))
    other_indices.remove(i)
    return G*sum([x_accel(s,i,j) for j in other_indices])

def ypp(s,i):
    other_indices = list(range(n))
    other_indices.remove(i)
    return G*sum([y_accel(s,i,j) for j in other_indices])

def F(s,t):
    return np.concatenate(
        (s[2*n:3*n],s[3*n:4*n],
         [xpp(s,i) for i in range(n)],
         [ypp(s,i) for i in range(n)]))

def solve(outfile, dt):
    x0 = [o['p'][0] for o in init]
    y0 = [o['p'][1] for o in init]
    vx0 = [o['v'][0] for o in init]
    vy0 = [o['v'][1] for o in init]
    s0 = np.concatenate((x0,y0,vx0,vy0))

    t = np.arange(0, 500, 1) * 0.5
    solution = odeint(F,s0,t)

    positions = []
    for i in range(len(t)):
        step_positions = []
        for j in range(n):
            x = solution[i,j]
            y = solution[i,n+j]
            step_positions.append(x)
            step_positions.append(y)
        positions.append(step_positions)

    np.savetxt(outfile, positions)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run simulation for different algorithms')
    parser.add_argument('--out', dest='outfile', required=True, type=str, help='output of movie')
    parser.add_argument('--dt', dest='timestep', required=True, type=float, default=25000, help='time stepsize')
    args = parser.parse_args()
    solve(args.outfile, args.timestep)
