import numpy as np
import math
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import csv
sys.setrecursionlimit(2000)


theta = 0.5
dt = 1e-3
num_bodies = 60000
num_iters = 1000
groups = 3
G = 100 / num_bodies / groups +  groups# + 3
epsilon = 1.0
L = 1.0
B = 1000

leapfrog = True
fileName = None
# fileName = "../output/initial-2000n-6000b-2g.csv"
def distance(bod1, bod2):
    x1, y1, z1 = bod1.px, bod1.py, bod1.pz
    x2, y2, z2 = bod2.px, bod2.py, bod2.pz
    return ((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)**0.5

def force(bod1, bod2):
    m1 = bod1.mass
    m2 = bod2.mass
    return G*m1*m2/distance(bod1,bod2)**2

def x_component(bod1, bod2):
    return (bod1.px-bod2.px)/(distance(bod1, bod2)+epsilon)

def y_component(bod1, bod2):
    return (bod1.py-bod2.py)/(distance(bod1, bod2)+epsilon)

def z_component(bod1, bod2):
    return (bod1.pz-bod2.pz)/(distance(bod1, bod2)+epsilon)


class Body:
    def __init__(self, mass, px, py, pz, vx, vy, vz):
        self.mass = mass
        self.px = px
        self.py = py
        self.pz = pz
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.fx = 0
        self.fy = 0
        self.fz = 0
        self.collidedWidth = []
    
    def zero_forces(self, by_root = False):
        if by_root:
            self.fx = 0
            self.fy = 0
            self.fz = 0
            self.colidedWith = []

class Node:
    def __init__(self, xleft, xright, ybot, ytop, zfront, zback):
        # Initialize an empty node, meaning a region in space but no bodies in it and no children
        
        # Define the children and domain. zback > zfront
        #front
        self.topleft, self.topright, self.botleft, self.botright = None, None, None, None
        #back
        self.topleftb, self.toprightb, self.botleftb, self.botrightb = None, None, None, None
        self.xleft, self.xright, self.ybot, self.ytop, self.zfront, self.zback = xleft, xright, ybot, ytop, zfront, zback
        self.centerx = (xleft+xright)/2
        self.centery = (ybot+ytop)/2
        self.centerz = (zfront+zback)/2
        
        # Define the Center of Mass and total Mass
        self.CoMx, self.CoMy, self.CoMz, self.totM = None, None, None, 0
        
        # Define
        self.body = None
        
    def which_child(self, x, y, z):
        assert x< self.xright and x > self.xleft and y < self.ytop and y > self.ybot and z > self.zfront and z < self.zback, "Must be in Rect"
        if x >= self.centerx and y >= self.centery and z < self.centerz: ## front
            return self.topright
        elif x >= self.centerx and y < self.centery and z < self.centerz:
            return self.botright
        elif x < self.centerx and y >= self.centery and z < self.centerz:
            return self.topleft
        elif x < self.centerx and y < self.centery and z < self.centerz:
            return self.botleft
        elif x >= self.centerx and y >= self.centery and z >= self.centerz: ## back
            return self.toprightb
        elif x >= self.centerx and y < self.centery and z >= self.centerz:
            return self.botrightb
        elif x < self.centerx and y >= self.centery and z >= self.centerz:
            return self.topleftb
        elif x < self.centerx and y < self.centery and z >= self.centerz:
            return self.botleftb
        else:
            return None

        
    def add_body(self, new_body):
        # if this node contains no bodies (is a leaf with no bodies)
        if self.body == None and self.topleft == None and self.topright == None and self.botleft == None and self.botright == None and self.topleftb == None and self.toprightb == None and self.botleftb == None and self.botrightb == None:
            self.body = new_body
            self.CoMx = new_body.px
            self.CoMy = new_body.py
            self.CoMz = new_body.pz
            self.totM += new_body.mass

            
        # if this node is internal (non leaf)
        elif self.body == None:
            self.CoMx = (self.totM*self.CoMx + new_body.mass*new_body.px)/(self.totM + new_body.mass)
            self.CoMy = (self.totM*self.CoMy + new_body.mass*new_body.py)/(self.totM + new_body.mass)
            self.CoMz = (self.totM*self.CoMz + new_body.mass*new_body.pz)/(self.totM + new_body.mass)
            self.totM += new_body.mass
            
            childNode = self.which_child(new_body.px, new_body.py, new_body.pz)
            childNode.add_body(new_body)

            
        # if this node is external (leaf that is 1 body)
        else:
            self.topleft = Node(self.xleft, self.centerx, self.centery, self.ytop, self.zfront, self.centerz) # front
            self.topright = Node(self.centerx, self.xright, self.centery, self.ytop, self.zfront, self.centerz)
            self.botleft = Node(self.xleft, self.centerx, self.ybot, self.centery, self.zfront, self.centerz)
            self.botright = Node(self.centerx, self.xright, self.ybot, self.centery, self.zfront, self.centerz)
            self.topleftb = Node(self.xleft, self.centerx, self.centery, self.ytop, self.centerz, self.zback) # back
            self.toprightb = Node(self.centerx, self.xright, self.centery, self.ytop, self.centerz, self.zback)
            self.botleftb = Node(self.xleft, self.centerx, self.ybot, self.centery, self.centerz, self.zback)
            self.botrightb = Node(self.centerx, self.xright, self.ybot, self.centery, self.centerz, self.zback)
            
            childNode = self.which_child(self.body.px, self.body.py, self.body.pz)
            childNode.add_body(self.body)
            
            childNode = self.which_child(new_body.px, new_body.py, new_body.pz)
            childNode.add_body(new_body)
            
            self.CoMx = (self.totM*self.CoMx + new_body.mass*new_body.px)/(self.totM + new_body.mass)
            self.CoMy = (self.totM*self.CoMy + new_body.mass*new_body.py)/(self.totM + new_body.mass)
            self.CoMz = (self.totM*self.CoMz + new_body.mass*new_body.pz)/(self.totM + new_body.mass)
            self.totM += new_body.mass
            self.body = None

            
    def calculate_force(self, body, by_root = False):
        body.zero_forces(by_root)
        
        # if this node is body
        if self.body == body:
            return
        
        # if this node is an empty node
        if self.body == None and self.topleft == None and self.topright == None and self.botleft == None and self.botright == None and self.topleftb == None and self.toprightb == None and self.botleftb == None and self.botrightb == None:
            return
        
        # if this node is a body (external node):
        elif self.body != None:
            f = force(body, self.body)
            body.fx += f*x_component(body, self.body)
            body.fy += f*y_component(body, self.body)
            body.fz += f*z_component(body, self.body)
        
        # if this node is an internal node
        else:
            s = self.xleft-self.xright
            d = ((self.CoMx - body.px)**2+(self.CoMy - body.py)**2+(self.CoMz - body.pz)**2)**0.5 + epsilon
            
            # if aggregate condition is met, aggregate
            if s/d < theta:
                f = G*self.totM*body.mass/d**2
                body.fx += f*(self.CoMx - body.px)/d
                body.fy += f*(self.CoMy - body.py)/d
                body.fz += f*(self.CoMz - body.pz)/d
                
            # if aggregate condition not met, recurse
            else:
                self.topleft.calculate_force(body) # front
                self.topright.calculate_force(body)
                self.botleft.calculate_force(body)
                self.botright.calculate_force(body)
                self.topleftb.calculate_force(body) # back
                self.toprightb.calculate_force(body)
                self.botleftb.calculate_force(body)
                self.botrightb.calculate_force(body)
                    
                
def step(bodies):
    for body in bodies:      
        body.px += body.vx*dt
        body.py += body.vy*dt
        body.pz += body.vz*dt
        body.vx += body.fx/body.mass*dt
        body.vy += body.fy/body.mass*dt
        body.vz += body.fz/body.mass*dt  
        
def preStep(bodies):
    for body in bodies:
        body.vx += body.fx/body.mass*dt / 2.0
        body.vy += body.fy/body.mass*dt / 2.0
        body.vz += body.fz/body.mass*dt / 2.0        
        body.px += body.vx*dt
        body.py += body.vy*dt
        body.pz += body.vz*dt
    

def postStep(bodies):
    for body in bodies:
        body.vx += body.fx/body.mass*dt / 2.0
        body.vy += body.fy/body.mass*dt / 2.0
        body.vz += body.fz/body.mass*dt / 2.0


def writeInitial(bodies):
    today = datetime.now()
    dateString = today.strftime("%Y-%m-%d-%H-%M")
    fileName = f'../output/initial-3d-{dateString}.csv'
    with open(fileName, "w+", newline ="") as csvFile:
        writer = csv.writer(csvFile, delimiter=",")

        for b in bodies:
            writer.writerow([b.mass, b.px, b.py, b.pz, b.vx, b.vy, b.vz])

def loadInitial(fileName):
    bodies = []
    with open(fileName, "r", newline ="") as csvFile:
        reader = csv.reader(csvFile, delimiter=",")
        for line in reader: 
            bodies.append(Body(float(line[0]), float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[5]), float(line[6])))
    return bodies
def main():
    pos_hist = []
    
    bodies = []
    if fileName is not None:
        bodies = loadInitial(fileName)
    else:
        for i in range(int(num_bodies / groups)):
            R = 10*np.random.uniform(0, L/4.0);
            theta = np.random.uniform(0, 2*np.pi);
            x =  R*np.cos(theta);
            y =  0.25*R*np.sin(theta);
            z = np.random.normal(0, L/32)
            R_prim = np.sqrt((x - L/2.0) ** 2 + (y - L/2.0) ** 2);
            vx = -20*R_prim*np.sin(theta);
            vy = 20*R_prim*np.cos(theta);
            vz = 5*R_prim*np.random.normal(0, 1)
            bodies.append(Body(5,x,y,z, vx, vy, vz))
        bodies.append(Body(1e2,.01,.01,.01, 0, 0, 0))

        if groups > 1:
            for i in range(int(num_bodies / groups)):
                R = 10*np.random.uniform(0, L/4.0);
                theta = np.random.uniform(0, 2*np.pi);
                x = R*np.cos(theta);
                y = 0.25*R*np.sin(theta);
                z = np.random.normal(0, L/32)
                R_prim = np.sqrt((x - L/2.0) ** 2 + (y - L/2.0) ** 2);
                
                x += 20 * L / 2
                y += 20 * L / 4
                z += 20 * L / 8

                vx = -20*R_prim*np.sin(theta);
                vy = 20*R_prim*np.cos(theta);
                vz = 5*R_prim*np.random.normal(0, 1)
                bodies.append(Body(5,x,y,z, vx, vy, vz))
            bodies.append(Body(5e2,20 * L / 2,20 * L / 4,20 * L / 8, -0, -0, -0))
        if groups > 2:
            for i in range(int(num_bodies / 3)):
                R = 10*np.random.uniform(0, L/4.0);
                theta = np.random.uniform(0, 2*np.pi);
                x = R*np.cos(theta);
                y = 0.25*R*np.sin(theta);
                z = np.random.normal(0, L/32)
                R_prim = np.sqrt((x - L/2.0) ** 2 + (y - L/2.0) ** 2);
                
                x -= 20 * L / 2
                y -= 20 * L / 4
                z -= 20 * L / 8

                vx = -20*R_prim*np.sin(theta);
                vy = 20*R_prim*np.cos(theta);
                vz = 5*R_prim*np.random.normal(0, 1)
                bodies.append(Body(5,x,y,z, vx, vy, vz))
            bodies.append(Body(5e2, -20*L/2, -20*L/4, -20*L/8, 0, 0, 0))

    writeInitial(bodies)



    # Constructing initial tree and storing initial positions
    root = Node(-B,B,-B,B,-B,B)
    this_pos = []
    for body in bodies:
        this_pos.append([body.px, body.py, body.pz])
        root.add_body(body)
    pos_hist.append(this_pos)
    
    
    # Iterating through simulation
    for i in range(num_iters):

        if leapfrog:
            preStep(bodies)
        for body in bodies:
            root.calculate_force(body, True)
        if leapfrog:
            postStep(bodies)
        else:
            step(bodies)
        
        this_pos = []
        for body in bodies:
            this_pos.append([body.px, body.py, body.pz])
        pos_hist.append(this_pos)
        print(i)
        try:
            root = Node(-B,B,-B,B,-B,B)
            for body in bodies:
                root.add_body(body)
        except:
            # pass
           return np.array(pos_hist)
    
    return np.array(pos_hist)

def plot_trajectories(pos_hist):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for i in range(num_bodies):
        ax.scatter(pos_hist[:,i,0], pos_hist[:,i,1], pos_hist[:,i,2], s = 0.25)
    
    
    # ax.set_xlim(-3,3)
    # ax.set_ylim(-3,3)
    # ax.set_zlim(-3,3)
  #  plt.show()


        
def writeOutput(result):
    today = datetime.now()
    dateString = today.strftime("%Y-%m-%d-%H-%M")
    print(result.shape)
    result = result.reshape((result.shape[0], result.shape[1] * result.shape[2]))
    np.savetxt(f'../output/result-3d-{dateString}.csv', result, delimiter=',')

trajectory = main()

writeOutput(trajectory)
plot_trajectories(trajectory)


# writeOutput(trajectory)
plt.show()

        
        