import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.animation as animation
from nbody import step as naive_step
import argparse
from leapfrog import Body, step as leapfrog_step

def parse_body(body_data): 
    return Body(*body_data.split(' '))

def getImage(fname):
    return OffsetImage(plt.imread(fname))

def simulate_leapfrog():
    bodies = []
    with open('planets.txt', 'r') as f:
        n = int(f.readline())
        r = float(f.readline())
        # print(n, r)
        for i in range(n):
            bodies.append(parse_body(f.readline()))

    fig, ax = plt.subplots()
    ims = []
    artists = []
    for body in bodies:
        img = getImage(body.fname)
        ab = AnnotationBbox(img, (body.x, body.y), frameon=False)
        ax.add_artist(ab)
        artists.append(ab)
    ims.append(artists)

    dt = 25000

    for i in range(500):
        x, y = leapfrog_step(bodies, dt)
        
        artists = []
        for j, body in enumerate(bodies):
            img = getImage(body.fname)
            ab = AnnotationBbox(img, (x[j], y[j]), frameon=False)
            ax.add_artist(ab)
            artists.append(ab)
        ims.append(artists)

    plt.xlim([-r, r])
    plt.ylim([-r, r])
    ani = animation.ArtistAnimation(fig, ims, interval=10, blit=True,
            repeat_delay=10000)

    ani.save("movie_leapfrog.mp4")

    plt.show()

def simulate_naive():
    bodies = []
    with open('planets.txt', 'r') as f:
        n = int(f.readline())
        r = float(f.readline())
        # print(n, r)
        for i in range(n):
            bodies.append(parse_body(f.readline()))

    fig, ax = plt.subplots()

    ims = []
    # starting positions
    for body in bodies:
        plt.scatter(body.x, body.y)

    artists = []
    for body in bodies:
        img = getImage(body.fname)
        ab = AnnotationBbox(img, (body.x, body.y), frameon=False)
        ax.add_artist(ab)
        artists.append(ab)
    ims.append(artists)

    x = []
    v = []
    m = []
    dt = 1
    d = 2
    for body in bodies:
        x.append([body.x, body.y])
        v.append([body.vx, body.vy])
        m.append(body.m)

    x = np.array(x)
    v = np.array(v)
    m = np.array(m)

    for i in range(100):
        x, v = naive_step(x, v, m, dt, d)
        
        artists = []
        for j, body in enumerate(bodies):
            img = getImage(body.fname)
            ab = AnnotationBbox(img, (x[j][0], x[j][1]), frameon=False)
            ax.add_artist(ab)
            artists.append(ab)
        ims.append(artists)

        print(f"step {i}:")
        print(x)
        print(v)

    print(len(ims))
   
    plt.xlim([-r, r])
    plt.ylim([-r, r])
    # plt.legend()
    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
            repeat_delay=10000)

    ani.save("movie.mp4")

    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run simulation for different algorithms')
    parser.add_argument('--alg', dest='algorithm', required=True, type=str, choices=['naive', 'leapfrog'])
    args = parser.parse_args()
    print(args.algorithm)
    if args.algorithm == 'naive':
        simulate_naive()
    else:
        simulate_leapfrog()

