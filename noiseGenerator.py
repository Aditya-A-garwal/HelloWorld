from opensimplex import OpenSimplex
from tables import *
from constants import *

class noiseGenerator:

    def __init__(self, seed = None):

        """Initializes the noise generator

        Args:
            seed (int, optional): The seed of the noise generator. Defaults to None.
        """

        self.gen = OpenSimplex()

    def frontVal(self, x, y):

        """Returns value of (x,y) at front-plane

        Args:
            x (float): The x-coordinate of the noise plane
            y (float): The y-coordinate of the noise plane

        Returns:
            float: Value on the noise plane at (x,y), normalized between 0 and 100
        """

        return (self.gen.noise3d( x, y, 1 ) + 1) * 50

    def backVal(self, x, y):

        """Returns value of (x,y) at back-plane

        Args:
            x (float): The x-coordinate of the noise plane
            y (float): The y-coordinate of the noise plane

        Returns:
            float: Value on the noise plane at (x,y), normalized between 0 and 100
        """

        return (self.gen.noise3d( x, y, -1 ) + 1) * 50

    def getLowerBedrockWastes(self, x, y):

        front  =  self.frontVal(x * BEDROCK_LOWER_X, y * BEDROCK_LOWER_Y)
        back   =  self.backVal(x * BEDROCK_LOWER_X, y * BEDROCK_LOWER_Y)
        return front, back

    def getUpperBedrockWastes(self, x, y):

        front  =  self.frontVal(x * BEDROCK_UPPER_X, y * BEDROCK_UPPER_Y)
        back   =  self.backVal(x * BEDROCK_UPPER_X, y * BEDROCK_UPPER_Y)
        return front, back

    def getLowerCaves(self, x, y):

        front  =  self.frontVal(x * CAVE_X, y * CAVE_Y)
        back   =  self.backVal(x * CAVE_X, y * CAVE_Y)
        return front, back

    def getMiddleCaves(self, x, y):

        front  =  self.frontVal(x * CAVE_X, y * CAVE_Y)
        back   =  self.backVal(x * CAVE_X, y * CAVE_Y)
        return front, back

    def getUpperCaves(self, x, y):

        front  =  self.frontVal(x * CAVE_X, y * CAVE_Y)
        back   =  self.backVal(x * CAVE_X, y * CAVE_Y)
        return front, back

    def getLowerUnderground(self, x, y):

        front  =  self.frontVal(x * UNDERGROUND_X, y * UNDERGROUND_Y)
        back   =  self.backVal(x * UNDERGROUND_X, y * UNDERGROUND_Y)
        return front, back

    def getUpperUnderground(self, x, y):

        front  =  self.frontVal(x * UNDERGROUND_X, y * UNDERGROUND_Y)
        back   =  self.backVal(x * UNDERGROUND_X, y * UNDERGROUND_Y)
        return front, back