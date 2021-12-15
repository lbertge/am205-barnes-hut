import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.animation as animation
from naive import Body as naive_body, step as naive_step
import argparse
from leapfrog import Body, step as leapfrog_step

def parse_body(body_data): 
    return Body(*body_data.split(' '))

def parse_naive_body(body_data): 
    return naive_body(*body_data.split(' '))

def getImage(fname):
    return OffsetImage(plt.imread(fname))

def simulate_leapfrog_data_only(infile, outfile, dt):
    bodies = []
    with open(infile, 'r') as f:
        n = int(f.readline())
        r = float(f.readline())
        # print(n, r)
        for i in range(n):
            bodies.append(parse_body(f.readline()))

    positions = []
    for i in range(500):
        x, y = leapfrog_step(bodies, dt)
        step_positions = []
        for j in range(len(x)):
            step_positions.append(x[j])
            step_positions.append(y[j])
        positions.append(step_positions)

    np.savetxt(outfile, positions)

def simulate_naive_data_only(infile, outfile, dt):
    bodies = []
    with open(infile, 'r') as f:
        n = int(f.readline())
        r = float(f.readline())
        # print(n, r)
        for i in range(n):
            bodies.append(parse_naive_body(f.readline()))

    positions = []
    for i in range(500):
        x, y = naive_step(bodies, dt)
        step_positions = []
        for j in range(len(x)):
            step_positions.append(x[j])
            step_positions.append(y[j])
        positions.append(step_positions)

    np.savetxt(outfile, positions)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run simulation for different algorithms')
    parser.add_argument('datafile', type=str, help='file containing initial planetary conditions')
    parser.add_argument('--alg', dest='algorithm', required=True, type=str, choices=['naive', 'leapfrog'])
    parser.add_argument('--out', dest='outfile', type=str, help='output of movie')
    parser.add_argument('--dt', dest='timestep', type=float, default=25000, help='time stepsize')
    args = parser.parse_args()
    print(args.algorithm)
    if args.algorithm == 'naive':
        simulate_naive_data_only(args.datafile, args.outfile, args.timestep)
    else:
        simulate_leapfrog_data_only(args.datafile, args.outfile, args.timestep)



