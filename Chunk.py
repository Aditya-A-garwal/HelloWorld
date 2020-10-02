import pickle
from Tile import *

from random import randint

class Chunk:

    def __init__(  self, index = 0, blocks = None, walls = None, localTable = {}  ):

        """[summary]

        Args:
            index ([type]): [description]
            blocks ([type]): [description]
            walls ([type]): [description]
            localTable ([type]): [description]
        """

        self.index            =  index
        self.TILE_TABLE_LOCAL =  localTable
        # for i in range(0, CHUNK_HEIGHT):
        #     for j in range(0, CHUNK_WIDTH):
        #         self.TILE_TABLE_LOCAL.setdefault( (i,j), [randint(-256, i) for i in range(0, 256)] )

        if(blocks is None):
            self.blocks         =  [[0 for i in range(0,   CHUNK_WIDTH)] for i in range(0, CHUNK_HEIGHT)]
            self.walls          =  [[0 for i in range(0,   CHUNK_WIDTH)] for i in range(0, CHUNK_HEIGHT)]
        else:
            self.blocks         =  blocks
            self.walls          =  walls

    def __getitem__(  self, key  ):
        """[summary]

        Args:
            key ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self.blocks[key]

    def __setitem__(  self, key, value  ):
        """[summary]

        Args:
            key ([type]): [description]
            value ([type]): [description]
        """
        self.blocks[key] = value

class ChunkBuffer:

    def __init__(  self, length, middleIndex, serializer, noiseGenerator  ):
        """[summary]

        Args:
            length ([type]): [description]
            middleIndex ([type]): [description]
            serializer ([type]): [description]
            noiseGenerator ([type]): [description]
        """

        self.serializer     =  serializer
        self.noiseGenerator =  noiseGenerator

        self.len            =  length-1
        self.middleIndex    =  middleIndex
        self.leftIndex      =  self.middleIndex - self.len // 2
        self.rightIndex     =  self.middleIndex + self.len // 2

        self.chunks         =  []
        self.surfaces       =  []

        for i in range( self.leftIndex,  self.rightIndex + 1 ):

            retrieved           =   self.serializer[i]

            if( retrieved is None ):
                retrieved  =   Chunk( i )
                self.populateChunk( retrieved )

            else:
                li         = pickle.loads( retrieved[0] )
                lo         = pickle.loads( retrieved[1] )

                retrieved  = Chunk( i, li[0], li[1], lo )

            self.chunks.append( retrieved )
            self.surfaces.append( pygame.Surface( ( CHUNK_WIDTH_P, CHUNK_HEIGHT_P ) ) )

    def shiftLeft(self):

        li, lo                           =  [self.chunks[0].blocks, self.chunks[0].walls], self.chunks[0].TILE_TABLE_LOCAL
        self.serializer[self.leftIndex]  =  pickle.dumps( li ), pickle.dumps( lo ) # move leftmost chunk into serializer
        self.leftIndex                   += 1

        surfRef                          =  self.surfaces[0]

        for i in range( 0, self.len ):

            self.chunks[i]      =  self.chunks[i+1]    # move all chunks one space left
            self.surfaces[i]    =  self.surfaces[i+1]

        self.surfaces[self.len]          =  surfRef
        self.middleIndex                 += 1

        self.rightIndex                  += 1
        self.chunks[self.len]            =  self.serializer[self.rightIndex] # take next left chunk from serializer and move into buffer

        if( self.chunks[self.len] is None ):
            self.chunks[self.len] = Chunk( self.rightIndex )
            self.populateChunk( self.chunks[self.len] )
        else:
            li, lo                 = pickle.loads( self.chunks[self.len][0]), pickle.loads(self.chunks[self.len][1] )
            self.chunks[self.len]  = Chunk( self.rightIndex, li[0], li[1], lo )

    def shiftRight(self):

        li, lo                            =  [self.chunks[self.len].blocks, self.chunks[self.len].walls], self.chunks[self.len].TILE_TABLE_LOCAL
        self.serializer[self.rightIndex]  =  pickle.dumps(li), pickle.dumps(lo) # move rightmost chunk into serializer
        self.rightIndex                   -= 1

        surfRef                           =  self.surfaces[self.len]

        for i in range(self.len, 0, -1):
            self.chunks[i]      =   self.chunks[i-1]    # move all chunks one space right
            self.surfaces[i]    =   self.surfaces[i-1]

        self.surfaces[0]                  =  surfRef
        self.middleIndex                  -= 1

        self.leftIndex -= 1
        self.chunks[0] = self.serializer[self.leftIndex] # take next left chunk from serializer and move into buffer

        if( self.chunks[0] is None ):
            self.chunks[0] = Chunk( self.leftIndex )
            self.populateChunk( self.chunks[0] )
        else:
            li, lo          =  pickle.loads( self.chunks[0][0]), pickle.loads(self.chunks[0][1] )
            self.chunks[0]  =  Chunk( self.leftIndex, li[0], li[1], lo )

    def saveComplete(self):
        """[summary]
        """
        for chunk in self.chunks:
            self.serializer[chunk.index] = pickle.dumps( [chunk.blocks, chunk.walls] ), pickle.dumps( chunk.TILE_TABLE_LOCAL )

    def populateChunk(self, chunk):
        """[summary]

        Args:
            chunk ([type]): [description]
        """
        absouluteIndex  =   chunk.index * CHUNK_WIDTH

        for i in range(0, CHUNK_WIDTH):

            for j in range(0, 10): ## Lower bedrock wastes

                obsidianProb =   j * 10   #** Goes from 0% to 100%
                frontVal    =  50 + self.noiseGenerator.noise3d(x = absouluteIndex * BEDROCK_LOWER_X, y = j * BEDROCK_LOWER_Y, z = -1) * 50
                backVal     =  50 + self.noiseGenerator.noise3d(x = absouluteIndex * BEDROCK_LOWER_X, y = j * BEDROCK_LOWER_Y, z = 1) * 50

                if(0 <= frontVal < obsidianProb):   chunk[j][i] = obsidian
                else                  :   chunk[j][i] = bedrock

                if(0 <= backVal < obsidianProb) :   chunk.walls[j][i] = obsidian
                else                  :   chunk.walls[j][i] = bedrock

            for j in range(10, 15): ## Upper bedrock wastes

                hellStoneProb       =  12.5 #** Always 12.5%
                frontVal            =  (self.noiseGenerator.noise3d(x = absouluteIndex * BEDROCK_UPPER_X, y = j * BEDROCK_UPPER_Y, z = -1) * 50) + 50

                chunk[j][i]         =  obsidian
                chunk.walls[j][i]   =  obsidian

                if(0 <= frontVal <= hellStoneProb):
                    chunk[j][i]     =  hellstone

            for j in range(15, 40):    ## Lower Caves

                quartzProb  =  25    #** Always 25%
                stoneProb   =  100*(j-15)/20   #** Always 33%

                frontVal    =  (self.noiseGenerator.noise3d(x = absouluteIndex * CAVE_X, y = j * CAVE_Y, z = -1) * 50) + 50
                backVal     =  (self.noiseGenerator.noise3d(x = absouluteIndex * CAVE_X, y = j * CAVE_Y, z = 1) * 50) + 50

                if( frontVal <= stoneProb ):
                    chunk[j][i]  =  greystone

                else:
                    chunk[j][i]  =  obsidian

                if( backVal <= stoneProb ):
                    chunk.walls[j][i]  =  greystone

                else:
                    chunk.walls[j][i] = obsidian

            for j in range(40, 80):    ## Middle Caves

                stoneProb      =  60                  #** Always 50%
                graniteProb    =  stoneProb + 20      #** Always 25%
                limestoneProb  =  graniteProb + 20    #** Always 25%

                frontVal    =  (self.noiseGenerator.noise3d(x = absouluteIndex * CAVE_X, y = j * CAVE_Y, z = -1) * 50) + 50

                if( frontVal <= stoneProb ):
                    chunk[j][i]  =  greystone

                elif( frontVal <= graniteProb ):
                    chunk[j][i]  =  granite

                else:
                    chunk[j][i]  =  limestone

            for j in range(80, 127):    ## Upper Caves

                stoneProb      =  60                    #** Always 50%
                limestoneProb  =  stoneProb + 20        #** Always 25%
                graniteProb    =  limestoneProb + 20    #** Always 25%

                frontVal    =  (self.noiseGenerator.noise3d(x = absouluteIndex * CAVE_X, y = j * CAVE_Y, z = -1) * 50) + 50
                backVal     =  (self.noiseGenerator.noise3d(x = absouluteIndex * CAVE_X, y = j * CAVE_Y, z = 1) * 50) + 50

                if( frontVal <= stoneProb ):
                    chunk[j][i]  =  greystone

                elif( frontVal <= limestoneProb ):
                    chunk[j][i]  =  limestone

                else:
                    chunk[j][i]  =  granite


            absouluteIndex  +=  1

    def __getitem__( self, key ):
        """[summary]

        Args:
            key ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self.chunks[key]

    def __setitem__( self, key, value ):
        """[summary]

        Args:
            key ([type]): [description]
            value ([type]): [description]
        """
        self.chunks[key] = value

    def __len__( self ):
        """[summary]

        Returns:
            [type]: [description]
        """
        return len( self.chunks )