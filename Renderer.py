import pygame
from pygame.locals import *
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
    def render(self, chunks, cameraCoors, playerCoors, displaySize, surface):
        """Renders given chunks onto given surface

        Requires chunks, cameraCoors, playerCoors, displaySize as sequences as surface as pygame.Surface
        """
        rects = []
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

                        coors[1] += TILE_TABLE[currentTile].rect[2] #currentTile.rect[2] # Add Offset to render from top-left instead of bottom-left
                        self.cameraToScreen(coors, displaySize)

                        rects.append(surface.blit(TILE_TABLE[currentTile].texture, coors, TILE_TABLE[currentTile].rect))

        # Temporary player crosshair rendering
        playerPos = [playerCoors[0], playerCoors[1]]
        self.graphToCamera(playerPos, cameraCoors)
        self.cameraToScreen(playerPos, displaySize)

        pygame.draw.circle(surface, (255,50,50), playerPos, 2)
        return rects

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
        coor[1] = dispSize[1] * 0.5 - coor[1]