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

    # def __init__( self , pos:list, chunkBuffer:Chunk.ChunkBuffer, eventHandler, friction:float, health:int=100, grounded:bool=True):

    #     super().__init__(pos, chunkBuffer, PLYR_WIDTH, PLYR_HEIGHT, friction, health, grounded)

    #     self.keyState = eventHandler.keyState
    #     self.mouseState = eventHandler.mouseState
    #     self.cursorPos = eventHandler.cursorPos

    #     self.eventHandler = eventHandler

    #     self.inventory = Inventory(INV_COLS, INV_ROWS)

    #     self.tangibility = 0
    #     # 0 means intangible
    #     # 1 means interacing with blocks
    #     # 2 means interacting with walls

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
            self.keyState[pygame.K_e] = False

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

        if  self.hitting and not self.placing :
            chunk = math.floor(self.cursorPos[0] / CHUNK_WIDTH_P)
            chunkInd = chunk - self.chunkBuffer.positions[0]

            x = (self.cursorPos[0] // TILE_WIDTH) - chunk * CHUNK_WIDTH
            y = (self.cursorPos[1] // TILE_WIDTH)

            self.chunkBuffer[ chunkInd ].breakBlockAt( x, y, 10, dt)
            self.chunkBuffer[ chunkInd ].breakWallAt( x, y, 10, dt)

            return chunkInd, x, y

        elif  self.placing:
            chunk = math.floor(self.cursorPos[0] / CHUNK_WIDTH_P)
            chunkInd = chunk - self.chunkBuffer.positoins[0]

            x = (self.cursorPos[0] // TILE_WIDTH) - chunk * CHUNK_WIDTH
            y = (self.cursorPos[1] // TILE_WIDTH)



            return chunkInd, x, y

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

class ClientEventHandler:
    """ Class to abstract recording, management and processing of client-side events

        Types of events

        1> User Keyboard input event:
            Description:
                This event is triggered when the user gives input from the keyboard, i.e. presses or releases keys.
                It may open the console for issuing text commands, open the chat-box for typing messages or cause
                the player to perform an action.
            Associated Data:
                - The key(s) which were pressed (if any) and the key(s) which were released (if any)

        2> User mouse button input event:
            Description:
                This event is triggered when the user gives input from the mouse buttons but does not include the
                movement of the mouse pointer.
            Associated Data:
                - The button(s) which were pressed (if any) and the button(s) which were released (if any)

        3> User mouse pointer input event:
            Description:
                This event is triggered when the user moves the mouse pointer on the window.
                It requires re-calculation of the cursor position.
            Associated Data:
                - New position of the mouse pointer
                - New position of the cursor

        4> Camera movement event:
            Description:
                This event is triggered when the camera moved between 2 consecutive frames.
                It requires the whole screen to be reloaded.
                It requires re-calculation of the cursor position.
            Associated Data:
                - New position of the cursor

        5> Window resize event
            Description:
                This event is triggered when the window is resized.
                It requires the whole screen to be reloaded.
                It requires re-calculation of the cursor position.
            Associated Data:
                - New size of the window
                - New position of the mouse pointer in the updated window
                - New position of the cursor

        6> player movement event
            Description:
                This event is triggered when the player moves or is moved.
                It must be sent to the server
            Associated Data:
                ?

        7> tile/wall break event
            Description:
                This event is triggered when a tile/wall is broken.
                It requires the light-maps to be reloaded
                It requires the affected regions of the screen to be reloaded
                It requires the chunk to be saved (or sent to the server)
            Associated Data:
                - Position of the tile being broken
                - Chunk of the tile being broken
                - Local-specific information of the tile

        8> tile/wall place event
            Description:
                This event is triggered when a tile/wall is placed
                It requires the light-maps to be reloaded
                It requires the affected regions of the screen to be reloaded
                It requires the chunk ot be saved (or sent to the server)
            Associated Data:
                - Position of the tile/wall being places
                - Chunk of the tile/wall being placed

        9> tile/wall alter event
            Description:
                This event is triggered when a tile/wall 's local data is altered
                It may or may not require the light maps to be reloaded
                It may or may not require the affected regions of the screen to be reloaded
                It required the chunk to be saved (or sent to the server)
            Associated Data:
                - Position of the tile/wall being altered
                - Nature of the data which was altered

        10> Chunk-shifting event
            Description:
                This event is triggered when the client's player switches chunks
                It requires the chunk buffer to serialize and de-serialize chunks
                It requires the entity buffer to serialize and de-serialize entities
                It requires the lightmaps to be reloaded
            Associated Data:
                The index of the newly added chunk

        11> Entity spawn event
                Description:
                    This event is triggered when an entity is spawned.
                    It requires the entity buffer to be updated
                    It requires a part of the screen to be updated
                    It may or may not require lightmaps to be reloaded
                    It requires information to be sent to the server
                Associated Data:
                    - The position where the entity was spawned
                    - The description of the entity

        12> Entity despawn event
                Description:
                    This event is triggered when an entity is de-spawned
                    It requires the entity buffer to be updated
                    It requires a part of the screen to be updated
                    It may or may not require lightmaps to be reloaded
                    It requires the information to be sent to the server
                Associated Data:
                    - The position where the entity was spawned
                    - The description of the entity

        13> Entity movement event
                Description:
                    This event is triggered when a mobile entity moves or is moved
                    It requires a part of the screen to be updated
                    It requires information be sent to the server
                    It may or may not require the entity buffer to be updated
                Associated Data:
                    - The new position of the entity
                    - The chunk of the entity
                    - The area of the screen occupied by the entity
                    - The description of the entity
    """

    def __init__( self ):

        self.playerMovementFlag = False
        self.cameraMovementFlag = False

        self.windowResizeFlag = False

        self.keyInFlag = False
        self.keyStates      =   { pygame.K_w : False, pygame.K_a : False, pygame.K_s : False, pygame.K_d : False, pygame.K_e : False }

        self.mouseInFlag = False
        self.mouseState     =   { 1 : False, 2 : False, 3 : False, 4 : False, 5 : False }

        self.mouseCursorFlag = False
        self.mousePos       =   [0, 0]
        self.cursorPos      =   [0, 0]

        self.entityMovementFlag = False
        self.entitySpawnedFlag = False
        self.entityDespawnFlag = False

        self.chunkShiftFlag = False
        self.loadChunkIndex =   None
        self.saveChunkIndex =   None

        self.tileBreakFlag = False
        self.tilePlaceFlag = False
        self.tileAlterFlag = False

    def addKey( self, key ):
        #print("KEY RELEASE")
        if(key in self.keyStates):
            self.keyInFlag = True
            self.keyStates[key] = True

    def remKey( self, key ):
        #print("KEY PRESS")
        if(key in self.keyStates):
            self.keyInFlag = True
            self.keyStates[key] = False

    def addMouseMotion( self, event, camera, displaySize ):
        #print("MOUSE MOTION")
        self.mouseInFlag = True
        self.mousePos[0] = event.pos[0]
        self.mousePos[1] = event.pos[1]
        self.cursorPos[0] = int(camera[0]) + self.mousePos[0] - displaySize[0]//2
        self.cursorPos[1] = int(camera[1]) + displaySize[1]//2 - self.mousePos[1]

    def addMouseButton( self, button ):
        #print("MOUSE PRESS")
        # 1 for left, 2 for middle, 3 for right, 4 for scroll up and 5 for scroll down
        mouseInFlag = True
        self.mouseState[ button ] = True

    def remMouseButton( self, button ):
        #print("MOUSE RELEASE")
        mouseInFlag = True
        self.mouseState[ button ] = False

    def addWindowResize( self ):
        #print("WINDOW RESIZE")
        self.windowResizeFlag = True

    def addCameraMotion( self ):
        #print("CAMERA MOVED")
        self.cameraMovementFlag = True


class EntityBuffer:
    def __init__( self ):
        self.length = 0
        self.len = 0

        self.entities = [ ]
        self.mousePos       =   [0, 0]
        self.entities = { }
        self.mousePos       =   [0, 0]

    def shiftLeftLoadRight( self ):
        pass

    def shiftRightLoadLeft( self ):
        pass

    def saveComplete( self ):
        pass
