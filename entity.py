from constants import *
import tiles, items
import math, Chunk
import gameUtilities

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


class ActiveNPC:
    def __init__(self):
        pass


class PassiveNPC:
    def __init__(self):
        pass


class ItemEntity:
    def __init__(self):
        pass


class Projectile:
    def __init__(self):
        pass

    def update(self):
        pass


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

        # ! these formulas are used in a lot of places(THEY MAY ALSO CHANGE!)
        self.le           = lambda off: (self.pos[0] - (self.width * 0.5) + off[0], self.pos[1] + off[1])    # Left
        self.ri           = lambda off: (self.pos[0] + (self.width * 0.5) + off[0], self.pos[1] + off[1])    # Right
        self.bo           = lambda off: (self.pos[0] + off[0], self.pos[1] - (self.height * 0.5) + off[1])    # Bottom
        self.up           = lambda off: (self.pos[0] + off[0], self.pos[1] + (self.height * 0.5) + off[1])    # Top
        self.lB           = lambda off: (self.pos[0] - (self.width * 0.5) + off[0], self.pos[1] - (self.height * 0.5) + off[1])    # Left bottom
        self.lU           = lambda off: (self.pos[0] - (self.width * 0.5) + off[0], self.pos[1] + (self.height * 0.5) + off[1])    # Left top
        self.rB           = lambda off: (self.pos[0] + (self.width * 0.5) + off[0], self.pos[1] - (self.height * 0.5) + off[1])    # Right bottom
        self.rU           = lambda off: (self.pos[0] + (self.width * 0.5) + off[0], self.pos[1] + (self.height * 0.5) + off[1])    # Right top
        # These are the rects of the player
        self.left         = self.le((0,0))
        self.right        = self.ri((0,0))
        self.bottom       = self.bo((0,0))
        self.top          = self.up((0,0))
        self.leftBot      = self.lB((0,0))
        self.leftUp       = self.lU((0,0))
        self.rightBot     = self.rB((0,0))
        self.rightUp      = self.rU((0,0))
        # In the following lambda functions, 'p' means position which is a tuple
        self.currChunk    = lambda p: int(math.floor(p[0] / CHUNK_WIDTH_P))
        self.currChunkInd = lambda p: int(self.currChunk(p) - self.chunkBuffer.positions[0])
        self.xPosChunk    = lambda p: int(p[0] // TILE_WIDTH - self.currChunk(p) * CHUNK_WIDTH)
        self.yPosChunk    = lambda p: int(p[1] // TILE_WIDTH)
        self.tile         = lambda p: self.chunkBuffer[self.currChunkInd(p)][self.yPosChunk(p)][self.xPosChunk(p)]
        # self.tileLeft     = self.chunkBuffer[self.currChunkInd( self.le((-1,0)) )][self.yPosChunk( self.le((-1,0)) )][self.xPosChunk( self.le((-1,0)) )]
        # self.tileRight    = self.chunkBuffer[self.currChunkInd( self.ri((1,0)) )][self.yPosChunk( self.ri((1,0)) )][self.xPosChunk( self.ri((1,0)) )]
        # self.tileBot      = self.chunkBuffer[self.currChunkInd( self.bo((0,0)) )][self.yPosChunk( self.bo((-1,0)) )][self.xPosChunk( self.bo((-1,0)) )]
        # self.tileUp       = self.chunkBuffer[self.currChunkInd( self.up((-1,0)) )][self.yPosChunk( self.up((-1,0)) )][self.xPosChunk( self.up((-1,0)) )]
        # self.tileLeftBot  = self.chunkBuffer[self.currChunkInd( self.lB((-1,0)) )][self.yPosChunk( self.lB((-1,0)) )][self.xPosChunk( self.lB((-1,0)) )]
        # self.tileLeftUp   = self.chunkBuffer[self.currChunkInd( self.lU((-1,0)) )][self.yPosChunk( self.lU((-1,0)) )][self.xPosChunk( self.lU((-1,0)) )]
        # self.tileRightBot = self.chunkBuffer[self.currChunkInd( self.rB((-1,0)) )][self.yPosChunk( self.rB((-1,0)) )][self.xPosChunk( self.rB((-1,0)) )]
        # self.tileRightUp  = self.chunkBuffer[self.currChunkInd( self.rU((-1,0)) )][self.yPosChunk( self.rU((-1,0)) )][self.xPosChunk( self.rU((-1,0)) )]

    def update(self, dt):
        """[summary]

        Args:
            dt ([type]): [description]
        """

        self.calcFriction()
        self.checkGround()
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
            if self.vel[i] < -MAX_VEL*(1-self.friction*0.2): self.vel[i] = -MAX_VEL*(1-self.friction*0.2)
            elif self.vel[i] > MAX_VEL*(1-self.friction*0.2): self.vel[i] = MAX_VEL*(1-self.friction*0.2)

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

    def jump(self):
        self.vel[1] = JUMP_VEL
        self.acc[1] = -GRAVITY_ACC
        self.grounded = False

    def calcFriction(self):
        # print(tiles.TILE_ATTR[self.tile(self.lB((0,-1)))])
        # print(self.acc)
        # print()
        if self.tile(self.lB((0,-1))) == 0:
            self.friction = DEFAULT_FRICTION
        else:
            self.friction = tiles.TILE_ATTR[self.tile(self.lB((0,-1)))][FRICTION]

    def checkGround(self):
        if self.tile(self.lB((0,-1))) == 0:
            self.grounded = False
            # return False
        else:
            self.grounded = True
            # return True

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

    def __init__( self , pos:list, chunkBuffer:Chunk.ChunkBuffer, eventHandler, keyState, mouseState, cursorPos, friction:float, health:int=100, grounded:bool=True):
        super().__init__(pos, chunkBuffer, PLYR_WIDTH, PLYR_HEIGHT, friction, health, grounded)

        self.eventHandler = eventHandler

        self.keyState = keyState
        self.mouseState = mouseState
        self.cursorPos = cursorPos

        self.inventory = Inventory(INV_COLS, INV_ROWS)

        self.tangibility = 0
        # 0 means intangible
        # 1 means interacting with blocks
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
            self.jump()

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
            dt (float): [description]
        """

        self.calcFriction()
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
            if self.vel[i] < -MAX_VEL*(1-self.friction*0.2): self.vel[i] = -MAX_VEL*(1-self.friction*0.2)
            elif self.vel[i] > MAX_VEL*(1-self.friction*0.2): self.vel[i] = MAX_VEL*(1-self.friction*0.2)

            self.pos[i] += self.vel[i] * SCALE_VEL * dt

        if  self.hitting and not self.placing :
            chunk = math.floor(self.cursorPos[0] / CHUNK_WIDTH_P)
            chunkInd = chunk - self.chunkBuffer.positions[0]

            x = (self.cursorPos[0] // TILE_WIDTH) - chunk * CHUNK_WIDTH
            y = (self.cursorPos[1] // TILE_WIDTH)

            self.chunkBuffer[ chunkInd ].breakBlockAt( x, y, 10, dt)
            self.chunkBuffer[ chunkInd ].breakWallAt( x, y, 10, dt)

            self.eventHandler.tileBreakFlag = True

            self.eventHandler.tileBreakIndex = chunkInd
            self.eventHandler.tileBreakPos[0] = x
            self.eventHandler.tileBreakPos[1] = y

        elif  self.placing:
            chunk = math.floor(self.cursorPos[0] / CHUNK_WIDTH_P)
            chunkInd = chunk - self.chunkBuffer.positoins[0]

            x = (self.cursorPos[0] // TILE_WIDTH) - chunk * CHUNK_WIDTH
            y = (self.cursorPos[1] // TILE_WIDTH)

            self.eventHandler.tilePlaceFlag = True

            self.eventHandler.tilePlaceFlag = chunkInd
            self.eventHandler.tilePlacePos[0] = x
            self.eventHandler.tilePlacePos[1] = y

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
        self.tileBreakIndex = -1
        self.tileBreakPos = [-1, -1]

        self.tilePlaceFlag = False
        self.tilePlaceIndex = -1
        self.tilePlacePos = [-1, -1]

        self.tileAlterFlag = False
        self.tileAlterPos = [-1, -1]

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


class Menu:
    def __init__(self, h:int, w:int, bL:list, bG=(130, 102, 68)):
        self.height  = h
        self.width   = w
        self.buttons = bL    # The list of buttons where each button is in the form of a list
        # Basic structure of each button - ['Text on button', ypos, color, color2, xpos=None, onlyText=False]
        self.menuSurf = pygame.surface.Surface( (self.height, self.width) )

    def create(self):
        pygame.font.init()
        font = pygame.font.SysFont(pygame.font.get_default_font(), 12)
        for i in self.buttons:
            buttonSurf = font.render(i[0], True, i[2])
            w = buttonSurf.get_width()
            buttonSurf.blit(self.menuSurf, [(self.width-w)//2, i[1]])
        return self.menuSurf

    def update(self, mP, mS):
        pass


class EntityBuffer:
    def __init__( self, cB:Chunk.ChunkBuffer, s:gameUtilities.Serializer):
        self.chunkBuffer = cB
        self.serializer  = s
        self.length = self.chunkBuffer.length
        self.len = 0

        self.entities = [[] for i in range(self.length)]
        self.mousePos       =   [0, 0]
        # self.entities = { }
        # self.mousePos       =   [0, 0]

    def add(self, e:Entity):
        self.entities[e.currChunkInd(e.pos)].append(e)

    def shift( self, d):
        if d < 0:       # Player has moved left
            self.serializer.setEntity(self.chunkBuffer.positions[-1]+1, self.entities[-1])
            del self.entities[-1]
            li = self.serializer.getEntity(self.chunkBuffer.positions[0])
            if li is None:
                self.entities.insert(0, [])
            else:
                self.entities.insert(0, li)
        elif d > 0:     # Player has moved right
            self.serializer.setEntity(self.chunkBuffer.positions[0]-1, self.entities[0])
            del self.entities[0]
            li = self.serializer.getEntity(self.chunkBuffer.positions[-1])
            if li is None:
                self.entities.insert(len(self.entities), [])
            else:
                self.entities.insert(len(self.entities), li)

    def update( self ):
        for i in self.entities:
            for j in i:
                j.update()

    def saveComplete( self ):
        pass
