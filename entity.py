from constants import *
import math, Chunk

class Entity:

    def __init__(self, i:int, sp:list, p:list, cb:Chunk.ChunkBuffer, f:float, h:int=100, g:bool=True):
        """[summary]

        Args:
            i (int): [description]
            sp (list): [description]
            p (list): [description]
            cb (Chunk.ChunkBuffer): [description]
            f (float): [description]
            h (int, optional): [description]. Defaults to 100.
            g (bool, optional): [description]. Defaults to True.
        """

        self.id          = i
        self.spawnPoint  = sp
        self.pos         = p
        # self.camera      = c
        # self.display     = d
        self.chunkBuffer = cb
        self.friction    = f
        self.health      = h
        self.grounded    = g

        # self.itemHeld    = None
        self.vel         = [0.0, 0.0]
        self.acc         = [0.0, 0.0]
        self.width       = PLYR_WIDTH
        self.height      = PLYR_HEIGHT
        # self.left        = self.display[0]+self.pos[0]-self.camera[0]-(self.width*0.5)
        # self.right       = self.display[1]-self.pos[1]+self.camera[1]-(self.height*0.5)
        # self.rect        = pygame.rect.Rect(self.left, self.right, )
        #
        # currentChunk = math.floor(self.pos[0] / CHUNK_WIDTH_P)
        # currentChunkInd = currentChunk - self.chunkBuffer.positions[0]
        # xPosChunk = self.pos[0] // TILE_WIDTH - currentChunk * CHUNK_WIDTH
        # yPosChunk = self.pos[1] // TILE_WIDTH
        # self.tile = self.chunkBuffer[currentChunkInd][yPosChunk][xPosChunk]

    def run(self, key):
        """[summary]

        Args:
            key ([type]): [description]
        """
        self.acc[0] = 0
        self.acc[1] = 0

        if( key[pygame.K_a] and not key[pygame.K_d] ):
            self.moveLeft()
        elif( key[pygame.K_d] and not key[pygame.K_a] ):
            self.moveRight()

        if( key[pygame.K_s] and not key[pygame.K_w] ):
            self.moveDown()
        elif( key[pygame.K_w] and not key[pygame.K_s] ):
            self.moveUp()

    def run2( self, mouse: dict ): # ! this should actually belong to the player
        """[summary]

        Args:
            mouse ([type]): [description]
        """
        if(mouse[1]): # left is there
            pass
        if(mouse[2]): # middle is there
            pass
        if(mouse[3]): # right is there
            pass
        if(mouse[4]): # scroll up
            pass
        if(mouse[5]): # scroll down
            pass

    def update(self, dt):
        """[summary]

        Args:
            dt ([type]): [description]
        """

        for i in range(0, 2):
            nextVel = self.vel[i] + self.acc[i]*dt
            absVel  = abs(nextVel)

            if absVel >= abs(self.friction*dt):
                # self.vel[i] -= (absVel//nextVel)*self.friction*dt
                if nextVel > 0:
                    self.vel[i] -= self.friction*dt
                elif nextVel < 0:
                    self.vel[i] += self.friction*dt
            else:
                self.vel[i] = 0
                self.acc[i] = 0

            # self.acc[i] = min(self.acc[i], MAX_ACC*2)
            # self.acc[i] = max(self.acc[i], -MAX_ACC*2)
            if self.acc[i] > MAX_ACC*2:
                self.acc[i] = MAX_ACC*2
            elif self.acc[i] < -MAX_ACC*2:
                self.acc[i] = -MAX_ACC*2

            self.vel[i] += self.acc[i] * dt
            if self.vel[i] < -MAX_VEL: self.vel[i] = -MAX_VEL
            elif self.vel[i] > MAX_VEL: self.vel[i] = MAX_VEL

            self.pos[i] += self.vel[i] * SCALE_VEL * dt

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

class Player(Entity):

    def __init__( self ):
        pass

class Inventory:

    def __init__( self, cols, rows ):
        """[summary]

        Args:
            cols ([type]): [description]
            rows ([type]): [description]
        """

        self.items          =  [ [ 0 for j in range( 0, rows ) ] for i in range( 0, cols ) ]
        self.quantities     =  [ [ 0 for j in range( 0, rows ) ] for i in range( 0, cols ) ]
        self.positions      =  { }
        self.selectedPos    =  0
        self.selectedItem   =  None

    def addItemStack( self, i, q ):
        pass

    def addItemPos( self, i, q, p ):
        pass

    def addItemLast( self, i, q ):
        pass

    def remItemStack( self, i, q ):
        pass

    def remItemPos( self, p, q ):
        pass

    def remItemLast( self, i, q ):
        pass

# class EntityBuffer:
#     pass
