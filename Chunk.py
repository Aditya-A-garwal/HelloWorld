import pickle
from Tile import *

# constants for chunk width and chunk height
CHUNK_WIDTH = 16
CHUNK_HEIGHT = 512

# constant for chunk generation
WALKING_CONSTANT = 0.0075

class Chunk:

    def __init__(self, index=0):
        self.index = index
        self.blocks = [[0 for i in range(0, CHUNK_WIDTH)] for i in range(0, CHUNK_HEIGHT)]       
        self.walls = self.blocks.copy()

    def __getitem__(self, key):
        return self.blocks[key[0]][key[1]]

    def __setitem__(self, key, value):
        self.blocks[key[0]][key[1]] = value

    @classmethod
    def populateChunk(cls, chunk, noiseObj, chunkInd):

        absouluteIndex = chunkInd * CHUNK_WIDTH

        for i in range(0, CHUNK_WIDTH):
            # Loops for bedrock wastes
            for j in range(0, 11): # Lower bedrock wastes
                bedrockProbability = (10-j)*10                
                frontVal = (noiseObj.noise3d(x=absouluteIndex, y = j, z = 0)+1)*50
                backVal = (noiseObj.noise3d(x=absouluteIndex, y = j, z = 1)+1)*50

                if(0 <= frontVal <= bedrockProbability): chunk[j, i] = bedrock
                else : chunk[j, i] = obsidian

                if(0 <= backVal <= bedrockProbability): chunk.walls[j][i] = bedrock
                else : chunk.walls[j][i] = obsidian

            absouluteIndex += 1


class ChunkBuffer:

    def __init__(self, length, serializer, currChunk, noise):

        self.serializer = serializer        

        self.chunks = []
        self.positions = []

        self.noise = noise

        self.len = length-1

        startVal = currChunk - (length - 1) * 0.5
        endVal = currChunk + (length - 1) * 0.5

        for i in range(int(startVal), int(endVal) + 1):
            self.positions.append(i)
            retrieved = self.serializer[i]
            if(retrieved is None):
                retrieved = Chunk(index=i)
                Chunk.populateChunk(retrieved, self.noise, i)
            else:
                retrieved = pickle.loads(retrieved)

            self.chunks.append(retrieved)

    def shiftLeft(self):

        self.serializer[self.positions[0]-1] = pickle.dumps(self.chunks[0]) # move leftmost chunk into serializer
        for i in range(0, len(self.chunks)-1): self.chunks[i] = self.chunks[i+1] # move all chunks one space left
        self.chunks[self.len] = self.serializer[self.positions[self.len]+1] # take next right chunk from serializer and move into buffer

        if(self.chunks[self.len] is None):
            self.chunks[self.len] = Chunk(index = self.positions[self.len]+1)
            Chunk.populateChunk(self.chunks[self.len], self.noise, self.positions[self.len]+1)
        else:
            self.chunks[self.len] = pickle.loads(self.chunks[self.len])

        for i in range(0, len(self.positions)): self.positions[i] += 1


    def shiftRight(self):

        self.serializer[self.positions[self.len]+1] = pickle.dumps(self.chunks[self.len]) # move rightmost chunk into serializer
        for i in range(len(self.chunks)-1, 0, -1): self.chunks[i] = self.chunks[i-1] # move all chunks one space right
        self.chunks[0] = self.serializer[self.positions[0]-1] # take next left chunks from serializer and move into buffer

        if(self.chunks[0] is None):
            self.chunks[0] = Chunk(index = self.positions[0]-1)
            Chunk.populateChunk(self.chunks[0], self.noise, self.positions[0]-1)
        else:
            self.chunks[0] = pickle.loads(self.chunks[0])

        for i in range(0, len(self.positions)): self.positions[i] -= 1

    def saveComplete(self):
        for i in range(0, len(self.positions)):
            self.serializer[self.positions[i]] = pickle.dumps(self.chunks[i])

    def __getitem__(self, key):
        return self.chunks[key]

    def __setitem__(self, key, value):
        self.chunks[key] = value

    def __len__(self):
        return len(self.chunks)