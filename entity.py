## Entity class

import tables
from constants import *


class Entity:

    def __init__(self, i, sp, p, f, h=100, g=True):
        """[summary]

        Args:
            i (int): [description]
            sp (list): [description]
            p (list): [description]
            f (float): [description]
            h (double, optional): [description]. Defaults to 100.
            g (boolean, optional): [description]. Defaults to True.
        """

        self.id             =  i
        self.spawnPoint     =  sp
        self.pos            =  p
        self.friction       =  f
        self.health         =  h
        self.grounded       =  g

        self.prevkp         =  None
        self.vel            =  [0.0, 0.0]
        self.acc            =  [0.0, 0.0]

    def run(self, kp, kr, dt):
        if self.prevkp is None:
            self.prevkp = kp

        if kr is kp:
            if (kp == pygame.K_a) or (kp == pygame.K_d):
                self.acc[0] = 0
            elif (kp == pygame.K_s) or (kp == pygame.K_w):
                self.acc[1] = 0
            kp = self.prevkp = None

        ## Key handling for movement
        if kp is pygame.K_a:
            self.moveLeft()
        elif kp is pygame.K_d:
            self.moveRight()
        elif kp is pygame.K_w:
            self.moveUp()
        elif kp is pygame.K_s:
            self.moveDown()

        self.update(dt)

        self.prevkp = kp

    def keyPress(self, key):
        if (key is pygame.K_a):
            self.acc[0] = -0.25
        elif (key is pygame.K_d):
            self.acc[0] = 0.25
        elif (key is pygame.K_s):
            self.acc[1] = -0.25
        elif (key is pygame.K_w):
            self.acc[1] = 0.25

    def keyRelease(self, key):
        if (key is pygame.K_a) or (key is pygame.K_d):
            self.acc[0] = 0
        elif (key is pygame.K_s) or (key is pygame.K_w):
            self.acc[1] = 0

    def update(self, dt):

        for i in range(0, 2):
            if(self.acc[i] is not 0):
                self.vel[i] += self.acc[i] * dt/1000

            elif(self.vel[i] < 0):
                self.vel[i] += self.friction * dt/1000

            elif(self.vel[i] > 0):
                self.vel[i] -= self.friction * dt/1000

            if(self.vel[i] > 1): self.vel[i] = 1
            elif(self.vel[i] < -1): self.vel[i] = -1

            self.pos[i] += self.vel[i] * SCALE_SPEED * dt/1000

    # def update(self, dt):
    #     # if self.acc[0]>0:
    #     #     self.acc[0] -= self.friction
    #     # elif self.acc[0]<0:
    #     #     self.acc[0] += self.friction

    #     # if self.acc[0] > 1:
    #     #     self.acc[0] = 1
    #     # elif self.acc[0] < -1:
    #     #     self.acc[0] = -1
    #     # if self.acc[1] > 1:
    #     #     self.acc[1] = 1
    #     # elif self.acc[1] < -1:
    #     #     self.acc[1] = -1

    #     if (self.vel[0] + self.acc[0] * dt) >= 0 >= (self.vel[0] + self.acc[0] * dt - self.friction * dt):
    #         self.vel[0] = 0
    #     elif (self.vel[0] + self.acc[0] * dt) <= 0 <= (self.vel[0] + self.acc[0] * dt + self.friction * dt):
    #         self.vel[0] = 0
    #     elif 0 <= self.vel[0] + self.acc[0] * dt - self.friction * dt < 1:
    #         self.vel[0] += self.acc[0] * dt - self.friction * dt
    #     elif 0 >= self.vel[0] + self.acc[0] * dt + self.friction * dt > -1:
    #         self.vel[0] += self.acc[0] * dt + self.friction * dt
    #     else:
    #         if self.vel[0] < 0:
    #             self.vel[0] = -1
    #         else:
    #             self.vel[0] = 1
    #     if (self.vel[1] + self.acc[1] * dt) >= 0 >= (self.vel[1] + self.acc[1] * dt - self.friction * dt):
    #         self.vel[1] = 0
    #     elif (self.vel[1] + self.acc[1] * dt) <= 0 <= (self.vel[1] + self.acc[1] * dt + self.friction * dt):
    #         self.vel[1] = 0
    #     elif 0 <= self.vel[1] + self.acc[1] * dt - self.friction * dt < 1:
    #         self.vel[1] += self.acc[1] * dt - self.friction * dt
    #     elif 0 >= self.vel[1] + self.acc[1] * dt + self.friction * dt > -1:
    #         self.vel[1] += self.acc[1] * dt + self.friction * dt
    #     else:
    #         if self.vel[1] < 0:
    #             self.vel[1] = -1
    #         else:
    #             self.vel[1] = 1

    #     self.pos[0] += self.vel[0] * dt * SCALE_SPEED
    #     self.pos[1] += self.vel[1] * dt * SCALE_SPEED

    def moveLeft(self):
        self.acc[0] = -self.friction * 2

    def moveRight(self):
        self.acc[0] = self.friction * 2

    def moveUp(self):  # only temporary to adjust to current usage. Will be changed to jump
        # self.vel[1] = JUMP_VEL
        # self.acc[1] = max(0, self.acc[1] - AIR_FRICTION)
        self.acc[1] = self.friction * 2

    def moveDown(self):  # only temporary to adjust to current usage. Will be changed/removed
        self.acc[1] = -self.friction * 2

    def calcFriction(self, c):
        pass

    def notGround(self, c):
        pass

    def damage(self):
        pass

    def notObstacle(self, c):
        pass

# class EntityBuffer:
#     pass