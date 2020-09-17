import pyglet
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
    def initialize(cls, chunkBuffer, camera, player, displaySize):
        cls.chunkBuffer, cls.player, cls.camera, cls.displaySize = chunkBuffer, player, camera, displaySize         

    @classmethod
    def render(cls):
        """
            Renders given chunks onto given surface
            Requires chunks, cameraCoors, playerCoors, displaySize as sequences 
        """        

        lowerIndex = int(max((cls.camera[1]-cls.displaySize[1]*0.5)/TILE_WIDTH, 0))
        upperIndex = int(min((cls.camera[1]+cls.displaySize[1]*0.5)/TILE_WIDTH, CHUNK_HEIGHT - 1))

        midpoint = int((len(cls.chunkBuffer)-1)*0.5)

        rightWalker = midpoint  # goes from midpoint to length-1 (both inclusive)
        leftWalker = midpoint-1 # goes from midpoint-1 to 0 (both inclusive)

        numRight, numRightDone = (cls.displaySize[0] * 0.5)/TILE_WIDTH + CHUNK_WIDTH - 1, 0
        numLeft, numLeftDone = (cls.displaySize[0] * 0.5)/TILE_WIDTH + 1, 0

        while(numLeftDone <= numLeft):

            absoluteChunkIndex = cls.chunkBuffer.positions[leftWalker]

            for j in range(CHUNK_WIDTH-1, -1, -1):

                x = cls.arrayToScreen_x(j, absoluteChunkIndex)
                numLeftDone += 1

                for i in range(lowerIndex, upperIndex+1):                

                    currentTile = cls.chunkBuffer[leftWalker].blocks[i][j]                        
                    y = cls.arrayToScreen_y(i, absoluteChunkIndex)                        

                    if(currentTile != 0): TILE_TABLE[currentTile].blit(x, y)        

                if(numLeftDone > numLeft): break      

            leftWalker -= 1

        while(numRightDone <= numRight):

            absoluteChunkIndex = cls.chunkBuffer.positions[rightWalker]

            for j in range(0, CHUNK_WIDTH):
                
                x = cls.arrayToScreen_x(j, absoluteChunkIndex)
                numRightDone += 1

                for i in range(lowerIndex, upperIndex+1):                

                    currentTile = cls.chunkBuffer[rightWalker].blocks[i][j]
                    y = cls.arrayToScreen_y(i, absoluteChunkIndex)                        

                    if(currentTile != 0): TILE_TABLE[currentTile].blit(x, y)                         

                if(numRightDone > numRight): break   

            rightWalker += 1

        # Temporary player crosshair rendering
        playerx = cls.graphToCamera_x(cls.cameraToScreen_x(cls.player[0]))
        playery = cls.graphToCamera_y(cls.cameraToScreen_y(cls.player[1]))
                
        pyglet.shapes.Circle(x=playerx, y=playery, radius=4, color=(255, 50, 50)).draw()        


    @classmethod
    def arrayToChunk_x(cls, x):
        return x * TILE_WIDTH

    @classmethod
    def arrayToChunk_y(cls, y):
        return y * TILE_WIDTH

    @classmethod
    def chunkToGraph_x(cls, x, chunkInd):
        # From chunk-space to absolute-space
        return x + chunkInd * CHUNK_WIDTH * TILE_WIDTH

    @classmethod
    def chunkToGraph_y(cls, y, chunkInd):
        # From chunk-space to absolute-space
        return y

    @classmethod
    def graphToCamera_x(cls, x):
        # From absolute-space to camera-space
        return x - cls.camera[0]        

    @classmethod
    def graphToCamera_y(cls, y):
        # From absolute-space to camera-space
        return y - cls.camera[1]

    @classmethod
    def cameraToScreen_x(cls, x):
        # From camera-space to screen-space
        return x + cls.displaySize[0] * 0.5        

    @classmethod
    def cameraToScreen_y(cls, y):
        # From camera-space to screen-space        
        return y + cls.displaySize[1] * 0.5

    @classmethod
    def arrayToScreen_x(cls, x, chunkInd):
        return cls.cameraToScreen_x(cls.graphToCamera_x(cls.chunkToGraph_x(cls.arrayToChunk_x(x), chunkInd)))        

    @classmethod
    def arrayToScreen_y(cls, y, chunkInd):
        return cls.cameraToScreen_y(cls.graphToCamera_y(cls.chunkToGraph_y(cls.arrayToChunk_y(y), chunkInd)))

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
        coor[1] += cls.displaySize[1] * 0.5

    @classmethod
    def chunkToScreen(cls, coor, chunkInd):
        cls.arrayToChunk(coor)       
        cls.chunkToGraph(coor, chunkInd)
        cls.graphToCamera(coor)
        cls.cameraToScreen(coor)