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
        cls.updateRefs()

    @classmethod
    def render(cls):
        """
            Renders given chunks onto given surface
            Requires chunks, cameraCoors, playerCoors, displaySize as sequences 
        """ 
        rects = [] 

        rightWalker = cls.midpoint  # goes from midpoint to length-1 (both inclusive)
        leftWalker = cls.midpoint-1 # goes from midpoint-1 to 0 (both inclusive)

        numRightDone = numLeftDone = 0 
        coors = [0,0]
        
        cls.screen.fill((30, 175, 250))

        flag = True 
        while(flag):
            absoluteChunkIndex = cls.chunkBuffer.positions[leftWalker]
            curChunkRef = cls.chunkBuffer[leftWalker]
            leftWalker -= 1            

            for j in range(CHUNK_WIDTH-1, -1, -1):
                coors[0] = cls.arrayToScreen_x(j, absoluteChunkIndex)

                for i in range(cls.lowerIndex, cls.upperIndex+1):                                    
                    coors[1] = cls.arrayToScreen_y(i)-TILE_WIDTH    
                    curTileRef = curChunkRef.blocks[i][j]                                           

                    if(curTileRef is not 0): rects.append(cls.screen.blit(TILE_TABLE[curTileRef], coors))
                
                numLeftDone += 1
                if(numLeftDone > cls.numLeft): 
                    flag = False
                    break

        flag = True
        while(flag):
            absoluteChunkIndex = cls.chunkBuffer.positions[rightWalker]
            curChunkRef = cls.chunkBuffer[rightWalker]
            rightWalker += 1

            for j in range(0, CHUNK_WIDTH):
                coors[0] = cls.arrayToScreen_x(j, absoluteChunkIndex)

                for i in range(cls.lowerIndex, cls.upperIndex+1):                
                    coors[1] = cls.arrayToScreen_y(i)-TILE_WIDTH             
                    curTileRef = curChunkRef.blocks[i][j]                    

                    if(curTileRef is not 0): rects.append(cls.screen.blit(TILE_TABLE[curTileRef], coors)                        )

                numRightDone += 1
                if(numRightDone > cls.numRight):
                    flag = False
                    break

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
    def chunkToGraph_y(cls, y):
        # From chunk-space to absolute-space
        # Redundant function
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
    def arrayToScreen_y(cls, y):
        return cls.cameraToScreen_y(cls.graphToCamera_y(cls.arrayToChunk_y(y)))

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

        cls.numRight = (cls.displaySize[0] * 0.5)/TILE_WIDTH + CHUNK_WIDTH
        cls.numLeft = (cls.displaySize[0] * 0.5)/TILE_WIDTH
    
    @classmethod
    def updateCam(cls):        
        cls.lowerIndex = int(max((cls.camera[1]-cls.displaySize[1]*0.5)/TILE_WIDTH, 0))
        cls.upperIndex = int(min((cls.camera[1]+cls.displaySize[1]*0.5)/TILE_WIDTH, CHUNK_HEIGHT - 1))

    @classmethod
    def updateRefs(cls):       
        cls.midpoint = int((len(cls.chunkBuffer)-1)*0.5)        

        cls.numRight = (cls.displaySize[0] * 0.5)/TILE_WIDTH + CHUNK_WIDTH
        cls.numLeft = (cls.displaySize[0] * 0.5)/TILE_WIDTH

        cls.lowerIndex = int(max((cls.camera[1]-cls.displaySize[1]*0.5)/TILE_WIDTH, 0))
        cls.upperIndex = int(min((cls.camera[1]+cls.displaySize[1]*0.5)/TILE_WIDTH, CHUNK_HEIGHT - 1))