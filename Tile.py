import pygame

TILE_WIDTH = 24

# List of attributes (constants)
HEALTH = 1
LUMINOSITY = 2

# Tile names along with their IDs

bedrock = 1
obsidian = 2
hellstone = 3

# Tile table with names
TILE_NAMES = {
    # bedrock wastes blocks
    "bedrock" : 1,
    "obsidian" : 2,
    "hellstone" : 3,
    # ores
    "unobtanium" : 4,
    "diamond ore" : 5,
    "platinum ore" : 6,
    "gold ore" : 7,
    "iron ore" : 8,
    "copper ore" : 9,
    # stones
    "granite" : 10,
    "quartz" : 11,
    "limestone" : 12,
    "stone" : 13,
    "sandstone" : 14,
    # transition blocks
    "gravel" : 15,
    "coke" : 16,
    # clays
    "clay" : 17,
    "red clay" : 18
}

TILE_TABLE = {
    1:pygame.image.load("Resources/Default/bedrock.png"),
    2:pygame.image.load("Resources/Mock/obsidian.png"),
    3:pygame.image.load("Resources/Mock/hellstone.png")
}

class Tile:

    def __init__(self, texture, rect=(0,0,TILE_WIDTH,TILE_WIDTH)):
        self.rect = rect
        self.texture = pygame.image.load("Resources/Mock/"+texture)

