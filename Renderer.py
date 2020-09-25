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
    def renderChunks(cls):         
        for c in range(0, len(cls.chunkBuffer)):
            cls.renderChunk(index=c)

    @classmethod
    def renderChunk(cls, index):
        currChunkRef = cls.chunkBuffer[index]        
        cls.chunkBuffer.surfaces[index].fill((30, 160, 240))
        coors = [0,WORLD_HEIGHT - TILE_WIDTH]
        for i in range(0, CHUNK_HEIGHT):
            for j in range(0, CHUNK_WIDTH):
                if(currChunkRef[i,j] is not 0): cls.chunkBuffer.surfaces[index].blit(TILE_TABLE[currChunkRef[i,j]], coors)                
                coors[0] += TILE_WIDTH
            coors[0] = 0
            coors[1] -= TILE_WIDTH 

    @classmethod
    def render(cls):
        """
            Renders given chunks onto given surface
            Requires chunks, cameraCoors, playerCoors, displaySize as sequences 
        """ 

        # Temporary rendering

        for i in range(cls.midpoint, len(cls.chunkBuffer), 1): # Loop to go from midpoint to right
            pass
        for i in range(cls.midpoint, -1, -1): # Loop to go from midpoint to left
            pass

        for i in range(0, len(cls.chunkBuffer)):
            tinySurf = cls.chunkBuffer.surfaces[i].subsurface((0, cls.upIndex, WORLD_CHUNK_WIDTH, cls.numDown+cls.numUp))         
            cls.screen.blit(tinySurf, [WORLD_CHUNK_WIDTH*i, 0])

        # Temporary player crosshair rendering
        
        playercoors = cls.player.copy()
        cls.graphToCamera(playercoors)
        cls.cameraToScreen(playercoors)        

        pygame.draw.circle(cls.screen, (255,50,50), playercoors, 2)

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
        cls.numUp = int(cls.displaySize[1]*0.5) + 1
        cls.numDown = int(cls.displaySize[1]*0.5) + 1
        cls.numLeft = int(cls.displaySize[0]*0.5) + 1
        cls.numRight = int(cls.displaySize[0]*0.5) + 1

    @classmethod
    def updateCam(cls):
        cls.upIndex = cls.camera[1] + cls.numUp
        cls.downIndex = cls.camera[1] - cls.numDown
        cls.leftIndex = cls.camera[0] - cls.numLeft
        cls.rightIndex = cls.camera[0] + cls.numRight

        cls.midpoint = int((len(cls.chunkBuffer)-1)*0.5)

    @classmethod
    def updateRefs(cls):
        cls.updateSize()
        cls.updateCam()