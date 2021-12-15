import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.animation as animation
from nbody import step as naive_step
import argparse
from leapfrog import Body, step as leapfrog_step
from matplotlib.pyplot import cm


def anim_only(infiles, outfile, r):
    fig, ax = plt.subplots()
    ims = []
    position_trajs = []
    for f in infiles: 
        position_trajs.append(np.loadtxt(f))
    
    movie_len = len(position_trajs[0])
    n = len(position_trajs)
    # color = np.array([cm.rainbow(np.linspace(0, 1, n))])
    color = cm.rainbow(np.linspace(0, 1, n))
    print(n)
    print(color.shape)

    for i in range(movie_len):
        artists = []
        for posIdx, positions in enumerate(position_trajs):
            positions_x = []
            positions_y = []
            for j in range(0, len(positions[i]), 2):
                positions_x.append(positions[i][j])
                positions_y.append(positions[i][j+1])

            if i == 1:
                artist = ax.scatter(positions_x, positions_y, color=color[posIdx], label=infiles[posIdx])
            else:
                artist = ax.scatter(positions_x, positions_y, color=color[posIdx])
            artists.append(artist)
        ims.append(artists)
    print(len(ims))
             
    plt.xlim([-r, r])
    plt.ylim([-r, r])
    ax.legend(loc='upper right')
    ani = animation.ArtistAnimation(fig, ims, interval=10, blit=True,
            repeat_delay=10000)

    ani.save(f"{outfile}.mp4")
    # plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run simulation for different algorithms')
    # parser.add_argument('datafile', type=str, help='file containing initial planetary conditions')
    parser.add_argument('-n', '--names-list', nargs='+', default=[])
    parser.add_argument('--out', dest='outfile', type=str, help='output of movie')
    parser.add_argument('--r', dest='r', type=float, default=5, help='canvas size')

    args = parser.parse_args()
    anim_only(args.names_list, args.outfile, args.r)
