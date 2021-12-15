import numpy as np
# G = 6.67408e-11 
G = 1

class Body:
    def __init__(self, x, y, vx, vy, m, fname=None):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.m = float(m)
        if fname is not None:
            self.fname = fname.rstrip('\n')

        self.fx = 0
        self.fy = 0

    def reset_force(self):
        self.fx = 0
        self.fy = 0

    def update_force(self, body, distance):
        temp = (body.m * self.m * G)/distance
        fx_temp = temp * (body.x - self.x)/np.sqrt(distance)
        fy_temp = temp * (body.y - self.y)/np.sqrt(distance)

        self.fx += fx_temp
        self.fy += fy_temp

    def update_acceleration(self):
        self.ax = self.fx/self.m
        self.ay = self.fy/self.m

    def update_velocity(self, dt):
        self.old_vx = self.vx
        self.old_vy = self.vy
        self.vx += dt * self.ax
        self.vy += dt * self.ay

    def update_position(self, dt):
        self.x += dt * self.old_vx
        self.y += dt * self.old_vy


def step(bodies, dt):
    # compute sum of forces on body i
    for i in range(len(bodies)):
        bodies[i].reset_force()
        for j in range(len(bodies)):
            if i != j:
                distance = (bodies[i].x - bodies[j].x) ** 2 + (bodies[i].y - bodies[j].y) ** 2
                bodies[i].update_force(bodies[j], distance)

    for i in range(len(bodies)):
        bodies[i].update_acceleration()
        bodies[i].update_velocity(dt)
        bodies[i].update_position(dt)

    # return a list of positions, so we can plot it
    x = []
    y = []
    for i in range(len(bodies)):
        x.append(bodies[i].x)
        y.append(bodies[i].y)
    
    return x, y

