import pickle
from Tile import *

# Constants for chunk width and chunk height (in tiles)
CHUNK_WIDTH         =   16
CHUNK_HEIGHT        =   512

# Constants for world height, world-chunk width
WORLD_HEIGHT        =   CHUNK_HEIGHT * TILE_WIDTH
WORLD_CHUNK_WIDTH   =   CHUNK_WIDTH * TILE_WIDTH

# Arbitrary constant for chunk generation
WALKING_CONSTANT    =   0.0075

class Chunk:

    def __init__(self, index = 0, noiseObj = None):

        self.index      =   index
        self.blocks     =   [[i%3 for i in range(0,   CHUNK_WIDTH)] for i in range(0, CHUNK_HEIGHT)]       
        self.walls      =   self.blocks.copy()

        # if(noiseObj is not None):
        #     Chunk.populateChunk(self, noiseObj)

    def __getitem__(self, key):        
        return self.blocks[key[0]][key[1]]

    def __setitem__(self, key, value):
        self.blocks[key[0]][key[1]] = value

    @classmethod
    def populateChunk(cls, chunk, noiseObj):

        absouluteIndex  =   chunk.index * CHUNK_WIDTH

        for i in range(0, CHUNK_WIDTH):
            # Loops for bedrock wastes
            for j in range(0, CHUNK_HEIGHT): # Lower bedrock wastes
                bedrockProbability = (10-j)*10                
                frontVal    =   (noiseObj.noise3d(x = absouluteIndex, y = j, z = 0) + 1) * 50
                backVal     =   (noiseObj.noise3d(x = absouluteIndex, y = j, z = 1) + 1) * 50

                if(0 <= frontVal <= bedrockProbability) :   chunk[j, i]         =   bedrock
                else                                    :   chunk[j, i]         =   obsidian

                if(0 <= backVal <= bedrockProbability)  :   chunk.walls[j][i]   =   bedrock
                else                                    :   chunk.walls[j][i]   =   obsidian

            absouluteIndex  +=  1


class ChunkBuffer:

    def __init__(self, length, serializer, middleIndex, noise):

        self.serializer     =   serializer             
        self.noise          =   noise

        self.len            =   length-1
        self.middleIndex    =   middleIndex
        self.leftIndex      =   int(self.middleIndex - self.len * 0.5)
        self.rightIndex     =   int(self.middleIndex + self.len * 0.5)

        self.chunks         =   []
        self.surfaces       =   []

        for i in range(self.leftIndex,  self.rightIndex + 1):

            retrieved           =   self.serializer[i]
            retrieved           =   Chunk(index = i, noiseObj = self.noise) if(retrieved is None) else pickle.loads(retrieved)

            self.chunks.append(retrieved)          
            self.surfaces.append(pygame.Surface((WORLD_CHUNK_WIDTH, WORLD_HEIGHT)))

    def shiftLeft(self):                    
        
        self.serializer[self.leftIndex-1]   =   pickle.dumps(self.chunks[0]) # move leftmost chunk into serializer
        self.leftIndex += 1

        for i in range(0, self.len):
            self.chunks[i]      =   self.chunks[i+1] # move all chunks one space left        

        self.middleIndex        +=  1

        self.chunks[self.len]   =   self.serializer[self.rightIndex+1] # take next left chunks from serializer and move into buffer
        self.rightIndex         +=  1

        self.chunks[self.len]   =   Chunk(index=self.rightIndex, noiseObj=self.noise) if(self.chunks[self.len] is None) else pickle.loads(self.chunks[self.len])

    def shiftRight(self):              

        self.serializer[self.rightIndex+1] = pickle.dumps(self.chunks[self.len]) # move rightmost chunk into serializer
        self.rightIndex -= 1

        for i in range(self.len, 0, -1): self.chunks[i] = self.chunks[i-1] # move all chunks one space right
        self.middleIndex -= 1

        self.chunks[0] = self.serializer[self.leftIndex-1] # take next left chunks from serializer and move into buffer        
        self.leftIndex -= 1

        self.chunks[0] = Chunk(index=self.leftIndex, noiseObj=self.noise) if(self.chunks[0] is None) else pickle.loads(self.chunks[0])        

    def saveComplete(self):
        for chunk in self.chunks:
            self.serializer[chunk.index] = pickle.dumps(chunk)

    def __getitem__(self, key):
        return self.chunks[key]

    def __setitem__(self, key, value):
        self.chunks[key] = value

    def __len__(self):
        return len(self.chunks)