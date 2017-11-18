import numpy as np
import random


# Parents Class of Moving Objects
class movingObjects():
    def __init__(self, ix, iy, vx, vy, dt):
        self.x = ix
        self.y = iy
        self.vx = vx
        self.vy = vy
        self.dt = dt


class Vehicle(movingObjects):
    drag_coef = 0.03

    def update_pos(self, acc):
        self.x += self.vx * self.dt
        self.vx += acc - self.drag_coef * self.vx
        self.dir = 0


class Aircraft(movingObjects):
    alpha_x = 0.5
    alpha_y = 1.05
    beta = 1

    def __init__(self, ix, iy, vx, vy, dt):
        movingObjects.__init__(self, ix, iy, vx, vy, dt)
        self.ax = 0
        self.ay = 0
        self.shoot_flag = 0

    def update_pos(self):
        if self.shoot_flag ==0:
           self.x += self.vx * self.dt
           self.y += self.vy * self.dt
           self.vx += self.ax * self.dt
           self.vy += self.ay * self.dt

        self.ax = self.alpha_x * self.ax + (2 * random.random() - 1) * self.beta
        self.ay = max(-10, min(10, self.alpha_y * self.ay + (2 * random.random() - 1) * self.beta))

        print(self.ax, self.ay)

        if self.vx == 0:
            self.dir = 90
        else:
            self.dir = np.arctan(self.vy / self.vx) * 180 / np.pi


class Missile(movingObjects):
    def __init__(self, ix, iy, vx, vy, dt):
        movingObjects.__init__(self, ix, iy, vx, vy, dt)
        self.shoot_flag = 0
    def update_pos(self, aircraft):
        Vr_x = aircraft.vx - self.vx
        Vr_y = aircraft.vy - self.vy
        Rx = aircraft.x - self.x
        Ry = aircraft.y - self.y
        Omega = (Rx * Vr_y - Ry * Vr_x) / (Rx * Rx + Ry * Ry)

        N = 10  # control gain

        ax = max(-1000, min(1000, N * Vr_y * Omega))
        ay = max(-5, min(5, N * Vr_x * Omega))

        # position update
        if self.shoot_flag==0:
           self.vx = self.vx + ax * self.dt
           self.vy = self.vy + ay * self.dt
           self.x = self.x + self.vx * self.dt
           self.y = self.y + self.vy * self.dt


        # calculate new variable
        self.distance = Rx*Rx+Ry*Ry
        if self.vx == 0:
            self.dir = 90
        else:
            self.dir = np.arctan(self.vy / self.vx) * 180 / np.pi - 90