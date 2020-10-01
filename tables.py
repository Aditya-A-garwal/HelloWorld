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

gravel          =   15
coke            =   16

clay            =   17
redClay         =   18

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
    "gravel"        : gravel,
    "coke"          : coke,

    # clays
    "clay"          : clay,
    "red clay"      : redClay

}

TILE_TABLE = {

    bedrock     :   pygame.image.load("Resources/Default/bedrock2.png"),
    obsidian    :   pygame.image.load("Resources/Default/obsidian.png"),
    hellstone   :   pygame.image.load("Resources/Default/hellstone.png"),

    #unobtanium  :   pygame.image.load("Resources/Default/unobtainium.png"),
    diamondOre  :   pygame.image.load("Resources/Default/diamondOre.png"),
    #platinumOre :   pygame.image.load("Resources/Default/platinumOre.png"),
    goldOre     :   pygame.image.load("Resources/Default/goldOre.png"),
    ironOre     :   pygame.image.load("Resources/Default/ironOre.png"),
    copperOre   :   pygame.image.load("Resources/Default/copperOre.png"),

    granite     :   pygame.image.load("Resources/Default/granite.png"),
    quartz      :   pygame.image.load("Resources/Default/quartz.png"),
    limestone   :   pygame.image.load("Resources/Default/limestone.png"),
    greystone   :   pygame.image.load("Resources/Default/greystone.png"),
    #sandstone   :   pygame.image.load("Resources/Default/sandstone.png"),

    #gravel      :   pygame.image.load("Resources/Default/gravel.png"),
    #coke        :   pygame.image.load("Resources/Default/coke.png"),

    clay        :   pygame.image.load("Resources/Default/clay.png"),
    redClay     :   pygame.image.load("Resources/Default/redClay.png")

}