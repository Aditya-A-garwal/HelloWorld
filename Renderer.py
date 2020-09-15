import pyglet
from Tile import *
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

    def __init__(self):
        pass

    # Take a chunk and render it
    def render(self, chunks, cameraCoors, playerCoors, displaySize):
        """
            Renders given chunks onto given surface

            Requires chunks, cameraCoors, playerCoors, displaySize as sequences as surface as pygame.Surface
        """
        #rects = []
        for c in range(0, len(chunks)):

            lowerIndex = int(max((cameraCoors[1]-displaySize[1]*0.5)/TILE_WIDTH, 0))
            upperIndex = int(min(1 + (cameraCoors[1]+displaySize[1]*0.5)/TILE_WIDTH, CHUNK_HEIGHT)) #1 is added to accomodate for exclusiveness of for loops

            absolutePos = chunks.positions[c]

            for i in range(lowerIndex, upperIndex):
                for j in range(0, CHUNK_WIDTH):
                    currentTile = chunks[c].blocks[i][j]

                    if(currentTile != 0):
                        coors = self.arrayToChunk((j, i))

                        self.chunkToGraph(coors, absolutePos)
                        self.graphToCamera(coors, cameraCoors)
                        self.cameraToScreen(coors, displaySize)
                        
                        TILE_TABLE[currentTile].texture.blit(coors[0], coors[1])                        

        # Temporary player crosshair rendering

        playerPos = [playerCoors[0], playerCoors[1]]
        self.graphToCamera(playerPos, cameraCoors)
        self.cameraToScreen(playerPos, displaySize)

        pyglet.shapes.Circle(x=playerPos[0], y=playerPos[1], radius=4, color=(255, 50, 50)).draw()        

    def arrayToChunk(self, coor):
        # From array-space to chunk-space
        return [coor[0] * TILE_WIDTH, coor[1] * TILE_WIDTH]

    def chunkToGraph(self, coor, chunkInd):
        # From chunk-space to absolute-space
        coor[0] += (chunkInd * CHUNK_WIDTH * TILE_WIDTH)
        coor[1] = coor[1]

    def graphToCamera(self, coor, camCoor):
        # From absolute-space to camera-space
        coor[0] -= camCoor[0]
        coor[1] -= camCoor[1]

    def cameraToScreen(self, coor, dispSize):
        # From camera-space to screen-space
        coor[0] += dispSize[0] * 0.5
        coor[1] += dispSize[1] * 0.5