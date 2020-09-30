import pygame

# List of attributes (constants)
ID              =   0
HEALTH          =   1
LUMINOSITY      =   2

# Tile names along with their IDs

air             =   0

bedrock         =   1
obsidian        =   2
hellstone       =   3

unobtanium      =   4
diamondOre      =   5
platinumOre     =   6
goldOre         =   7
ironOre         =   8
copperOre       =   9

granite         =   10
quartz          =   11
limestone       =   12
greystone       =   13
sandstone       =   14

# Tile table with names
TILE_NAMES = {
    # air
    "air"           : air,

    # bedrock wastes blocks
    "bedrock"       : bedrock,
    "obsidian"      : obsidian,
    "hellstone"     : hellstone,

    # ores
    "unobtanium"    : unobtanium,
    "diamond ore"   : diamondOre,
    "platinum ore"  : platinumOre,
    "gold ore"      : goldOre,
    "iron ore"      : ironOre,
    "copper ore"    : copperOre,

    # stones
    "granite"       : granite,
    "quartz"        : quartz,
    "limestone"     : limestone,
    "stone"         : greystone,
    "sandstone"     : sandstone,

    # transition blocks
    "gravel"        : 15,
    "coke"          : 16,

    # clays
    "clay"          : 17,
    "red clay"      : 18

}

TILE_TABLE = {

    bedrock:   pygame.image.load("Resources/Default/bedrock.png"),
    obsidian:   pygame.image.load("Resources/Mock/obsidian.png"),
    hellstone:   pygame.image.load("Resources/Mock/hellstone.png"),

    greystone: pygame.image.load("Resources/Default/ironblock.png")

}