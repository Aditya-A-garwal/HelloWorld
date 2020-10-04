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
        self.vel            =  [0, 0]
        self.acc            =  [0, 0]

    def run(self, kp, kr, dt):

        if self.prevkp is None:
            self.prevkp = kp

        if kr is kp:
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

    def update(self, dt):
        if self.acc[0] - self.friction > 0:
            self.acc[0] -= self.friction
        elif self.acc[0] + self.friction < 0:
            self.acc[0] += self.friction
        else:
            self.acc[0] = 0

        if self.acc[0] > 1:
            self.acc[0] = 1
        elif self.acc[0] < -1:
            self.acc[0] = -1
        if self.acc[1] > 1:
            self.acc[1] = 1
        elif self.acc[1] < -1:
            self.acc[1] = -1

        if abs(self.vel[0]+self.acc[0]*dt)<1:
            self.vel[0] += self.acc[0]*dt
        else:
            if self.vel[0] < 0:
                self.vel[0] = -1
            else:
                self.vel[0] = 1
        if abs(self.vel[1]+self.acc[1]*dt) < 1:
            self.vel[1] += self.acc[1]*dt
        else:
            if self.vel[1] < 0:
                self.vel[1] = -1
            else:
                self.vel[1] = 1
        self.pos[0] += self.vel[0]*dt*SCALE_SPEED
        self.pos[1] += self.vel[1]*dt*SCALE_SPEED

    def moveLeft(self):
        self.acc[0] -= self.friction*2

    def moveRight(self):
        self.acc[0] += self.friction*2

    def moveUp(self):    # only temporary to adjust to current usage. Will be changed to jump
        # self.vel[1] = JUMP_VEL
        # self.acc[1] = max(0, self.acc[1] - AIR_FRICTION)
        self.acc[1] += UP_ACC

    def moveDown(self):    # only temporary to adjust to current usage. Will be changed/removed
        self.acc[1] -= DOWN_ACC

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