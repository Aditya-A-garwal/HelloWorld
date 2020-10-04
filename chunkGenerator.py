#from noiseModules import RidgedMulti, Voronoi, OpenSimplex
from opensimplex import OpenSimplex
from tables import *
from constants import *

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