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

        # Index of the middle chunk in the chunk buffer
        cls.midChunk        =   int((len(cls.chunkBuffer) - 1) * 0.5)

        # Update constants to reflect new References
        cls.updateRefs()        

    @classmethod
    def renderChunks(cls):         

        for c in range(0,   len(cls.chunkBuffer),   1):
            cls.renderChunk(index = c)

    @classmethod
    def renderChunk(cls,    index):

        currChunkRef        =   cls.chunkBuffer[index]        
        coors               =   [0, 0]

        cls.chunkBuffer.surfaces[index].fill((30, 160, 240))                
        
        for i in range(0,   CHUNK_HEIGHT,   1):
            
            coors[1]    =   (CHUNK_HEIGHT - i - 1) * TILE_WIDTH
            for j in range(0,   CHUNK_WIDTH,    1):

                coors[0]    =   j * TILE_WIDTH
                if(currChunkRef[i, j] is not 0):                    
                    cls.chunkBuffer.surfaces[index].blit(TILE_TABLE[currChunkRef[i, j]], coors)                                            


    @classmethod
    def render(cls):        
        
        for i in range(cls.midChunk,    len(cls.chunkBuffer),  1):

            for j in range(0,   CHUNK_WIDTH,    1):

                sliceInd    =   (cls.chunkBuffer[i].index * CHUNK_WIDTH) + j
                slicePos    =   [sliceInd * TILE_WIDTH - cls.camera[0] + cls.numHorz, 0]

                sliceRect   =   [j * TILE_WIDTH, cls.upIndex, TILE_WIDTH, cls.downIndex]
                sliceSurf   =   cls.chunkBuffer.surfaces[i].subsurface(sliceRect)                

                cls.screen.blit(sliceSurf, slicePos)

            if(slicePos[0] > cls.displaySize[0]): break

        for i in range(cls.midChunk - 1,    -1,   -1):
                        
            for j in range(0,   CHUNK_WIDTH,    1):

                sliceInd    =   (cls.chunkBuffer[i].index * CHUNK_WIDTH) + j
                slicePos    =   [sliceInd * TILE_WIDTH - cls.camera[0] + cls.numHorz, 0]

                sliceRect   =   [j * TILE_WIDTH, cls.upIndex, TILE_WIDTH, cls.downIndex]
                sliceSurf   =   cls.chunkBuffer.surfaces[i].subsurface(sliceRect)                

                cls.screen.blit(sliceSurf, slicePos)

            if(slicePos[0] <= -TILE_WIDTH): break

        #Temporary player crosshair rendering
        playerCoors = cls.player.copy()

        playerCoors[0] -= cls.camera[0]
        playerCoors[1] -= cls.camera[1]

        playerCoors[0] += cls.numHorz
        playerCoors[1] = cls.numVert - playerCoors[1]

        pygame.draw.circle(cls.screen, (255,50,50), playerCoors, 2)

    @classmethod
    def updateRefs(cls):

        # Number of pixels to be rendered on the top and side halves of the camera
        cls.numHorz         =   cls.displaySize[0] * 0.5
        cls.numVert         =   cls.displaySize[1] * 0.5        

        # Indexes of the top and bottom-most pixels of the chunk to be rendered
        # W.R.T to the origin of the chunk-surface
        cls.upIndex         =   CHUNK_HEIGHT_P - (cls.camera[1] + cls.numVert) if(cls.camera[1] + cls.numVert >= 0) else 0
        cls.downIndex       =   cls.displaySize[1] if(cls.upIndex + cls.displaySize[1] <= CHUNK_HEIGHT_P) else CHUNK_HEIGHT_P - cls.upIndex

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