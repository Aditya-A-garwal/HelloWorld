import pickle
from Tile import *

class Chunk:

    def __init__(self, index = 0, blocks = None, walls = None, loc = {}):

        self.index              =   index

        if(blocks is None):
            self.blocks             =   [[0 for i in range(0,   CHUNK_WIDTH)] for i in range(0, CHUNK_HEIGHT)]
            self.walls              =   [[0 for i in range(0,   CHUNK_WIDTH)] for i in range(0, CHUNK_HEIGHT)]
        else:
            self.blocks             =   blocks
            self.walls              =   walls

        self.TILE_TABLE_LOCAL   = loc

    def __getitem__(self, key):
        return self.blocks[key]

    def __setitem__(self, key, value):
        self.blocks[key[0]][key[1]] = value

class ChunkBuffer:

    def __init__(self, length, middleIndex, serializer, noiseGenerator):

        self.serializer     =   serializer
        self.noiseGenerator =   noiseGenerator

        self.len            =   length-1
        self.middleIndex    =   middleIndex
        self.leftIndex      =   self.middleIndex - self.len // 2
        self.rightIndex     =   self.middleIndex + self.len // 2

        self.chunks         =   []
        self.surfaces       =   []

        for i in range(self.leftIndex,  self.rightIndex + 1):

            retrieved           =   self.serializer[i]

            if(retrieved is None):
                retrieved   =   Chunk(i)
                self.populateChunk(retrieved)
            else:
                li = pickle.loads(retrieved[0])
                lo = pickle.loads(retrieved[1])
                retrieved = Chunk(i, li[0], li[1], lo)

            self.chunks.append(retrieved)
            self.surfaces.append(None)

    def shiftLeft(self):

        li, lo = [self.chunks[0].blocks, self.chunks[0].walls], self.chunks[0].TILE_TABLE_LOCAL
        self.serializer[self.leftIndex]   =   pickle.dumps(li), pickle.dumps(lo) # move leftmost chunk into serializer
        self.leftIndex += 1

        for i in range(0, self.len):
            self.chunks[i]      =   self.chunks[i+1]    # move all chunks one space left
            self.surfaces[i]    =   self.surfaces[i+1]

        self.middleIndex        +=  1

        self.rightIndex         +=  1
        self.chunks[self.len]   =   self.serializer[self.rightIndex] # take next left chunk from serializer and move into buffer

        if(self.chunks[self.len] is None):
            self.chunks[self.len] = Chunk(self.rightIndex)
            self.populateChunk(self.chunks[self.len])
        else:
            li, lo = pickle.loads(self.chunks[self.len][0]), pickle.loads(self.chunks[self.len][1])
            self.chunks[self.len] = Chunk(self.rightIndex, li[0], li[1], lo)

    def shiftRight(self):

        li, lo = [self.chunks[self.len].blocks, self.chunks[self.len].walls], self.chunks[self.len].TILE_TABLE_LOCAL
        self.serializer[self.rightIndex] = pickle.dumps(li), pickle.dumps(lo) # move rightmost chunk into serializer
        self.rightIndex -= 1

        for i in range(self.len, 0, -1):
            self.chunks[i]      =   self.chunks[i-1]    # move all chunks one space right
            self.surfaces[i]    =   self.surfaces[i-1]

        self.middleIndex -= 1

        self.leftIndex -= 1
        self.chunks[0] = self.serializer[self.leftIndex] # take next left chunk from serializer and move into buffer

        if(self.chunks[0] is None):
            self.chunks[0] = Chunk(self.leftIndex)
            self.populateChunk(self.chunks[0])
        else:
            li, lo = pickle.loads(self.chunks[0][0]), pickle.loads(self.chunks[0][1])
            self.chunks[0] = Chunk(self.leftIndex, li[0], li[1], lo)

    def saveComplete(self):
        for chunk in self.chunks:
            self.serializer[chunk.index] = pickle.dumps([chunk.blocks, chunk.walls]), pickle.dumps(chunk.TILE_TABLE_LOCAL)

    def populateChunk(self, chunk):

        absouluteIndex  =   chunk.index * CHUNK_WIDTH

        for i in range(0, CHUNK_WIDTH):

            for j in range(0, 10): # Lower bedrock wastes

                obsidianProb =   j   # Goes from 0 to 100 (0% to 100%)
                frontVal    =   (self.noiseGenerator.noise3d(x = absouluteIndex * BEDROCK_LOWER_X, y = j * BEDROCK_LOWER_Y, z = -1) + 1) * 5
                backVal     =   (self.noiseGenerator.noise3d(x = absouluteIndex * BEDROCK_LOWER_X, y = j * BEDROCK_LOWER_Y, z = 1) + 1) * 5

                if(0 <= frontVal < obsidianProb):   chunk[j][i] = obsidian
                else                  :   chunk[j][i] = bedrock

                if(0 <= backVal < obsidianProb) :   chunk.walls[j][i] = obsidian
                else                  :   chunk.walls[j][i] = bedrock

            for j in range(10, 25): # Upper bedrock wastes

                obsidianProb    =   2*(25-j)/3  # Goes from 0 to 10 (0% to 10%)
                hellStoneProb   =   obsidianProb + 0.015 # Always 0.015 (0.15%)
                frontVal        =   (self.noiseGenerator.noise3d(x = absouluteIndex * BEDROCK_UPPER_X, y = j * BEDROCK_UPPER_Y, z = -1) + 1) * 5
                backVal         =   (self.noiseGenerator.noise3d(x = absouluteIndex * BEDROCK_UPPER_X, y = j * BEDROCK_UPPER_Y, z = 1) + 1) * 5

                if(0 <= frontVal < obsidianProb):
                    chunk[j][i] = obsidian
                elif(obsidianProb <= frontVal < hellStoneProb):
                    chunk[j][i] = hellstone
                else:
                    chunk[j][i] = greystone

                if(0 <= backVal < obsidianProb):
                    chunk.walls[j][i] = obsidian
                elif(obsidianProb <= backVal < hellStoneProb):
                    chunk.walls[j][i] = hellstone
                else:
                    chunk.walls[j][i] = greystone

            absouluteIndex  +=  1

    def __getitem__(self, key):
        return self.chunks[key]

    def __setitem__(self, key, value):
        self.chunks[key] = value

    def __len__(self):
        return len(self.chunks)