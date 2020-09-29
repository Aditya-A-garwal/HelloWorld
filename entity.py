## Entity class

from pygame.locals import *


class Entity:
    GRAVITY = 9.8

    def __init__(self, i, w, sp, p, f, g=True):
        self.id = i
        self.weight = w
        self.spawnPoint = sp
        self.pos = p
        self.friction = f
        self.grounded = g
        self.prevkp = None
        self.vel = [0, 0]
        self.driftVel = 0

    def run(self, kp, kr, cl, el, pl, dt):
        if self.prevkp is None:
            self.prevkp = kp
        if (kr == kp == K_a) or (kr == kp == K_d) or (self.prevkp != kp):
            self.driftVel = self.vel[0]
            if kr == kp:
                kp = None
        if self.driftVel - self.friction*dt > 0:
            self.driftVel -= self.friction*dt
        elif self.driftVel + self.friction*dt < 0:
            self.driftVel += self.friction*dt
        else:
            self.driftVel = 0

        if kp == K_a:
            if self.vel[0] - self.friction*dt >= -6:
                self.vel[0] -= self.friction*dt
            else:
                self.vel[0] = 6

        elif kp == K_d:
            if self.vel[0] + self.friction*dt <= 6:
                self.vel[0] += self.friction*dt
            else:
                self.vel[0] = 6

        elif kp == K_w:
            self.jump()

        if not self.isObstacle(self.pos[0] + self.vel[0]*dt):
            self.pos[0] += self.vel[0]*dt
        else:
            pass    # set position of player such that right/left edge of hitbox just touches the obstacle
        if not self.isObstacle(self.pos[1] + self.vel[1]*dt):
            self.pos[1] += self.vel[1]*dt
        else:
            pass    # set position of player such that upper edge of hitbox just touches the obstacle

        if not self.groundBelow():
            pass

        self.prevkp = kp

    def moveLeft(self):
        pass

    def moveRight(self):
        pass

    def jump(self):
        pass

    def groundBelow(self):
        pass

    def damage(self):
        pass

    def isObstacle(self, c):
        pass
