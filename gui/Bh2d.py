import numpy as np
import math
import matplotlib.pyplot as plt
from datetime import datetime
import sys
sys.setrecursionlimit(2000)

G = 0.04
theta = 0.5
dt = 1e-3
num_bodies = 2500
epsilon = 0.1
L = 1

def distance(bod1, bod2):
    x1, y1 = bod1.px, bod1.py
    x2, y2 = bod2.px, bod2.py
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def force(bod1, bod2):
    x1, y1, m1 = bod1.px, bod1.py, bod1.mass
    x2, y2, m2 = bod2.px, bod2.py, bod2.mass
    return G*m1*m2/(distance(bod1,bod2)**2 + epsilon)

def x_component(bod1, bod2):
    return (bod1.px-bod2.px)/(distance(bod1, bod2) + epsilon)

def y_component(bod1, bod2):
    return (bod1.py-bod2.py)/(distance(bod1, bod2) + epsilon)

class Body:
    def __init__(self, mass, px, py, vx, vy):
        self.mass = mass
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.fx = 0
        self.fy = 0
    
    def zero_forces(self, by_root = False):
        if by_root:
            self.fx = 0
            self.fy = 0

class Node:
    def __init__(self, xleft, xright, ybot, ytop):
        # Initialize an empty node, meaning a region in space but no bodies in it and no children
        
        # Define the children and domain
        self.topleft, self.topright, self.botleft, self.botright = None, None, None, None
        self.xleft, self.xright, self.ybot, self.ytop = xleft, xright, ybot, ytop
        self.centerx = (xleft+xright)/2
        self.centery = (ybot+ytop)/2
        
        # Define the Center of Mass and total Mass
        self.CoMx, self.CoMy, self.totM = None, None, 0
        
        # Define
        self.body = None
        
    def which_child(self, x, y):
        assert x< self.xright and x > self.xleft and y < self.ytop and y > self.ybot, "Must be in Rect"
        if x >= self.centerx and y >= self.centery:
            return self.topright
        elif x >= self.centerx and y < self.centery:
            return self.botright
        elif x < self.centerx and y >= self.centery:
            return self.topleft
        elif x < self.centerx and y < self.centery:
            return self.botleft
        else:
            return None

        
    def add_body(self, new_body):
        # if this node contains no bodies (is a leaf with no bodies)
        if self.body == None and self.topleft == None and self.topright == None and self.botleft == None and self.botright == None:
            self.body = new_body
            self.CoMx = new_body.px
            self.CoMy = new_body.py
            self.totM += new_body.mass

            
        # if this node is internal (non leaf)
        elif self.body == None:
            self.CoMx = (self.totM*self.CoMx + new_body.mass*new_body.px)/(self.totM + new_body.mass)
            self.CoMy = (self.totM*self.CoMy + new_body.mass*new_body.py)/(self.totM + new_body.mass)
            self.totM += new_body.mass
            
            childNode = self.which_child(new_body.px, new_body.py)
            childNode.add_body(new_body)

            
        # if this node is external (leaf that is 1 body)
        else:
            self.topleft = Node(self.xleft, self.centerx, self.centery, self.ytop)
            self.topright = Node(self.centerx, self.xright, self.centery, self.ytop)
            self.botleft = Node(self.xleft, self.centerx, self.ybot, self.centery)
            self.botright = Node(self.centerx, self.xright, self.ybot, self.centery)
            
            childNode = self.which_child(self.body.px, self.body.py)
            childNode.add_body(self.body)
            
            childNode = self.which_child(new_body.px, new_body.py)
            childNode.add_body(new_body)
            
            self.CoMx = (self.totM*self.CoMx + new_body.mass*new_body.px)/(self.totM + new_body.mass)
            self.CoMy = (self.totM*self.CoMy + new_body.mass*new_body.py)/(self.totM + new_body.mass)
            self.totM += new_body.mass
            self.body = None

            
    def calculate_force(self, body, by_root = False):
        body.zero_forces(by_root)
        
        # if this node is itself:
        if self.body == body:
            return
        
        # if this node is an empty node
        if self.body == None and self.topleft == None and self.topright == None and self.botleft == None and self.botright == None:
            return
        
        # if this node is a body (external node):
        elif self.body != None:
            f = force(body, self.body)
            body.fx += f*x_component(body, self.body)
            body.fy += f*y_component(body, self.body)
        
        # if this node is an internal node
        else:
            s = self.xleft-self.xright
            d = ((self.CoMx - body.px)**2+(self.CoMy - body.py)**2)**0.5 + epsilon
            
            # if aggregate condition is met, aggregate
            if s/d < theta:
                f = G*self.totM*body.mass/d**2
                body.fx += f*(self.CoMx - body.px)/d
                body.fy += f*(self.CoMy - body.py)/d
                
            # if aggregate condition not met, recurse
            else:
                self.topleft.calculate_force(body)
                self.topright.calculate_force(body)
                self.botleft.calculate_force(body)
                self.botright.calculate_force(body)
                    
                
            
                
                    
def step(bodies):
    for body in bodies:
        body.px += body.vx*dt
        body.py += body.vy*dt
        body.vx += body.fx/body.mass*dt
        body.vy += body.fy/body.mass*dt

        # if(body.px > L):
        #     body.px = 2 * L - body.px
        #     body.vx *=-1
        #     del body

        # if(body.px < -L):
        #     body.px =  -body.px

        #     body.vx *=-1
        #     del body
        # if(body.py > L):
        #     body.py = 2 * L - body.py
        #     body.vy *=-1
        #     del body
        # if(body.py < -L):
        #     body.py = -body.py
        #     body.vy *=-1
        #     del body

def main(num_iters, num_bodies):
   # num_iters = 1000
    pos_hist = []
    
    bodies = []
    for i in range(num_bodies):
        j = np.random.rand(5)
        R = np.random.uniform(0, L/4.0);
        theta = np.random.uniform(0, 2*np.pi);
        x =  R*np.cos(theta);
        y =  0.25*R*np.sin(theta);
        R_prim = np.sqrt((x - L/2) ** 2 + (y - L/2) ** 2);
        u = -5*R_prim*np.sin(theta);
        v = 5*R_prim*np.cos(theta);
        bodies.append(Body(1,x,y, u, v))

    root = Node(-L,L,-L,L)
    this_pos = []
    for body in bodies:
        this_pos.append([body.px, body.py])
        root.add_body(body)
    pos_hist.append(this_pos)
    
    for i in range(num_iters):
        
        for body in bodies:
            root.calculate_force(body, True)
        step(bodies)
        
        this_pos = []
        for body in bodies:
            this_pos.append([body.px, body.py])
        pos_hist.append(this_pos)
        print(i)
        try:
            root = Node(-L,L,-L,L)
            for body in bodies:
                root.add_body(body)
        except:
            print("Failed")
            pass
            return np.array(pos_hist)
    
    return np.array(pos_hist)

def plot_trajectories(pos_hist):
    for i in range(num_bodies):
        plt.scatter(pos_hist[:,i,0], pos_hist[:,i,1], s = 0.1)

# def main():
#     num_iters = 1000
#     pos_hist = []
    
#     bodies = []
#     for i in range(num_bodies):
#         j = np.random.rand(5)
#         R = np.random.uniform(0, L/4);
#         theta = np.random.uniform(0, 2*np.pi);
#         x =  R*np.cos(theta);
#         y =  0.25*R*np.sin(theta);
#         R_prim = np.sqrt((x - L/2) ** 2 + (y - L/2) ** 2);
#         u = 0#-1*R_prim*np.sin(theta);
#         v = 0#1*R_prim*np.cos(theta);
#         bodies.append(Body(1,x,y, u, v))

#     root = Node(-L,L,-L,L)
#     this_pos = []
#     for body in bodies:
#         this_pos.append([body.px, body.py])
#         root.add_body(body)
#     pos_hist.append(this_pos)
    
#     for i in range(num_iters):
        
#         for body in bodies:
#             root.calculate_force(body)
#         step(bodies)
        
#         this_pos = []
#         for body in bodies:
#             this_pos.append([body.px, body.py])
#         pos_hist.append(this_pos)
#         print(i)
#         try:
#             root = Node(-L,L,-L,L)
#             for body in bodies:
#                 root.add_body(body)
#         except:
#              pass
#          #   return np.array(pos_hist)
#     # print(pos_hist)
#     return np.array(pos_hist)


def plot_trajectories(pos_hist):
    print(pos_hist.shape)
    for i in range(num_bodies):
        plt.scatter(pos_hist[:,i,0], pos_hist[:,i,1], s = 0.1)
    
    plt.show
   # plt.xlim((-3,3))
   # plt.ylim((-3,3))
        
def writeOutput(result):
    today = datetime.now()
    dateString = today.strftime("%Y-%m-%d-%H-%M")
    print(result.shape)
    result = result.reshape((result.shape[0], result.shape[1] * result.shape[2]))
    np.savetxt(f'../output/result-{dateString}.csv', result, delimiter=',')

# trajectory = main()
# plot_trajectories(trajectory)


# writeOutput(trajectory)
# plt.show()



# plt.figure(figsize = (6,6))
# plt.xlim((0,1))
# plt.ylim((0,1))
# for i,body in enumerate(bodies):
#     plt.scatter(body.px, body.py,label = i, s = 1000*body.mass)
# plt.legend()
# plt.show()
from time import time
def timeit(params=((10, 2), (10, 3), (10, 5), (10, 10), (10, 20), (10, 50), (10, 75), (10, 100), (10, 1000), (10, 10000), (10, 20000), (10, 40000), (10, 50000), (10, 100000)), n_average=2):
    itters = 1
    elapsed = []
    for _, n in params:
        timeaccum = 0
        for k in range(n_average):
            start = time()
            merged = main(itters, n)
            end   = time()
            timeaccum += end-start
            print("finished ", k , itters, n)
        elapsed.append(timeaccum / n_average)

    return elapsed


plt.rcParams.update({'font.size': 24})




results = timeit()
x2 = [2,3,5,10,20,50, 75,100, 1000, 10000, 20000, 40000]


# Y = np.log(results)
# X = np.asarray([(np.log(np.log(item)), np.log(item), 1) for item in x2])

def complex():
    # x = np.linspace(2, 20000, 20000)
    # fn = lambda x : 1e-6 * x ** 1.2 * np.log(x) ** 2.4
    # print(x[0])
    # Y = np.log(fn(x))

    # X = np.asarray([[np.log(np.log(item)), np.log(item), 1] for item in x])
    # X = x[np.newaxis].T
    # print(X.shape)
    # print(Y)
    # print(X)
    # print(Y)
    # exit()
    Y = np.log(results)
    X = np.asarray([(np.log(np.log(item)), np.log(item), 1) for item in x2])

    c, b, a = np.linalg.lstsq(X, Y, rcond = None)[0]
    fn = lambda n : np.exp(a) * n ** b * np.log(n) ** c
    print(np.exp(a), b, c)
    x = np.linspace(0, 40000, 40000)
    plt.plot(x, fn(x), label = f"{np.exp(a):.2f}n^{b:.2f}log(n)^{c:.2f}")
    plt.scatter(x2, results, label = "Nieve Run Time")
    plt.title("N-body Scaling with N (10 itterations) - Barnes Hut")
    plt.xlabel("Bodies")
    plt.ylabel("Run Time (s)")
    plt.legend()
    plt.show()
complex()
exit()

def anlogn():
    Y = results
    X = np.asarray([n * np.log(n) for n in x2])[np.newaxis].T
    print(X)

    a = np.linalg.lstsq(X, Y, rcond = None)[0][0]
    print(a)
    fn = lambda n : a * n * np.log(n)
    x = np.linspace(0, 40000, 40000)
    plt.plot(x, fn(x), label = f"{a:.5f}nlog(n)")
    plt.scatter(x2, results, label = "Run Time")
    plt.title("N-body Scaling with N (10 itterations) - Barnes Hut")
    plt.xlabel("Bodies")
    plt.ylabel("Run Time (s)")
    plt.legend()
    plt.show()
anlogn()