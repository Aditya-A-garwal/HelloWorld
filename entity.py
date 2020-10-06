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

        self.vel            =  [0.0, 0.0]
        self.acc            =  [0.0, 0.0]

    def run(self, kp, kr, dt):

        if kr is kp:
            if (kp == pygame.K_a) or (kp == pygame.K_d):
                self.acc[0] = 0
            elif (kp == pygame.K_s) or (kp == pygame.K_w):
                self.acc[1] = 0
            kp = None

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

    # def keyPress(self, key):
    #     if (key is pygame.K_a):
    #         self.acc[0] = -0.25
    #     elif (key is pygame.K_d):
    #         self.acc[0] = 0.25
    #     elif (key is pygame.K_s):
    #         self.acc[1] = -0.25
    #     elif (key is pygame.K_w):
    #         self.acc[1] = 0.25

    # def keyRelease(self, key):
    #     if (key is pygame.K_a) or (key is pygame.K_d):
    #         self.acc[0] = 0
    #     elif (key is pygame.K_s) or (key is pygame.K_w):
    #         self.acc[1] = 0

    # def update(self, dt):

    #     for i in range(0, 2):
    #         if(self.acc[i] is not 0):
    #             self.vel[i] += self.acc[i] * dt/1000

    #         elif(self.vel[i] < 0):
    #             self.vel[i] += self.friction * dt/1000

    #         elif(self.vel[i] > 0):
    #             self.vel[i] -= self.friction * dt/1000

    #         if(self.vel[i] > 1): self.vel[i] = 1
    #         elif(self.vel[i] < -1): self.vel[i] = -1

    #         self.pos[i] += self.vel[i] * SCALE_VEL * dt/1000

    def update(self, dt):

        if abs(self.vel[0] + self.acc[0]*dt) >= abs(self.friction*dt):
            if self.vel[0] + self.acc[0]*dt > 0:
                self.acc[0] -= self.friction
            elif self.vel[0] + self.acc[0]*dt < 0:
                self.acc[0] += self.friction
        else:
            self.vel[0] = 0
            self.acc[0] = 0
        if abs(self.vel[1] + self.acc[1]*dt) >= abs(self.friction*dt):
            if self.vel[1] + self.acc[1]*dt > 0:
                self.acc[1] -= self.friction
            elif self.vel[1] + self.acc[1]*dt < 0:
                self.acc[1] += self.friction
        else:
            self.vel[1] = 0
            self.acc[1] = 0

        if self.acc[0] > MAX_ACC:
            self.acc[0] = MAX_ACC
        elif self.acc[0] < -MAX_ACC:
            self.acc[0] = -MAX_ACC
        if self.acc[1] > MAX_ACC:
            self.acc[1] = MAX_ACC
        elif self.acc[1] < -MAX_ACC:
            self.acc[1] = -MAX_ACC

        if -MAX_VEL <= self.vel[0] + self.acc[0] * dt <= MAX_VEL:
            self.vel[0] += self.acc[0] * dt
        else:
            if self.vel[0] + self.acc[0] * dt < 0:
                self.vel[0] = -MAX_VEL
            elif self.vel[0] + self.acc[0] * dt > 0:
                self.vel[0] = MAX_VEL
        if -MAX_VEL <= self.vel[1] + self.acc[1] * dt <= MAX_VEL:
            self.vel[1] += self.acc[1] * dt
        else:
            if self.vel[1] + self.acc[1] * dt < 0:
                self.vel[1] = -MAX_VEL
            elif self.vel[1] + self.acc[1] * dt > 0:
                self.vel[1] = MAX_VEL

        self.pos[0] += self.vel[0] * dt * SCALE_VEL
        self.pos[1] += self.vel[1] * dt * SCALE_VEL

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
