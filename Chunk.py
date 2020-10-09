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

        self.lightMap           =  [[0 for i in range(0,   CHUNK_WIDTH)] for i in range(0, CHUNK_HEIGHT)]

    def __getitem__(  self, key  ):
        return self.blocks[key]

    def __setitem__(  self, key, value  ):
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

        # Create references to required objects
        self.serializer     =  serializer
        self.chunkGenerator =  chunkGenerator

        # Save length and index of last item
        self.length         =  length
        self.len            =  length - 1

        # Positions of the left-most, middle and right-most chunks
        self.positions      =  [ middleIndex - self.len // 2, middleIndex, middleIndex + self.len // 2 ]

        # Create lists of required objects
        self.chunks         =  [ ]
        self.surfaces       =  [ ]
        self.lightSurfs     =  [ ]

        # Load all objects
        for i in range( self.positions[ 0 ],  self.positions[ 2 ] + 1 ):

            retrieved           =   self.serializer[ i ]

            if( retrieved is None ):
                retrieved  =  Chunk( i )
                self.populateChunk( retrieved )

            else:
                li         =  pickle.loads( retrieved[ 0 ] )
                lo         =  pickle.loads( retrieved[ 1 ] )

                retrieved  =  Chunk( i, li[ 0 ], li[ 1 ], lo )

            self.chunks.append( retrieved )
            self.surfaces.append( pygame.Surface( ( CHUNK_WIDTH_P, CHUNK_HEIGHT_P ) ) )
            self.lightSurfs.append( pygame.Surface( ( CHUNK_WIDTH_P, CHUNK_HEIGHT_P ) ) )

        for i in range( 0, self.length ):
            self.formLightMap( i )

    def shiftBuffer( self, deltaChunk ):

        """Shifts the chunkBuffer by one on either side

        Args:
            deltaChunk (int): The change in the player's chunk
            callback (function): Reference to the renderer to render the newly loaded chunks
        """

        #rep = lambda num : ( num-1 )//2
        #rep = lambda num : 0 if num is 1 else -1
        rep = lambda num : 0 if num == 1 else -1

        # Index of the chunk to be dumped (-1 while shifting left, 0 while shifting right) and the extremity needing to be changed
        dumpIndex = rep( deltaChunk)

        # Index of the chunk to be loaded (0 while shifting left, -1 while shifting right) and the extremity needing to be changed
        loadIndex = rep( -deltaChunk )

        # Ready the tiles, walls and local table to be serialized and dump
        li                                              =  [ self.chunks[ dumpIndex ].blocks, self.chunks[ dumpIndex ].walls ]
        lo                                              =  self.chunks[ dumpIndex ].TILE_TABLE_LOCAL
        self.serializer[ self.positions[ dumpIndex ] ]  =  pickle.dumps( li ), pickle.dumps( lo )

        # After dumping, increment the position of the dumped tile by deltaChunk
        self.positions[dumpIndex]                       += deltaChunk

        # Get references to surfaces which must be recycled
        recycleSurf                                     =  self.surfaces[dumpIndex]
        recycleShade                                    =  self.lightSurfs[dumpIndex]

        # Start from last if shifting right otherwise from 0
        moveIndex                                       =  self.len * -dumpIndex

        for i in range( 0, self.len ):

            nextMoveIndex                 =  moveIndex + deltaChunk

            self.chunks[ moveIndex ]      =  self.chunks[ nextMoveIndex ]
            self.surfaces[ moveIndex ]    =  self.surfaces[ nextMoveIndex ]
            self.lightSurfs[ moveIndex ]  =  self.lightSurfs[ nextMoveIndex ]

            moveIndex += deltaChunk

        # Recycle surfaces
        self.surfaces [loadIndex ]                      =  recycleSurf
        self.lightSurfs[ loadIndex ]                    =  recycleShade

        # Increment positions of the chunk to be loaded and the middle chunk by deltaChunk
        self.positions[ 1 ]                             += deltaChunk
        self.positions[ loadIndex ]                     += deltaChunk

        # Load new chunk and populate if not generated
        self.chunks[ loadIndex ]                        =  self.serializer[ self.positions[ loadIndex ] ]

        if( self.chunks[ loadIndex ] is None ):
            self.chunks[ loadIndex ]      =  Chunk( self.positions[ loadIndex ] )
            self.populateChunk( self.chunks[ loadIndex ] )

        else:
            li                      =  pickle.loads( self.chunks[ loadIndex ][ 0 ] )
            lo                      =  pickle.loads( self.chunks[ loadIndex ][ 1 ] )
            self.chunks[loadIndex]  =  Chunk( self.positions[loadIndex], li[ 0 ], li[ 1 ], lo )

        # Form light map for newly loaded chunk and the chunk before it
        # In case of left shift, i=-1,-2 are generated
        # In case of right shift, i=0, 1 are generated
        self.formLightMap( loadIndex )
        self.formLightMap( loadIndex - deltaChunk )

        return loadIndex

    def saveComplete(self):
        """Saves the complete chunk buffer
        """
        for chunk in self.chunks:
            self.serializer[chunk.index] = pickle.dumps( [ chunk.blocks, chunk.walls ] ), pickle.dumps( chunk.TILE_TABLE_LOCAL )

    def formLightMap( self, index ):

        for i in range( 0, CHUNK_HEIGHT ):
            for j in range( 0, CHUNK_WIDTH ):

                currTileRef = self[index][i][j]
                currWallRef = self[index].walls[i][j]

                if(currTileRef > 0 or currWallRef <= 0):    # Front tile is present or wall is absent
                    self[index].lightMap[i][j] = TILE_ATTR[currTileRef][LUMINOSITY]
                elif(currWallRef > 0):                      # Front tile is absent but wall is present
                    self[index].lightMap[i][j] = TILE_ATTR[currTileRef][LUMINOSITY]

                self.propagate(index, j, i)

    def propagate( self, index, x, y, top=True, right=True, bottom=True, left=True ):

        if(index < 0): index = self.length+index

        topVal      =  self[index].lightMap[y][x]-16
        rightVal    =  self[index].lightMap[y][x]-16
        bottomVal   =  self[index].lightMap[y][x]-16
        leftVal     =  self[index].lightMap[y][x]-16

        # Top side
        if(topVal > 0):
            if(y+1 < CHUNK_HEIGHT):         #check if the next position (1 above) is valid
                if(topVal >= self[index].lightMap[y+1][x]):
                    self[index].lightMap[y+1][x]   =  topVal
                    #self.propagate(index, x, y+1)

        # Right side
        if(rightVal > 0):
            if(x+1 < CHUNK_WIDTH):          #check if the next position (1 to the right) is valid
                if(rightVal >= self[index].lightMap[y][x+1]):
                    self[index].lightMap[y][x+1]   =  rightVal
                    #self.propagate(index, x+1, y)

            elif(index+1 < self.length):    #check if next chunk exists in the chunk buffer
                if(rightVal >= self[index+1].lightMap[y][0]):
                    self[index+1].lightMap[y][0]   =  rightVal
                    #self.propagate(index+1, 0, y)

        # Bottom side
        if(bottomVal > 0):
            if(y-1 >= 0):                   #check if the next position (1 below) is valid
                if(bottomVal >= self[index].lightMap[y-1][x]):
                    self[index].lightMap[y-1][x]   =  bottomVal
                    #self.propagate(index, x, y-1)

        # Left side
        if(leftVal > 0):
            if(x-1 >= 0):                   #check if the next position (1 to the left) is valid
                if(leftVal >= self[index].lightMap[y][x-1]):
                    self[index].lightMap[y][x-1]   =  leftVal
                    #self.propagate(index, x-1, y)

            elif(index-1 >= 0):             #check if previous chunk exists in the chunk buffer
                if(leftVal >= self[index-1].lightMap[y][CHUNK_WIDTH-1]):
                    self[index-1].lightMap[y][CHUNK_WIDTH-1]   =  leftVal
                    #self.propagate(index-1, CHUNK_WIDTH-1, y)

    def __getitem__( self, key ):
        return self.chunks[key]

    def __setitem__( self, key, value ):
        self.chunks[key] = value

    def __len__( self ):
        """Returns the number of active chunks

        Returns:
            int: Number of active chunks
        """
        return self.length

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