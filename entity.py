from constants import *
import tiles, items
import math, Chunk

#!----------------------------------------------------------------------------------------------------
# todo  Please add all the entities for the various items
# todo  Please make sure that they are named appropriately
# todo  Please make sure that they are numbered properly
#!----------------------------------------------------------------------------------------------------

player = 0
zombie = 1

ENTITY_NAMES = {
    zombie  :   "Zombie"
}
ENTITY_TABLE = {}

class Entity:

    def __init__(self, pos:list, chunkBuffer:Chunk.ChunkBuffer, width, height, friction:float, health:int=100, grounded:bool=True):
        """[summary]

        Args:
            p (list): [description]
            cb (Chunk.ChunkBuffer): [description]
            f (float): [description]
            h (int, optional): [description]. Defaults to 100.
            g (bool, optional): [description]. Defaults to True.
        """

        self.pos         = pos
        self.chunkBuffer = chunkBuffer
        self.friction    = friction
        self.health      = health
        self.grounded    = grounded

        # self.itemHeld    = None
        self.vel         = [0.0, 0.0]
        self.acc         = [0.0, 0.0]

        self.width       = width
        self.height      = height

        self.hitting     = False
        self.placing     = False

        # self.left        = self.display[0]+self.pos[0]-self.camera[0]-(self.width*0.5)
        # self.right       = self.display[1]-self.pos[1]+self.camera[1]-(self.height*0.5)
        # self.rect        = pygame.rect.Rect(self.left, self.right, )
        # ! these formulas are used in a lot of places and must be made into functions (THEY ARE ALSO GOING TO CHANGE!)
        # currentChunk = math.floor(self.pos[0] / CHUNK_WIDTH_P)
        # currentChunkInd = currentChunk - self.chunkBuffer.positions[0]
        # xPosChunk = self.pos[0] // TILE_WIDTH - currentChunk * CHUNK_WIDTH
        # yPosChunk = self.pos[1] // TILE_WIDTH
        # self.tile = self.chunkBuffer[currentChunkInd][yPosChunk][xPosChunk]

    def update(self, dt):
        """[summary]

        Args:
            dt ([type]): [description]
        """

        for i in range(0, 2):
            nextVel = self.vel[i] + self.acc[i]*dt

            if nextVel >= abs(self.friction*dt):
                self.vel[i] -= self.friction*dt
            elif nextVel <= -abs(self.friction*dt):
                self.vel[i] += self.friction*dt

            else:
                self.vel[i] = 0
                self.acc[i] = 0

            self.acc[i] = MAX_ACC*2 if(self.acc[i] > MAX_ACC*2) else -MAX_ACC*2 if(self.acc[i] < -MAX_ACC*2) else self.acc[i]

            self.vel[i] += self.acc[i] * dt
            if self.vel[i] < -MAX_VEL: self.vel[i] = -MAX_VEL
            elif self.vel[i] > MAX_VEL: self.vel[i] = MAX_VEL

            self.pos[i] += self.vel[i] * SCALE_VEL * dt

    def moveLeft(self):
        self.acc[0] = -self.friction * 2

    def moveRight(self):
        self.acc[0] = self.friction * 2

    def moveDown(self):  # only temporary to adjust to current usage. Will be changed/removed
        self.acc[1] = -self.friction * 2

    def moveUp(self):  # only temporary to adjust to current usage. Will be changed to jump
        # self.vel[1] = JUMP_VEL
        # self.acc[1] = max(0, self.acc[1] - AIR_FRICTION)
        self.acc[1] = self.friction * 2

    def calcFriction(self, c):
        pass

    def notGround(self, c):
        pass

    def damage(self):
        pass

    def notObstacle(self, c):
        pass

class Player(Entity):

    def __init__( self , pos:list, chunkBuffer:Chunk.ChunkBuffer, keyState, mouseState, cursorPos, friction:float, health:int=100, grounded:bool=True):
        super().__init__(pos, chunkBuffer, PLYR_WIDTH, PLYR_HEIGHT, friction, health, grounded)

        self.keyState = keyState
        self.mouseState = mouseState
        self.cursorPos = cursorPos

        self.tangibility = 0
        # 0 means intangible
        # 1 means interacing with blocks
        # 2 means interacting with walls

    def run( self ):
        """[summary]

        Args:
            key ([type]): [description]
        """
        self.acc[0] = 0
        self.acc[1] = 0

        self.hitting = False
        self.placing = False

        if( self.keyState[pygame.K_a] and not self.keyState[pygame.K_d] ):
            self.moveLeft()
        elif( self.keyState[pygame.K_d] and not self.keyState[pygame.K_a] ):
            self.moveRight()

        if( self.keyState[pygame.K_s] and not self.keyState[pygame.K_w] ):
            self.moveDown()
        elif( self.keyState[pygame.K_w] and not self.keyState[pygame.K_s] ):
            self.moveUp()

        if(self.mouseState[1]): # left is there
            self.hitting = True

        if(self.mouseState[2]): # middle is there
            self.placing = True

        if(self.mouseState[3]): # right is there
            pass
        if(self.mouseState[4]): # scroll up
            pass
        if(self.mouseState[5]): # scroll down
            pass

    def update( self, dt ):
        """[summary]

        Args:
            dt ([type]): [description]
        """

        for i in range(0, 2):
            nextVel = self.vel[i] + self.acc[i]*dt

            if nextVel >= abs(self.friction*dt):
                self.vel[i] -= self.friction*dt
            elif nextVel <= -abs(self.friction*dt):
                self.vel[i] += self.friction*dt

            else:
                self.vel[i] = 0
                self.acc[i] = 0

            self.acc[i] = MAX_ACC*2 if(self.acc[i] > MAX_ACC*2) else -MAX_ACC*2 if(self.acc[i] < -MAX_ACC*2) else self.acc[i]

            self.vel[i] += self.acc[i] * dt
            if self.vel[i] < -MAX_VEL: self.vel[i] = -MAX_VEL
            elif self.vel[i] > MAX_VEL: self.vel[i] = MAX_VEL

            self.pos[i] += self.vel[i] * SCALE_VEL * dt

        if(self.hitting):
            chunk = math.floor(self.cursorPos[0] / CHUNK_WIDTH_P)
            chunkInd = chunk - self.chunkBuffer.positions[0]

            x = (self.cursorPos[0] // TILE_WIDTH) - chunk * CHUNK_WIDTH
            y = (self.cursorPos[1] // TILE_WIDTH)

            self.chunkBuffer[ chunkInd ].breakBlockAt( x, y, 10, dt)
            self.chunkBuffer[ chunkInd ].breakWallAt( x, y, 10, dt)

            return chunkInd

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
#    def __init__( self ):
#        pass
