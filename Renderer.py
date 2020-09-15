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

    def __init__(self, chunkBuffer, camera, player, displaySize):
        self.chunkBuffer = chunkBuffer
        self.camera = camera
        self.player = player
        self.displaySize = displaySize        

    # Take a chunk and render it
    def render(self):
        """
            Renders given chunks onto given surface

            Requires chunks, cameraCoors, playerCoors, displaySize as sequences as surface as pygame.Surface
        """        
        lowerIndex = int(max((self.camera[1]-self.displaySize[1]*0.5)/TILE_WIDTH, 0))
        upperIndex = int(min(1 + (self.camera[1]+self.displaySize[1]*0.5)/TILE_WIDTH, CHUNK_HEIGHT)) #1 is added to accomodate for exclusiveness of for loops
        for c in range(0, len(self.chunkBuffer)):            
            absolutePos = self.chunkBuffer.positions[c]

            for i in range(lowerIndex, upperIndex):
                for j in range(0, CHUNK_WIDTH):
                    currentTile = self.chunkBuffer[c].blocks[i][j]

                    if(currentTile != 0):
                        coors = self.arrayToChunk((j, i))

                        self.chunkToGraph(coors, absolutePos)
                        self.graphToCamera(coors)
                        self.cameraToScreen(coors)
                        
                        TILE_TABLE[currentTile].blit(coors[0], coors[1])                        

        # Temporary player crosshair rendering
        playerPos = [self.player[0], self.player[1]]
        self.graphToCamera(playerPos)
        self.cameraToScreen(playerPos)

        pyglet.shapes.Circle(x=playerPos[0], y=playerPos[1], radius=4, color=(255, 50, 50)).draw()        

    def arrayToChunk(self, coor):
        # From array-space to chunk-space
        return [coor[0] * TILE_WIDTH, coor[1] * TILE_WIDTH]

    def chunkToGraph(self, coor, chunkInd):
        # From chunk-space to absolute-space
        coor[0] += (chunkInd * CHUNK_WIDTH * TILE_WIDTH)
        coor[1] = coor[1]

    def graphToCamera(self, coor):
        # From absolute-space to camera-space
        coor[0] -= self.camera[0]
        coor[1] -= self.camera[1]

    def cameraToScreen(self, coor):
        # From camera-space to screen-space
        coor[0] += self.displaySize[0] * 0.5
        coor[1] += self.displaySize[1] * 0.5