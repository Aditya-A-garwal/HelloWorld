import pickle
from Tile import *

from random import randint

class Chunk:

    def __init__(  self, index = 0, blocks = None, walls = None, localTable = {}  ):

        """Constructor for the chunk

        Args:
            index (int): The absoulute index of the chunk
            blocks (list): A container to hold the blocks in the chunjk
            walls (list): A container to hold the blocks in the chunjk
            localTable (dictionary): Table containing Local chunk-specific data
        """

        self.index            =  index
        self.TILE_TABLE_LOCAL =  localTable

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

    def __init__(  self, length, middleIndex, serializer, chunkGenerator  ):
        """Contructor for a chunk buffer

        Args:
            length (int): The number of chunks in the chunk buffer (Always an odd integer)
            middleIndex (int): The absoulute index of the middle chunk of the chunk buffer
            serializer (Serializer): The serializer used by the chunk buffer
            chunkGenerator (chunkGenerator): The noise generator used to generate chunks for the first time
        """

        self.serializer     =  serializer
        self.chunkGenerator =  chunkGenerator

        self.len            =  length-1
        self.middleIndex    =  middleIndex
        self.leftIndex      =  self.middleIndex - self.len // 2
        self.rightIndex     =  self.middleIndex + self.len // 2

        self.chunks         =  []
        self.surfaces       =  []
        self.lightSurfs     =  []

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
            self.lightSurfs.append( pygame.Surface( ( CHUNK_WIDTH_P, CHUNK_HEIGHT_P ) ) )

    def shiftLeft(self):

        li, lo                           =  [self.chunks[0].blocks, self.chunks[0].walls], self.chunks[0].TILE_TABLE_LOCAL
        self.serializer[self.leftIndex]  =  pickle.dumps( li ), pickle.dumps( lo ) # move leftmost chunk into serializer
        self.leftIndex                   += 1

        surfRef                          =  self.surfaces[0]
        lightSurfRef                     =  self.lightSurfs[0]

        for i in range( 0, self.len ):

            self.chunks[i]      =  self.chunks[i+1]    # move all chunks one space left
            self.surfaces[i]    =  self.surfaces[i+1]
            self.lightSurfs[i]  =  self.lightSurfs[i+1]

        self.surfaces[self.len]          =  surfRef
        self.lightSurfs[self.len]        =  lightSurfRef
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
        lightSurfRef                      =  self.lightSurfs[self.len]

        for i in range( self.len, 0, -1 ):
            self.chunks[i]      =   self.chunks[i-1]    # move all chunks one space right
            self.surfaces[i]    =   self.surfaces[i-1]
            self.lightSurfs[i]  =   self.lightSurfs[i-1]

        self.surfaces[0]                  =  surfRef
        self.lightSurfs[0]                =  lightSurfRef
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

        absouluteIndex  =   chunk.index * CHUNK_WIDTH

        for i in range(0, CHUNK_WIDTH):

            ## Lower bedrock wastes
            for j in range(0, 10):

                front, back  =  self.chunkGenerator.getLowerBedrockWastes( absouluteIndex, j )
                chunk[j][i]  = front
                chunk.walls[j][i]  = back

            ## Upper bedrock wastes
            for j in range(10, 20):

                front, back   =  self.chunkGenerator.getUpperBedrockWastes( absouluteIndex, j )
                chunk[j][i]  = front
                chunk.walls[j][i]  = back

            ## Lower Caves
            for j in range(20, 50):

                front, back   =  self.chunkGenerator.getLowerCaves( absouluteIndex, j )
                chunk[j][i]  = front
                chunk.walls[j][i]  = back

            ## Middle Caves
            for j in range(50, 90):

                front, back    =  self.chunkGenerator.getMiddleCaves( absouluteIndex, j )
                chunk[j][i]  = front
                chunk.walls[j][i]  = back

            ## Upper Caves
            for j in range(90, 120):

                front, back    =  self.chunkGenerator.getUpperCaves( absouluteIndex, j )
                chunk[j][i]  = front
                chunk.walls[j][i]  = back

            ## Lower Undergrounds
            for j in range(120, 140):

                front, back    =  self.chunkGenerator.getUpperUnderground( absouluteIndex, j )
                chunk[j][i]  = front
                chunk.walls[j][i]  = back

            ## Upper Undergrounds
            for j in range(140, 170):

                front, back    =  self.chunkGenerator.getUpperUnderground( absouluteIndex, j )
                chunk[j][i]  = front
                chunk.walls[j][i]  = back


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