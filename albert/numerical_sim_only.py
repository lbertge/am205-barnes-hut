import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.animation as animation
from naive import Body as naive_body, step as naive_step
import argparse
from leapfrog import Body, step as leapfrog_step

G = 1

def parse_body(body_data): 
    return Body(*body_data.split(' '))

def parse_naive_body(body_data): 
    return naive_body(*body_data.split(' '))

def getImage(fname):
    return OffsetImage(plt.imread(fname))

def save_energy(outfile, bodies, positions, velocities):
    energies = []
    # step_positions: x1, y1, x2, y2, x3, y3, ...
    # step_velocities: vx1, vy1, vx2, vy2, vx3, vy3, ...
    for k, step_positions in enumerate(positions):
        pe = 0
        ke = 0
        step_velocities = velocities[k]
        for i in range(len(bodies)):
            for j in range(len(bodies)):
                if i != j:
                    distance = (step_positions[2*i] - step_positions[2*j]) ** 2 + \
                            (step_positions[2*i+1] - step_positions[2*j+1]) ** 2

                    pe += bodies[i].m * bodies[j].m / np.sqrt(distance)
            
            v2 = step_velocities[2*i] ** 2 + step_velocities[2*i+1] ** 2
            ke += bodies[i].m * v2

        # print(ke, pe)
        energy = 0.5 * ke - 0.5 * G * pe 

        energies.append(energy)
    np.savetxt(f"{outfile}_energy", energies)


def simulate_leapfrog_data_only(infile, outfile, dt, iterations):
    bodies = []
    with open(infile, 'r') as f:
        n = int(f.readline())
        r = float(f.readline())
        # print(n, r)
        for i in range(n):
            bodies.append(parse_body(f.readline()))

    positions = []
    velocities = []
    for i in range(iterations):
        x, y, vx, vy = leapfrog_step(bodies, dt)
        step_positions = []
        step_velocities = []
        for j in range(len(x)):
            step_positions.append(x[j])
            step_positions.append(y[j])
            step_velocities.append(vx[j])
            step_velocities.append(vy[j])
            
        positions.append(step_positions)
        velocities.append(step_velocities)

    np.savetxt(outfile, positions)

    save_energy(outfile, bodies, positions, velocities)

def simulate_naive_data_only(infile, outfile, dt, iterations):
    bodies = []
    with open(infile, 'r') as f:
        n = int(f.readline())
        r = float(f.readline())
        # print(n, r)
        for i in range(n):
            bodies.append(parse_naive_body(f.readline()))

    positions = []
    velocities = []
    for i in range(iterations):
        x, y, vx, vy = naive_step(bodies, dt)
        step_positions = []
        step_velocities = []
        for j in range(len(x)):
            step_positions.append(x[j])
            step_positions.append(y[j])
            step_velocities.append(vx[j])
            step_velocities.append(vy[j])
            
        positions.append(step_positions)
        velocities.append(step_velocities)

    np.savetxt(outfile, positions)

    save_energy(outfile, bodies, positions, velocities)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run simulation for different algorithms')
    parser.add_argument('datafile', type=str, help='file containing initial planetary conditions')
    parser.add_argument('--alg', dest='algorithm', required=True, type=str, choices=['naive', 'leapfrog'])
    parser.add_argument('--out', dest='outfile', type=str, help='output of movie')
    parser.add_argument('--dt', dest='timestep', type=float, default=25000, help='time stepsize')
    parser.add_argument('--it', dest='iterations', type=int, default=500, help='number of timesteps')
    args = parser.parse_args()
    print(args.algorithm)
    if args.algorithm == 'naive':
        simulate_naive_data_only(args.datafile, args.outfile, args.timestep, args.iterations)
    else:
        simulate_leapfrog_data_only(args.datafile, args.outfile, args.timestep, args.iterations)



