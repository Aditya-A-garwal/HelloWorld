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
        Renderer.chunkBuffer, Renderer.player, Renderer.camera, Renderer.displaySize = chunkBuffer, player, camera, displaySize         

    @classmethod
    def render(self):
        """
            Renders given chunks onto given surface
            Requires chunks, cameraCoors, playerCoors, displaySize as sequences 
        """        

        lowerIndex = int(max((Renderer.camera[1]-Renderer.displaySize[1]*0.5)/TILE_WIDTH, 0))
        upperIndex = int(min(1 + (Renderer.camera[1]+Renderer.displaySize[1]*0.5)/TILE_WIDTH, CHUNK_HEIGHT)) 

        length = len(Renderer.chunkBuffer)
        midpoint = int((length-1)*0.5)

        rightWalker = midpoint  # goes from midpoint to length-1
        leftWalker = midpoint-1 # goes from midpoint-1 to 0

        while(leftWalker >= 0):
            absoluteChunkIndex = Renderer.chunkBuffer.positions[leftWalker]
            for j in range(CHUNK_WIDTH-1, -1, -1):
                for i in range(lowerIndex, upperIndex):                
                    currentTile = Renderer.chunkBuffer[leftWalker].blocks[i][j]
                    coors = [j, i]

                    if(currentTile != 0):                        
                        Renderer.chunkToScreen(coors, absoluteChunkIndex)                                                                   
                        TILE_TABLE[currentTile].blit(coors[0], coors[1])        

                if(coors[0] < 0):
                    leftWalker = -1
                    break                
            leftWalker -= 1

        while(rightWalker < length):
            absoluteChunkIndex = Renderer.chunkBuffer.positions[rightWalker]
            for j in range(0, CHUNK_WIDTH):
                for i in range(lowerIndex, upperIndex):                
                    currentTile = Renderer.chunkBuffer[rightWalker].blocks[i][j]
                    coors = [j, i]

                    if(currentTile != 0):                        
                        Renderer.chunkToScreen(coors, absoluteChunkIndex)                                               
                        TILE_TABLE[currentTile].blit(coors[0], coors[1])        

                if(coors[0] > Renderer.displaySize[0]-TILE_WIDTH):
                    leftWalker = length
                    break                                     
            rightWalker += 1
    
        # Temporary player crosshair rendering
        playerPos = Renderer.player.copy()        
        Renderer.graphToCamera(playerPos)
        Renderer.cameraToScreen(playerPos)
        pyglet.shapes.Circle(x=playerPos[0], y=playerPos[1], radius=4, color=(255, 50, 50)).draw()        

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