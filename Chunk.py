import pickle
from Tile import *

class Chunk:

    def __init__(self, index = 0):

        self.index              =   index
        self.blocks             =   [[0 for i in range(0,   CHUNK_WIDTH)] for i in range(0, CHUNK_HEIGHT)]
        self.walls              =   [[0 for i in range(0,   CHUNK_WIDTH)] for i in range(0, CHUNK_HEIGHT)]

        self.TILE_TABLE_LOCAL   = {}

    def __getitem__(self, key):
        return self.blocks[key[0]][key[1]]

    def __setitem__(self, key, value):
        self.blocks[key[0]][key[1]] = value

class ChunkBuffer:

    def __init__(self, length, middleIndex, serializer, noiseGenerator):

        self.serializer     =   serializer
        self.noiseGenerator =   noiseGenerator

        self.len            =   length-1
        self.middleIndex    =   int(middleIndex)
        self.leftIndex      =   int(self.middleIndex - self.len * 0.5)
        self.rightIndex     =   int(self.middleIndex + self.len * 0.5)

        self.chunks         =   []
        self.surfaces       =   []

        for i in range(self.leftIndex,  self.rightIndex + 1):

            retrieved   =   self.serializer[i]

            if(retrieved is None):
                retrieved   =   Chunk(index = i)
                self.populateChunk(retrieved)
            else:
                retrieved = pickle.loads(retrieved)

            self.chunks.append(retrieved)
            self.surfaces.append(None)

    def shiftLeft(self):

        self.serializer[self.leftIndex]   =   pickle.dumps(self.chunks[0]) # move leftmost chunk into serializer
        self.leftIndex += 1

        for i in range(0, self.len):
            self.chunks[i]      =   self.chunks[i+1]    # move all chunks one space left
            self.surfaces[i]    =   self.surfaces[i+1]

        self.middleIndex        +=  1

        self.rightIndex         +=  1
        self.chunks[self.len]   =   self.serializer[self.rightIndex] # take next left chunk from serializer and move into buffer        

        if(self.chunks[self.len] is None):
            self.chunks[self.len] = Chunk(index=self.rightIndex)
            self.populateChunk(self.chunks[self.len])
        else:
            self.chunks[self.len] = pickle.loads(self.chunks[self.len])

    def shiftRight(self):

        self.serializer[self.rightIndex] = pickle.dumps(self.chunks[self.len]) # move rightmost chunk into serializer
        self.rightIndex -= 1

        for i in range(self.len, 0, -1):
            self.chunks[i]      =   self.chunks[i-1]    # move all chunks one space right
            self.surfaces[i]    =   self.surfaces[i-1]

        self.middleIndex -= 1

        self.leftIndex -= 1
        self.chunks[0] = self.serializer[self.leftIndex] # take next left chunk from serializer and move into buffer

        if(self.chunks[0] is None):
            self.chunks[0] = Chunk(index=self.leftIndex)
            self.populateChunk(self.chunks[0])
        else:
            self.chunks[0] = pickle.loads(self.chunks[0])

    def saveComplete(self):
        for chunk in self.chunks:
            self.serializer[chunk.index] = pickle.dumps(chunk)

    def populateChunk(self, chunk):

        absouluteIndex  =   chunk.index * CHUNK_WIDTH

        for i in range(0, CHUNK_WIDTH):

            for j in range(0, 10): # Lower bedrock wastes
                bedrockProbability = (10-j)*10
                frontVal    =   (self.noiseGenerator.noise3d(x = absouluteIndex, y = j, z = -1) + 1) * 50
                backVal     =   (self.noiseGenerator.noise3d(x = absouluteIndex, y = j, z = 1) + 1) * 50

                if(0 <= frontVal <= bedrockProbability) :   chunk[j,i] = bedrock
                else                                    :   chunk[j,i] = obsidian

                if(0 <= backVal <= bedrockProbability)  :   chunk.walls[j][i] = bedrock
                else                                    :   chunk.walls[j][i] = obsidian

            for j in range(10, 25): # Upper bedrock wastes
                pass

            absouluteIndex  +=  1

    def __getitem__(self, key):
        return self.chunks[key]

    def __setitem__(self, key, value):
        self.chunks[key] = value

    def __len__(self):
        return len(self.chunks)