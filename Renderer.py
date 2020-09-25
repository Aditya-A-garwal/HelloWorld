from Chunk import *

'''
Translations
    From                        To
1   array-space                 chunk-space
    coordinates in the array    coordinates in the chunk
2   chunk-space                 world-space
    coordinates in the chunk    coordinates in the world (absolute coordinates)
3   world-space                 camera-space
    coordinates in the world    coordinates relative to camera
4   camera-space                screen-space
    coordinates in the array    coordinates on the display
'''
class Renderer:
        
    @classmethod    
    def initialize(cls, chunkBuffer, camera, player, displaySize, screen):         

        # Create references to global objects
        cls.chunkBuffer     =   chunkBuffer
        cls.player          =   player
        cls.camera          =   camera
        cls.displaySize     =   displaySize
        cls.screen          =   screen

        # Update constants to reflect new References
        cls.updateRefs()

    @classmethod
    def renderChunks(cls):         

        for c in range(0,   len(cls.chunkBuffer),   1):
            cls.renderChunk(index = c)

    @classmethod
    def renderChunk(cls,    index):

        currChunkRef        =   cls.chunkBuffer[index]
        coors               =   [0, WORLD_HEIGHT - TILE_WIDTH]

        cls.chunkBuffer.surfaces[index].fill((30, 160, 240))        

        for i in range(0,   CHUNK_HEIGHT,   1):

            for j in range(0,   CHUNK_WIDTH,    1):

                if(currChunkRef[i, j] is not 0):    cls.chunkBuffer.surfaces[index].blit(TILE_TABLE[currChunkRef[i, j]], coors)                
                coors[0]  +=  TILE_WIDTH

            coors[0]    =   0
            coors[1]    -=  TILE_WIDTH 

    @classmethod
    def render(cls):        
        
        # Loop to render from middle-chunk to the bordering chunk on the right-side
        for i in range(cls.midChunk,    cls.midpoint + cls.numRightChunks + 1,     1):

            subSurfRect     =   [0, cls.upIndex, WORLD_CHUNK_WIDTH, cls.upIndex+cls.downIndex]
            tinySurf        =   cls.chunkBuffer.surfaces[i].subsurface(subSurfRect)

            renderPos       =   [int(cls.displaySize[0]*0.5+WORLD_CHUNK_WIDTH*i), 0]
            cls.screen.blit(tinySurf, renderPos)

        # Loop to render from middle-chunk to the bordering chunk on the left-side
        for i in range(cls.midChunk,    cls.midpoint - cls.numLeftChunks - 1,     -1):

            subSurfRect     =   [0, cls.upIndex, WORLD_CHUNK_WIDTH, cls.upIndex + cls.downIndex]
            tinySurf        =   cls.chunkBuffer.surfaces[i].subsurface(subSurfRect)

            renderPos       =   [int(cls.displaySize[0]*0.5+WORLD_CHUNK_WIDTH*i), 0]
            cls.screen.blit(tinySurf, renderPos)

        # Temporary player crosshair rendering        
        playercoors = cls.player.copy()
        cls.graphToCamera(playercoors)
        cls.cameraToScreen(playercoors)        

        pygame.draw.circle(cls.screen, (255,50,50), playercoors, 2)

    @classmethod
    def updateSize(cls):

        # Number of pixels to be rendered on either side of camera to rendered        
        cls.numUp           =   int(cls.displaySize[1] * 0.5)
        cls.numDown         =   int(cls.displaySize[1] * 0.5)
        cls.numLeft         =   int(cls.displaySize[0] * 0.5)
        cls.numRight        =   int(cls.displaySize[0] * 0.5)

        # Index of the middle chunk in the chunk buffer
        cls.midChunk        =   int((len(cls.chunkBuffer) - 1) * 0.5)

        # Number of "complete" chunks to be rendered on either side of the camera
        cls.numRightChunks  =   int(cls.numRight // WORLD_CHUNK_WIDTH)
        cls.numLeftChunks   =   int(cls.numLeft  // WORLD_CHUNK_WIDTH)

        # Indexes (in the chunk buffer) of the "bordering" chunks (final chunks to be rendered on either side)
        cls.finalRightIndex =   cls.midChunk + cls.numRightChunks
        cls.finalLeftIndex  =   cls.midChunk - cls.numLeftChunks

        # Number of pixels left over on either side of the camera after rendering complete chunks
        cls.numRightExtra   =   cls.numRight % WORLD_CHUNK_WIDTH + 1
        cls.numLeftExtra    =   cls.numLeft  % WORLD_CHUNK_WIDTH + 1

    @classmethod
    def updateCam(cls):

        # Indexes of the top and bottom-most pixels of the chunk to be rendered
        # W.R.T to the origin of the chunk-surface at its top-left
        cls.upIndex         =   cls.camera[1] - cls.numUp
        cls.downIndex       =   cls.camera[1] + cls.numDown        

    @classmethod
    def updateRefs(cls):

        # Update all the constants to reflect changes in references
        cls.updateSize()
        cls.updateCam()

# REDUNDANT METHODS
    @classmethod
    def arrayToChunk(cls, coor):
        # From array-space to chunk-space
        coor[0] *= TILE_WIDTH
        coor[1] *= TILE_WIDTH

    @classmethod
    def chunkToGraph(cls, coor, chunkInd):
        # From chunk-space to absolute-space
        coor[0] += (chunkInd * CHUNK_WIDTH * TILE_WIDTH)
        coor[1] = coor[1]

    @classmethod
    def graphToCamera(cls, coor):
        # From absolute-space to camera-space
        coor[0] -= cls.camera[0]
        coor[1] -= cls.camera[1]

    @classmethod
    def cameraToScreen(cls, coor):
        # From camera-space to screen-space
        coor[0] += cls.displaySize[0] * 0.5
        coor[1] = cls.displaySize[1] * 0.5 - coor[1]

    @classmethod
    def chunkToScreen(cls, coor, chunkInd):
        cls.arrayToChunk(coor)       
        cls.chunkToGraph(coor, chunkInd)
        cls.graphToCamera(coor)
        cls.cameraToScreen(coor)