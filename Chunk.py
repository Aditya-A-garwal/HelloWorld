import pickle
from constants import *
#from noiseModules import RidgedMulti, Voronoi, OpenSimplex
from opensimplex import OpenSimplex

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
            self.blocks         =  [[air for i in range(0,   CHUNK_WIDTH)] for i in range(0, CHUNK_HEIGHT)]
            self.walls          =  [[air for i in range(0,   CHUNK_WIDTH)] for i in range(0, CHUNK_HEIGHT)]
        else:
            self.blocks         =  blocks
            self.walls          =  walls

        self.lightMap           =  [[air for i in range(0,   CHUNK_WIDTH)] for i in range(0, CHUNK_HEIGHT)]


    def formLightMap( self ):

        for i in range(0, CHUNK_HEIGHT):
            for j in range(0, CHUNK_WIDTH):

                self.lightMap[i][j] = TILE_ATTR[self[i][j]][LUMINOSITY]
                # if(currTileRef >= 0):
                #     currLightMap[i][j] = TILE_ATTR[currTileRef][LUMINOSITY]
                # elif(currWallRef >= 0):
                #     currLightMap[i][j] = TILE_ATTR[currTileRef][LUMINOSITY]

    # def propogate( cls, index, x, y ):

    #     currChunkRef = cls.chunkBuffer[index]
    #     currLightMap = currChunkRef.lightMap

    #     if(currLightMap[y][x] > 0):
    #         pass


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

        self.positions      =  [middleIndex - self.len // 2, middleIndex, middleIndex + self.len // 2]

        self.chunks         =  []
        self.surfaces       =  []
        self.lightSurfs     =  []

        self.length         =  length

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
        self.rightIndex                   += -1

        surfRef                           =  self.surfaces[self.len]
        lightSurfRef                      =  self.lightSurfs[self.len]

        for i in range( self.len, 0, -1 ):
            self.chunks[i]      =   self.chunks[i-1]    # move all chunks one space right
            self.surfaces[i]    =   self.surfaces[i-1]
            self.lightSurfs[i]  =   self.lightSurfs[i-1]

        self.surfaces[0]                  =  surfRef
        self.lightSurfs[0]                =  lightSurfRef
        self.middleIndex                  += -1

        self.leftIndex                    += -1
        self.chunks[0] = self.serializer[self.leftIndex] # take next left chunk from serializer and move into buffer

        if( self.chunks[0] is None ):
            self.chunks[0] = Chunk( self.leftIndex )
            self.populateChunk( self.chunks[0] )
        else:
            li, lo          =  pickle.loads( self.chunks[0][0]), pickle.loads(self.chunks[0][1] )
            self.chunks[0]  =  Chunk( self.leftIndex, li[0], li[1], lo )


    def shiftBuffer( self, deltaChunk ):

        rep = lambda num : ( num-1 )//2

        li                                                  =  [self.chunks[rep( deltaChunk )].blocks, self.chunks[rep( deltaChunk )].walls]
        lo                                                  =  self.chunks[rep( deltaChunk )].TILE_TABLE_LOCAL
        self.serializer[self.positions[rep(deltaChunk)]]    =  pickle.dumps( li ), pickle.dumps( lo )

        self.positions[rep(deltaChunk)]                     += deltaChunk

        surfRef                                             =  self.surfaces[rep( deltaChunk )]
        lightSurfRef                                        =  self.lightSurfs[rep( deltaChunk )]

        if( deltaChunk > 0 ):
            print("LEFT")
            for i in range( 0, self.len ):
                self.chunks[i]      =  self.chunks[i+1]
                self.surfaces[i]    =  self.surfaces[i+1]
                self.lightSurfs[i]  =  self.lightSurfs[i+1]

        elif( deltaChunk < 0 ):
            for i in range( self.len, 0, -1 ):
                self.chunks[i]      =   self.chunks[i-1]
                self.surfaces[i]    =   self.surfaces[i-1]
                self.lightSurfs[i]  =   self.lightSurfs[i-1]

        self.surfaces[rep(-deltaChunk)]                     =  surfRef
        self.lightSurfs[rep(-deltaChunk)]                   =  lightSurfRef

        self.positions[1]                                   += deltaChunk
        self.positions[rep(-deltaChunk)]                    += deltaChunk

        self.chunks[rep(-deltaChunk)]                       = self.serializer[self.positions[rep(-deltaChunk)]]

        if( self.chunks[rep(-deltaChunk)] is None ):
            self.chunks[rep(-deltaChunk)] = Chunk( self.positions[rep(-deltaChunk)] )
            self.populateChunk( self.chunks[rep( -deltaChunk )] )
        else:
            li, lo          =  pickle.loads( self.chunks[rep(-deltaChunk)][0] ), pickle.loads( self.chunks[rep(-deltaChunk)][1] )
            self.chunks[0]  =  Chunk( self.positions[rep(-deltaChunk)], li[0], li[1], lo )

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
        """Returns the number of active chunks

        Returns:
            int: Number of active chunks
        """
        return self.length

class chunkGenerator:

    def __init__(self, seed = None):

        """Initializes the noise generator

        Args:
            seed (int, optional): The seed of the noise generator. Defaults to None.
        """

        # self.simp = OpenSimplex()
        # self.voronoi = Voronoi()
        # self.ridgedMulti = RidgedMulti()
        self.simp = OpenSimplex()

    def frontVal(self, x, y):

        """Returns value of (x,y) at front-plane

        Args:
            x (float): The x-coordinate of the noise plane
            y (float): The y-coordinate of the noise plane

        Returns:
            float: Value on the noise plane at (x,y), normalized between 0 and 100
        """

        #return (self.simp[x, y, 0.1] * 50)
        return ( self.simp.noise3d( x, y, 0.1 ) + 1 ) * 50

    def backVal(self, x, y):

        """Returns value of (x,y) at back-plane

        Args:
            x (float): The x-coordinate of the noise plane
            y (float): The y-coordinate of the noise plane

        Returns:
            float: Value on the noise plane at (x,y), normalized between 0 and 100
        """

        #return (self.simp[x, y, -0.1] * 50)
        return ( self.simp.noise3d(x, y, -0.1) + 1 ) * 50

    def getLowerBedrockWastes(self, x, y):

        if(y == 0):
            return bedrock, bedrock

        else:
            front  =  self.frontVal(x * BEDROCK_LOWER_X, y * BEDROCK_LOWER_Y)
            back   =  self.backVal(x * BEDROCK_LOWER_X, y * BEDROCK_LOWER_Y)

            bedrockProbability = 50

            front = obsidian
            if( front <= bedrockProbability ):
                front = bedrock

            back = obsidian
            if( back <= bedrockProbability ):
                back = bedrock

            return front, back

    def getUpperBedrockWastes(self, x, y):

        front  =  self.frontVal(x * BEDROCK_UPPER_X, y * BEDROCK_UPPER_Y)
        back   =  self.backVal(x * BEDROCK_UPPER_X, y * BEDROCK_UPPER_Y)

        obsidianProbability = 70
        stoneProbability = 20 + obsidianProbability
        hellStoneProbability = 12.5 + stoneProbability

        if(front <= obsidianProbability):
            front = obsidian
        elif(front <= stoneProbability):
            front = greystone
        else:
            front = hellstone

        if(back <= obsidianProbability):
            back = obsidian
        else:
            back = greystone

        return front, back

    def getLowerCaves(self, x, y):

        front  =  self.frontVal(x * CAVE_X, y * CAVE_Y)
        back   =  self.backVal(x * CAVE_X, y * CAVE_Y)

        obsidianProbability   =  20
        stoneProbability      =  obsidianProbability + 20
        graniteProbability    =  stoneProbability + 20
        limestoneProbability  =  graniteProbability + 20

        unobtaniumProbability =  limestoneProbability + 10
        diamondProbability    =  unobtaniumProbability + 7.5
        platinumProbability   =  diamondProbability + 7.5

        if(front <= obsidianProbability):
            front = obsidian

        elif(front <= stoneProbability):
            front = greystone

        elif(front <= graniteProbability):
            front = granite

        elif(front <= limestoneProbability):
            front = limestone

        elif(front <= unobtaniumProbability):
            front = unobtaniumOre

        elif(front <= diamondProbability):
            front = diamondOre

        else:
            front = platinumOre

        return front, back

    def getMiddleCaves(self, x, y):

        front  =  self.frontVal(x * CAVE_X, y * CAVE_Y)
        back   =  self.backVal(x * CAVE_X, y * CAVE_Y)

        stoneProbability = 30
        graniteProbability = 20 + stoneProbability
        quartzProbability = 20 + graniteProbability
        unobtaniumProbability = 10 + quartzProbability
        diamondProbability = 10 + unobtaniumProbability
        platinumProbability = 10 + diamondProbability

        if(front <= stoneProbability):
            front = greystone
        elif(front <= graniteProbability):
            front = granite
        elif(front <= quartzProbability):
            front = quartz
        elif(front <= unobtaniumProbability):
            front = unobtaniumOre
        elif(front <= diamondProbability):
            front = diamondOre
        elif(front <= platinumProbability):
            front = platinumOre

        if(back <= stoneProbability):
            back = greystone
        elif(back <= graniteProbability):
            back = granite
        elif(back <= quartzProbability):
            back = quartz
        else:
            back = greystone

        return front, back

    def getUpperCaves(self, x, y):

        front  =  self.frontVal(x * CAVE_X, y * CAVE_Y)
        back   =  self.backVal(x * CAVE_X, y * CAVE_Y)

        stoneProbability = 75
        ironProbability = 12.5 + stoneProbability
        goldProbability = 12.5 + ironProbability

        back = greystone

        if(front <= stoneProbability):
            front = greystone
        elif(front <= ironProbability):
            front = ironOre
        elif(front <= goldProbability):
            front = goldOre

        return front, back

    def getLowerUnderground(self, x, y):

        front  =  self.frontVal(x * UNDERGROUND_X, y * UNDERGROUND_Y)
        back   =  self.backVal(x * UNDERGROUND_X, y * UNDERGROUND_Y)

        gravelProbability = 20
        dirtProbability = 20 + gravelProbability
        redclayProbability = 20 + dirtProbability
        coalProbability = 20 + redclayProbability
        copperProbability = 20 + coalProbability

        if(front <= gravelProbability):
            front = gravel
        elif(front <= dirtProbability):
            front = brownDirt
        elif(front <= redclayProbability):
            front = redClay
        elif(front <= coalProbability):
            front = coke
        elif(front <= copperProbability):
            front = copperOre

        if(back <= gravelProbability):
            back = gravel
        elif(back <= dirtProbability):
            back = brownDirt
        else:
            back = redclayProbability

        return front, back

    def getUpperUnderground(self, x, y):

        front  =  self.frontVal(x * UNDERGROUND_X, y * UNDERGROUND_Y)
        back   =  self.backVal(x * UNDERGROUND_X, y * UNDERGROUND_Y)

        gravelProbability = 20
        dirtProbability = 20 + gravelProbability
        redclayProbability = 20 + dirtProbability
        coalProbability = 20 + redclayProbability
        copperProbability = 20 + coalProbability

        if(front <= gravelProbability):
            front = gravel
        elif(front <= dirtProbability):
            front = brownDirt
        elif(front <= redclayProbability):
            front = redClay
        elif(front <= coalProbability):
            front = coke
        elif(front <= copperProbability):
            front = copperOre

        if(back <= gravelProbability):
            back = gravel
        elif(back <= dirtProbability):
            back = brownDirt
        else:
            back = redclayProbability

        return front, back