import pygame

# Tile table with names
TILE_NAMES = {
    # air
    "air"           : 0,

    # bedrock wastes blocks
    "bedrock"       : 1,
    "obsidian"      : 2,
    "hellstone"     : 3,

    # ores
    "unobtanium"    : 4,
    "diamond ore"   : 5,
    "platinum ore"  : 6,
    "gold ore"      : 7,
    "iron ore"      : 8,
    "copper ore"    : 9,

    # stones
    "granite"       : 10,
    "quartz"        : 11,
    "limestone"     : 12,
    "stone"         : 13,
    "sandstone"     : 14,

    # transition blocks
    "gravel"        : 15,
    "coke"          : 16,

    # clays
    "clay"          : 17,
    "red clay"      : 18

}

TILE_TABLE = {

    1:   pygame.image.load("Resources/Default/bedrock.png"),
    2:   pygame.image.load("Resources/Mock/obsidian.png"),
    3:   pygame.image.load("Resources/Mock/hellstone.png")
}