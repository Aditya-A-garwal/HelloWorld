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

        self.inventory = Inventory(INV_COLS, INV_ROWS)

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

        if(self.keyState[pygame.K_e]):
            self.inventory.isEnabled = not self.inventory.isEnabled

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

        self.items      = [ [ None for j in range( 0, cols ) ] for i in range( 0, rows ) ]
        self.quantities = [ [ 0 for j in range( 0, cols ) ] for i in range( 0, rows ) ]
        self.positions  = {}

        self.ITEM_TABLE_LOCAL = []

        self.selPos     = 0
        self.selItem    = [None, 0]

        self.itemHeld   = None

        self.isEnabled = False

    def addItem( self, i:int, q:int ):
        pass

    def addItemPos( self, item, quantity:int, pos ):

        if( self.items[pos[1]][pos[0]] != item ):

            self.selItem[0] = self.items[ pos[1] ][ pos[0] ]
            self.selItem[1] = self.quantities[ pos[1] ][ pos[0] ]

            self.items[ pos[1] ][ pos[0] ] = item
            self.quantities[ pos[1] ][ pos[0] ] = quantity

        else:

            self.items[pos[1]][pos[0]] = item
            self.items[pos[1]][pos[0]] = item

            if( self.quantities[pos[1]][pos[0]] + quantity > items.ITEM_ATTR[i][MAX_STACK] ):

                self.selItem[0] = item
                self.selItem[1] = self.quantities[pos[1]][pos[0]] + quantity - items.ITEM_ATTR[i][MAX_STACK]

                self.quantities[pos[1]][pos[0]] = items.ITEM_ATTR[i][MAX_STACK]

            else:

                self.selItem[0] = None
                self.selItem[1] = 0

                self.quantities[pos[1]][pos[0]] += quantity

    def addItemLast( self, i, q ):
        pass

    def remItemStack( self, i, q ):
        pass

    def remItemPos( self, p, q ):
        pass

    def remItemLast( self, i, q ):
        pass

class WorldEventHandler:
    """ Class to abstract recording, management and processing of client-side events

        Types of events

        1> Camera movement event:
            Description:
                This event is triggered when the camera moved between 2 consecutive frames.
                It requires the whole screen to be reloaded.
                It requires re-calculation of the cursor position.
            Associated Data:
                - position of the mouse pointer in the updated window

        2> User Keyboard input event:
            Description:
                This event is triggered when the user gives input from the keyboard, i.e. presses or releases keys.
                It may open the console for issuing text commands, open the chat-box for typing messages or cause
                the player to perform an action.
            Associated Data:
                - The key(s) which were pressed (if any) and the key(s) which were released (if any)

        3> User mouse button input event:
            Description:
                This event is triggered when the user gives input from the mouse buttons but does not include the
                movement of the mouse pointer. It might require either the whole screen or a part to be reloaded
            Associated Data:
                - The button(s) which were pressed (if any) and the button(s) which were released (if any)
                - The changed regions of the chunk (in case of blocks broken, placed or altered
                - The entity being affected, and all associated region data

        4> User mouse pointer input event:
            Description:
                This event is triggered when the user moves the mouse pointer on the window.
                It requires re-calculation of the cursor position.

        5> Window resize event
            Description:
                This event is triggered when the window is resized.
                It requires the whole screen to be reloaded.
                It requires re-calculation of the cursor position.
            Associated Data:
                - The new size of the window
                - position of the mouse pointer in the resized window

        6> tile/wall break event
            Description:
            Associated Data:

        7> tile/wall place event
            Description:
            Associated Data:

        8> tile/wall alter event
            Description:
            Associated Data:

        9> chunk-shifting event
            Description:
            Associated Data:

    """

    def __init__( self ):

        self.userInputFlag  =   False       # This holds whether the user gave an input or not (NOT IMP FOR RENDERING)
        self.vidResizeFlag  =   False       # This holds whether the window was resized or not (IMPORTANT FOR RENDERING)
        self.cameraFlag     =   False       # This holds whether the camera has moved or not (IMPORTANT FOR RENDERING)

        self.keyStates      =   { pygame.K_w : False, pygame.K_a : False, pygame.K_s : False, pygame.K_d : False, pygame.K_e : False }

        self.mouseState     =   { 1 : False, 2 : False, 3 : False, 4 : False, 5 : False }
        self.mousePos       =   [0, 0]
        self.cursorPos      =   [0, 0]

        self.chunkShifts    =   False
        self.loadChunkIndex =   None

    def resetFlags( self ):
        self.userInputFlag = False
        self.vidResizeFlag = False

    def addKey( self, key ):
        #print("KEY RELEASE")
        if(key in self.keyStates):
            self.userInputFlag = True
            self.keyStates[key] = True

    def remKey( self, key ):
        #print("KEY PRESS")
        if(key in self.keyStates):
            self.userInputFlag = True
            self.keyStates[key] = False

    def addMouseMotion( self, event, camera, displaySize ):
        #print("MOUSE MOTION")
        userInputFlag = True
        self.mousePos[0] = event.pos[0]
        self.mousePos[1] = event.pos[1]
        self.cursorPos[0] = int(camera[0]) + self.mousePos[0] - displaySize[0]//2
        self.cursorPos[1] = int(camera[1]) + displaySize[1]//2 - self.mousePos[1]

    # 1 for left, 2 for middle, 3 for right, 4 for scroll up and 5 for scroll down
    def addMouseButton( self, button ):
        #print("MOUSE PRESS")
        userInputFlag = True
        self.mouseState[ button ] = True

    def remMouseButton( self, button ):
        #print("MOUSE RELEASE")
        userInputFlag = True
        self.mouseState[ button ] = False

    def addVideoResize( self ):
        #print("VIDEO RESIZE")
        vidResizeFlag = True

    def addCameraMotion( self ):
        #print("CAMERA MOVED")
        userInputFlag = True


# class EntityBuffer:
#    def __init__( self ):
#        pass
