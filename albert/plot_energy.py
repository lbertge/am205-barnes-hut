import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.animation as animation
from nbody import step as naive_step
import argparse
from leapfrog import Body, step as leapfrog_step
from matplotlib.pyplot import cm

def plot_energies(infile, dt):

    energies = np.loadtxt(infile)
    t = np.arange(0, len(energies)) * dt

    plt.plot(t, energies)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run simulation for different algorithms')
    parser.add_argument('datafile', type=str, help='file containing initial planetary conditions')
    parser.add_argument('--dt', dest='timestep', type=float, default=25000, help='time stepsize')
    args = parser.parse_args()
    plot_energies(args.datafile, args.timestep)

