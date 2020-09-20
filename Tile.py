import pygame

TILE_WIDTH = 24

# List of attributes (constants)
HEALTH = 1
LUMINOSITY = 2

# Tile names along with their IDs


# Tile table with names
TILE_NAMES = {
    # bedrock wastes blocks
    "Bedrock" : 1,
    "Obsidian" : 2,
    "Hellstone" : 3,
    # ores
    "Unobtanium" : 4,
    "Diamond ore" : 5,
    "Platinum ore" : 6,
    "Gold ore" : 7,
    "Iron ore" : 8,
    "Copper ore" : 9,
    # stones
    "Granite" : 10,
    "Quartz" : 11,
    "Limestone" : 12,
    "Stone" : 13,
    "Sandstone" : 14,
    # transition blocks
    "Gravel" : 15,
    "Coke" : 16,
    # clays
    "Clay" : 17,
    "Red clay" : 18
}

TILE_TABLE = {
    1:pygame.image.load("Resources/Default/grass.png"),
    2:pygame.image.load("Resources/Default/dirt.png"),
    3:pygame.image.load("Resources/Default/grass.png")
}

class Tile:

    def __init__(self, texture, rect=(0,0,TILE_WIDTH,TILE_WIDTH)):
        self.rect = rect
        self.texture = pygame.image.load("Resources/Mock/"+texture)

class Grass(Tile):

    def __init__(self):
        super().__init__("grass.png")

class Stone(Tile):

    def __init__(self):
        super().__init__("stone.png")

class Bedrock(Tile):

    def __init__(self):
        super().__init__("bedrock.png")
