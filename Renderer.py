import pygame
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
        Renderer.screen = screen
        Renderer.chunkBuffer, Renderer.player, Renderer.camera, Renderer.displaySize = chunkBuffer, player, camera, displaySize         

    @classmethod
    def render(cls):
        """
            Renders given chunks onto given surface
            Requires chunks, cameraCoors, playerCoors, displaySize as sequences 
        """        

        lowerIndex = int(max((Renderer.camera[1]-Renderer.displaySize[1]*0.5)/TILE_WIDTH, 0))
        upperIndex = int(min((Renderer.camera[1]+Renderer.displaySize[1]*0.5)/TILE_WIDTH, CHUNK_HEIGHT - 1))

        midpoint = int((len(Renderer.chunkBuffer)-1)*0.5)

        rightWalker = midpoint  # goes from midpoint to length-1 (both inclusive)
        leftWalker = midpoint-1 # goes from midpoint-1 to 0 (both inclusive)

        numRight, numRightDone = (Renderer.displaySize[0] * 0.5)/TILE_WIDTH + CHUNK_WIDTH - 1, 0
        numLeft, numLeftDone = (Renderer.displaySize[0] * 0.5)/TILE_WIDTH + 1, 0

        while(numLeftDone <= numLeft):

            absoluteChunkIndex = Renderer.chunkBuffer.positions[leftWalker]

            for j in range(CHUNK_WIDTH-1, -1, -1):

                x = Renderer.arrayToScreen_x(j, absoluteChunkIndex)
                numLeftDone += 1

                for i in range(lowerIndex, upperIndex+1):                

                    currentTile = Renderer.chunkBuffer[leftWalker].blocks[i][j]                        
                    y = Renderer.arrayToScreen_y(i, absoluteChunkIndex)                        

                    if(currentTile != 0): Renderer.screen.blit(TILE_TABLE[currentTile].texture, [x,y])

                if(numLeftDone > numLeft): break      

            leftWalker -= 1

        while(numRightDone <= numRight):

            absoluteChunkIndex = Renderer.chunkBuffer.positions[rightWalker]

            for j in range(0, CHUNK_WIDTH):
                
                x = Renderer.arrayToScreen_x(j, absoluteChunkIndex)
                numRightDone += 1

                for i in range(lowerIndex, upperIndex+1):                

                    currentTile = Renderer.chunkBuffer[rightWalker].blocks[i][j]
                    y = Renderer.arrayToScreen_y(i, absoluteChunkIndex)                        

                    if(currentTile != 0): Renderer.screen.blit(TILE_TABLE[currentTile].texture, [x,y])                        

                if(numRightDone > numRight): break   

            rightWalker += 1

        # Temporary player crosshair rendering
        playerPos = [Renderer.player[0], Renderer.player[1]]
        Renderer.graphToCamera(playerPos)
        Renderer.cameraToScreen(playerPos)

        pygame.draw.circle(Renderer.screen, (255,50,50), playerPos, 2)        
        #pyglet.shapes.Circle(x=playerx, y=playery, radius=4, color=(255, 50, 50)).draw()        


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
        return x - Renderer.camera[0]        

    @classmethod
    def graphToCamera_y(cls, y):
        # From absolute-space to camera-space
        return y - Renderer.camera[1]

    @classmethod
    def cameraToScreen_x(cls, x):
        # From camera-space to screen-space
        return x + Renderer.displaySize[0] * 0.5        

    @classmethod
    def cameraToScreen_y(cls, y):
        # From camera-space to screen-space        
        return Renderer.displaySize[1] * 0.5 - y

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
        coor[0] -= Renderer.camera[0]
        coor[1] -= Renderer.camera[1]

    @classmethod
    def cameraToScreen(cls, coor):
        # From camera-space to screen-space
        coor[0] += Renderer.displaySize[0] * 0.5
        coor[1] += Renderer.displaySize[1] * 0.5

    @classmethod
    def chunkToScreen(cls, coor, chunkInd):
        cls.arrayToChunk(coor)       
        cls.chunkToGraph(coor, chunkInd)
        cls.graphToCamera(coor)
        cls.cameraToScreen(coor)