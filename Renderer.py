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

        for c in range(0, len(Renderer.chunkBuffer)):            

            absolutePos = Renderer.chunkBuffer.positions[c]

            for i in range(lowerIndex, upperIndex):
                for j in range(0, CHUNK_WIDTH):
                    currentTile = Renderer.chunkBuffer[c].blocks[i][j]

                    if(currentTile != 0):
                        coors = self.arrayToChunk((j, i))

                        Renderer.chunkToGraph(coors, absolutePos)
                        Renderer.graphToCamera(coors)
                        Renderer.cameraToScreen(coors)
                        
                        TILE_TABLE[currentTile].blit(coors[0], coors[1])                        

        # Temporary player crosshair rendering
        playerPos = [Renderer.player[0], Renderer.player[1]]
        Renderer.graphToCamera(playerPos)
        Renderer.cameraToScreen(playerPos)

        pyglet.shapes.Circle(x=playerPos[0], y=playerPos[1], radius=4, color=(255, 50, 50)).draw()        

    @classmethod
    def arrayToChunk(self, coor):
        # From array-space to chunk-space
        return [coor[0] * TILE_WIDTH, coor[1] * TILE_WIDTH]

    @classmethod
    def chunkToGraph(self, coor, chunkInd):
        # From chunk-space to absolute-space
        coor[0] += (chunkInd * CHUNK_WIDTH * TILE_WIDTH)
        coor[1] = coor[1]

    @classmethod
    def graphToCamera(self, coor):
        # From absolute-space to camera-space
        coor[0] -= Renderer.camera[0]
        coor[1] -= Renderer.camera[1]

    @classmethod
    def cameraToScreen(self, coor):
        # From camera-space to screen-space
        coor[0] += Renderer.displaySize[0] * 0.5
        coor[1] += Renderer.displaySize[1] * 0.5