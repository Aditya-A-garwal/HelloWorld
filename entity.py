from constants import *

class Entity:

    def __init__(self, i, sp, p, pcb, f, h=100, g=True):
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

        self.parentChunkBuffer = pcb

    # def run(self, kp, kr, dt):

    #     dt /= 1000

    #     if kr is kp:
    #         if (kp == pygame.K_a) or (kp == pygame.K_d):
    #             self.acc[0] = 0
    #         elif (kp == pygame.K_s) or (kp == pygame.K_w):
    #             self.acc[1] = 0
    #         kp = None

    #     ## Key handling for movement
    #     if kp is pygame.K_a:
    #         self.moveLeft()
    #     elif kp is pygame.K_d:
    #         self.moveRight()
    #     elif kp is pygame.K_w:
    #         self.moveUp()
    #     elif kp is pygame.K_s:
    #         self.moveDown()

    def keyPress(self, key):
        if (key is pygame.K_a):
            self.moveLeft()
        elif (key is pygame.K_d):
            self.moveRight()
        elif (key is pygame.K_s):
            self.moveDown()
        elif (key is pygame.K_w):
            self.moveUp()

    def keyRelease(self, key):
        if (key is pygame.K_a or key is pygame.K_d):
            self.acc[0] = 0
        elif (key is pygame.K_s or key is pygame.K_w):
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

            self.pos[i] += self.vel[i] * SCALE_VEL * dt/1000

    # def update(self, dt):

    #     dt /= 1000

    #     for i in range(0, 2):
    #         nextVel = self.vel[0] + self.acc[0]*dt

    #         if abs(nextVel) >= abs(self.friction*dt):
    #             if nextVel > 0:
    #                 self.acc[0] -= self.friction
    #             elif nextVel < 0:
    #                 self.acc[0] += self.friction
    #         else:
    #             self.vel[0] = 0
    #             self.acc[0] = 0

    #         if self.acc[0] > MAX_ACC:
    #             self.acc[0] = MAX_ACC
    #         elif self.acc[0] < -MAX_ACC:
    #             self.acc[0] = -MAX_ACC

    #         self.vel[0] += self.acc[0] * dt
    #         if(self.vel[0] < -MAX_VEL): self.vel[0] = -MAX_VEL
    #         elif(self.vel[0] > MAX_VEL): self.vel[0] = MAX_VEL

    #         self.pos[0] += self.vel[0] * SCALE_VEL * dt

    #     # if -MAX_VEL <= self.vel[0] + self.acc[0] * dt <= MAX_VEL:
    #     #     self.vel[0] += self.acc[0] * dt
    #     # else:
    #     #     if self.vel[0] + self.acc[0] * dt < 0:
    #     #         self.vel[0] = -MAX_VEL
    #     #     elif self.vel[0] + self.acc[0] * dt > 0:
    #     #         self.vel[0] = MAX_VEL

    #     # if -MAX_VEL <= self.vel[1] + self.acc[1] * dt <= MAX_VEL:
    #     #     self.vel[1] += self.acc[1] * dt
    #     # else:
    #     #     if self.vel[1] + self.acc[1] * dt < 0:
    #     #         self.vel[1] = -MAX_VEL
    #     #     elif self.vel[1] + self.acc[1] * dt > 0:
    #     #         self.vel[1] = MAX_VEL

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


class Inventory:

    def __init__( self, cols, rows ):

        self.items = [ [ 0 for j in range( 0, rows ) ] for i in range( 0, cols ) ]
        self.count = [ [ 0 for j in range( 0, rows ) ] for i in range( 0, cols ) ]
        self.positions = { }

    def addItemtoStack( self, item, quantity ):
        pass
    def addItemtoPosition( self, item, quantity, position ):
        pass
    def addItemtoLast( self, item, quantity ):
        pass

    def remItemFromStack( self, item, quantity ):
        pass
    def remItemFromPosition( self, position, quantity ):
        pass
    def remItemFromLast( self, item, quantity ):
        pass

# class EntityBuffer:
#     pass


##  currentChunk = math.floor(xpos/CHUNK_WIDTH_P)
##  currentChunkInd = currentChunk - chunkBuffer.positions[0]
##  xposinChunk = xpos//TILE_WIDTH - currentChunk * CHUNK_WIDTH
##  yposinChunk = ypos//TILE_WIDTH
##  chunkBuffer[currentChunkInd][yposinChunk][xposinChunk]
