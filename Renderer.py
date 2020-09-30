from Chunk import *
import math

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
        cls.length          =   len(cls.chunkBuffer)
        cls.midChunk        =   int((cls.length - 1) * 0.5)

        # Update constants to reflect new References
        cls.updateRefs()
        cls.renderChunks()

    @classmethod
    def renderChunks(cls):

        for c in range(0,   cls.length,   1):
            cls.renderChunk(index = c)

    @classmethod
    def renderChunk(cls,    index,  rect = [0, 0, CHUNK_WIDTH, CHUNK_HEIGHT]):

        cls.chunkBuffer.surfaces[index] =   pygame.Surface((CHUNK_WIDTH_P, CHUNK_HEIGHT_P))
        currChunkRef                    =   cls.chunkBuffer[index]
        coors                           =   [0, 0]

        # ! NEEDS TO BE CHECKED (UPDATES THE COMPLETE CHUNK INSTEAD OF PORTION)
        cls.chunkBuffer.surfaces[index].fill((30, 150, 240))

        for i in range(rect[1],   rect[3],   1):

            coors[1]    =   (CHUNK_HEIGHT - i - 1) * TILE_WIDTH
            for j in range(rect[0],   rect[2],    1):

                currTileRef =   currChunkRef[i, j]
                currWallRef =   currChunkRef.walls[i][j]

                coors[0]    =   j * TILE_WIDTH

                if(currTileRef > 0):
                    cls.chunkBuffer.surfaces[index].blit(TILE_TABLE[currTileRef], coors)
                elif(currTileRef < 0):
                    pass
                elif(currWallRef > 0):
                    cls.chunkBuffer.surfaces[index].blit(TILE_TABLE[currWallRef], coors)
                elif(currWallRef < 0):
                    pass


    @classmethod
    def render(cls):

        rightWalker     =   cls.midChunk
        leftWalker      =   cls.midChunk - 1

        while(rightWalker < cls.length):

            tileWalker = 0
            while(tileWalker < CHUNK_WIDTH):

                sliceInd    =   (cls.chunkBuffer[rightWalker].index * CHUNK_WIDTH) + tileWalker
                slicePos    =   [sliceInd * TILE_WIDTH - cls.camera[0] + cls.numHorz, 0]

                sliceRect   =   [tileWalker * TILE_WIDTH, cls.upIndex, TILE_WIDTH, cls.downIndex]
                sliceSurf   =   cls.chunkBuffer.surfaces[rightWalker].subsurface(sliceRect)

                if(slicePos[0] > cls.displaySize[0]):
                    rightWalker = cls.length
                    break

                cls.screen.blit(sliceSurf, slicePos)
                tileWalker += 1

            rightWalker += 1

        while(leftWalker >= 0):

            tileWalker = CHUNK_WIDTH - 1
            while(tileWalker >= 0):

                sliceInd    =   (cls.chunkBuffer[leftWalker].index * CHUNK_WIDTH) + tileWalker
                slicePos    =   [sliceInd * TILE_WIDTH - cls.camera[0] + cls.numHorz, 0]

                sliceRect   =   [tileWalker * TILE_WIDTH, cls.upIndex, TILE_WIDTH, cls.downIndex]
                sliceSurf   =   cls.chunkBuffer.surfaces[leftWalker].subsurface(sliceRect)

                if(slicePos[0] < -TILE_WIDTH):
                    leftWalker = -1
                    break

                cls.screen.blit(sliceSurf, slicePos)
                tileWalker -= 1

            leftWalker -= 1

        # Temporary player crosshair rendering
        playerCoors = cls.player.copy()

        # Translate to be in camera space
        playerCoors[0] -= cls.camera[0]
        playerCoors[1] -= cls.camera[1]

        # Translate to be in screen space
        playerCoors[0] += cls.numHorz
        playerCoors[1] = cls.numVert - playerCoors[1]

        pygame.draw.circle(cls.screen, (255,50,50), playerCoors, 2)

    @classmethod
    def updateSize(cls):

        # Number of pixels to be rendered on the top and side halves of the camera
        cls.numHorz         =   cls.displaySize[0] * 0.5
        cls.numVert         =   cls.displaySize[1] * 0.5

    @classmethod
    def updateCam(cls):

        # Indexes of the top and bottom-most pixels of the chunk to be rendered
        # W.R.T to the origin of the chunk-surface

        cls.upIndex         =   CHUNK_HEIGHT_P - (cls.camera[1] + cls.numVert)
        if(cls.upIndex < 0):
            cls.upIndex         =    0

        cls.downIndex       =   CHUNK_HEIGHT_P - cls.upIndex
        if(cls.downIndex > cls.displaySize[1]):
            cls.downIndex       =   cls.displaySize[1]

    @classmethod
    def updateRefs(cls):

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