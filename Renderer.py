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
        cls.chunkBuffer, cls.player, cls.camera, cls.displaySize, cls.screen = chunkBuffer, player, camera, displaySize, screen        
        cls.updateSize()
        cls.updateCam()

    @classmethod
    def render(cls):
        """
            Renders given chunks onto given surface
            Requires chunks, cameraCoors, playerCoors, displaySize as sequences 
        """ 
        rects = [] 

        rightWalker = cls.midpoint  # goes from midpoint to length-1 (both inclusive)
        leftWalker = cls.midpoint-1 # goes from midpoint-1 to 0 (both inclusive)

        numRightDone = 0
        numLeftDone = 0

        while(numLeftDone <= cls.numLeft):

            absoluteChunkIndex = cls.chunkBuffer.positions[leftWalker]

            for j in range(CHUNK_WIDTH-1, -1, -1):

                x = cls.arrayToScreen_x(j, absoluteChunkIndex)
                numLeftDone += 1

                for i in range(cls.lowerIndex, cls.upperIndex+1):                

                    currentTile = cls.chunkBuffer[leftWalker].blocks[i][j]                        
                    y = cls.arrayToScreen_y(i, absoluteChunkIndex)-TILE_WIDTH                       

                    if(currentTile != 0): rects.append(cls.screen.blit(TILE_TABLE[currentTile], [x,y]))

                if(numLeftDone > cls.numLeft): break      

            leftWalker -= 1

        while(numRightDone <= cls.numRight):

            absoluteChunkIndex = cls.chunkBuffer.positions[rightWalker]

            for j in range(0, CHUNK_WIDTH):
                
                x = cls.arrayToScreen_x(j, absoluteChunkIndex)
                numRightDone += 1

                for i in range(cls.lowerIndex, cls.upperIndex+1):                

                    currentTile = cls.chunkBuffer[rightWalker].blocks[i][j]
                    y = cls.arrayToScreen_y(i, absoluteChunkIndex)-TILE_WIDTH             

                    if(currentTile != 0): rects.append(cls.screen.blit(TILE_TABLE[currentTile], [x,y])                        )

                if(numRightDone > cls.numRight): break   

            rightWalker += 1

        # Temporary player crosshair rendering
        
        playercoors = cls.player.copy()
        cls.graphToCamera(playercoors)
        cls.cameraToScreen(playercoors)        

        rects.append(pygame.draw.circle(cls.screen, (255,50,50), playercoors, 2))
        return rects


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
        return cls.displaySize[1] * 0.5 - y

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
        coor[1] = cls.displaySize[1] * 0.5 - coor[1]

    @classmethod
    def chunkToScreen(cls, coor, chunkInd):
        cls.arrayToChunk(coor)       
        cls.chunkToGraph(coor, chunkInd)
        cls.graphToCamera(coor)
        cls.cameraToScreen(coor)

    @classmethod
    def updateSize(cls):        
        cls.midpoint = int((len(cls.chunkBuffer)-1)*0.5)        

        cls.numRight = (cls.displaySize[0] * 0.5)/TILE_WIDTH + CHUNK_WIDTH - 1
        cls.numLeft = (cls.displaySize[0] * 0.5)/TILE_WIDTH + 1
    
    @classmethod
    def updateCam(cls):        
        cls.lowerIndex = int(max((cls.camera[1]-cls.displaySize[1]*0.5)/TILE_WIDTH, 0))
        cls.upperIndex = int(min((cls.camera[1]+cls.displaySize[1]*0.5)/TILE_WIDTH, CHUNK_HEIGHT - 1))