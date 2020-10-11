import pygame

# Width of an individual tile unit (in points)
TILE_WIDTH          =  24

# Width, height of chunk (in tiles)
CHUNK_WIDTH         =  16
CHUNK_HEIGHT        =  512

# Width, height of chunk (in points)
CHUNK_HEIGHT_P      =  CHUNK_HEIGHT * TILE_WIDTH
CHUNK_WIDTH_P       =  CHUNK_WIDTH * TILE_WIDTH

# Constants for chunk generation
BEDROCK_LOWER_X     =  0.1
BEDROCK_LOWER_Y     =  0.2

BEDROCK_UPPER_X     =  0.1
BEDROCK_UPPER_Y     =  0.2

CAVE_X              =  0.05
CAVE_Y              =  0.1

UNDERGROUND_X       =  0.05
UNDERGROUND_Y       =  0.1

## Constants for entity and physics (time_unit = seconds, length_unit = points)
GRAVITY_ACC         =  9.8
SCALE_VEL           =  TILE_WIDTH * 12    # 6 is number of tiles to move
AIR_FRICTION        =  0.2
UP_ACC              =  0.8
DOWN_ACC            =  0.8
DEFAULT_FRICTION    =  0.5
MAX_ACC             =  1
MAX_VEL             =  1


# List of attributes (constants)

# Tiles, items, entities
ID                  = 0

# Tiles
LUMINOSITY          = 1
FRICTION            = 2
BREAKTIME           = 3
HEALTH              = 4
INFLAMMABLE         = 5
LTIMPERMEABILITY    = 6
DROPS               = 7

# items
PLACEABLE           = 8
PLACES              = 9
DAMAGE              = 10

# entities
WEIGHT              = 11


# Tile names along with their IDs

air             =  0

bedrock         =  1
obsidian        =  2
hellstone       =  3

unobtaniumOre   =  4
diamondOre      =  5
platinumOre     =  6
goldOre         =  7
ironOre         =  8
copperOre       =  9

granite         =  10
quartz          =  11
limestone       =  12
greystone       =  13
sandstone       =  14

gravel          =  15
coke            =  16

clay            =  17
redClay         =  18
sand            =  19
browndirt       =  20
grass           =  21
snowygrass      =  22

snow            =  23
ice             =  24

jungleblock     =  25
oakblock        =  26
borealblock     =  27
pineblock       =  28
cactusblock     =  29
palmblock       =  30

cosmoniumblock  =  31
adamantiteblock =  32
unobtaniumblock =  33
diamondblock    =  34
platinumblock   =  35
goldblock       =  36
ironblock       =  37
copperblock     =  38

glass           =  39
glasswindow     =  40

torch           =  41

# Item names along with their IDs

berry           =  1
apple           =  2

junglewood      =  3
oakwood         =  4
borealwood      =  5
pinewood        =  6
cactuswood      =  7
palmwood        =  8

bow             =  46
arrow           =  47

pickaxe         =  48
axe             =  50
battleaxe       =  49
sword           =  51
lighter         =  52

deerskin        =  53
rottenleather   =  54

chicken         =  55
deermeat        =  56
rottenmeat      =  57

door            =  43
bed             =  44
bucket          =  45

# Tile table with names
TILE_NAMES = {

    # air
    air            : "air",

    # bedrock wastes blocks
    bedrock        : "bedrock",
    obsidian       : "block of obsidian",
    hellstone      : "block of hellstone",

    # ores
    unobtaniumOre   : "unrefined unobtanium",
    diamondOre      : "diamond ore",
    platinumOre     : "platinum ore",
    goldOre         : "gold ore",
    ironOre         : "iron ore",
    copperOre       : "copper ore",


    # stones
    granite        : "block of granite",
    quartz         : "block of quartz",
    limestone      : "block of limestone",
    greystone      : "block of stone",
    sandstone      : "block of sandstone",

    # transition blocks
    gravel         : "block of gravel",
    coke           : "block of coke",

    # clays
    clay           : "block of clay",
    redClay        : "block of red clay",

    # sand
    sand           : "block of sand",

    # dirt, grass
    browndirt      : "block of dirt",
    grass          : "block of grass",

    #Snowy blocks
    snowygrass     : "block of snowy grass",
    snow           : "block of snow",
    ice            : "block of ice",

    # woods
    jungleblock    : "jungle logs",
    oakblock       : "oak logs",
    borealblock    : "boreal logs",
    pineblock      : "pine logs",
    cactusblock    : "cactus",
    palmblock      : "palm logs",

    # mineral blocks
    cosmoniumblock : "block of cosmonium",
    adamantiteblock: "block of adamantite",
    unobtaniumblock: "unobtanium block",
    diamondblock   : "diamond block",
    platinumblock  : "platinum block",
    goldblock      : "gold block",
    ironblock      : "iron block",
    copperblock    : "copper block",

    glass          : "block of glass",
    glasswindow    : "glass window",

    torch          : "torch",

}

ITEM_NAMES = {
    door           : "door",
    bed            : "bed",
    bucket         : "bucket",
    bow            : "bow",
    arrow          : "arrow",
    pickaxe        : "pickaxe",
    battleaxe      : "battle axe",
    axe            : "axe",
    sword          : "sword",
    lighter        : "lighter",
    deerskin       : "deer skin",
    rottenleather  : "rotten leather",
    chicken        : "chicken",
    deermeat       : "deer meat",
    rottenmeat     : "rotten meat",
    berry          : "berry",
    apple          : "apple"
}

TILE_TABLE = {

    bedrock         :   pygame.image.load("Resources/Default/bedrock2.png"),
    obsidian        :   pygame.image.load("Resources/Default/obsidian.png"),
    hellstone       :   pygame.image.load("Resources/Default/hellstone.png"),

    unobtaniumOre   :   pygame.image.load("Resources/Default/unobtaniumOre.png"),
    diamondOre      :   pygame.image.load("Resources/Default/diamondOre.png"),
    platinumOre     :   pygame.image.load("Resources/Default/ironOre.png"),
    goldOre         :   pygame.image.load("Resources/Default/goldOre.png"),
    ironOre         :   pygame.image.load("Resources/Default/ironOre.png"),
    copperOre       :   pygame.image.load("Resources/Default/copperOre.png"),

    granite         :   pygame.image.load("Resources/Default/granite.png"),
    quartz          :   pygame.image.load("Resources/Default/quartz.png"),
    limestone       :   pygame.image.load("Resources/Default/limestone.png"),
    greystone       :   pygame.image.load("Resources/Default/greystone.png"),
    sandstone       :   pygame.image.load("Resources/Default/sandstone.png"),

    gravel          :   pygame.image.load("Resources/Default/gravel.png"),
    coke            :   pygame.image.load("Resources/Default/coalOre.png"),

    clay            :   pygame.image.load("Resources/Default/clay.png"),
    redClay         :   pygame.image.load("Resources/Default/redClay.png"),
}

ITEM_TABLE = {}

TILE_ATTR={
    air:{LUMINOSITY:255},
    bedrock:{ID:1,WEIGHT:100,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:None,HEALTH:10**10,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    obsidian:{ID:2,WEIGHT:99,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:10,PLACEABLE:True,DAMAGE:10,HEALTH:100,INFLAMMABLE:0,LTIMPERMEABILITY:0},
    hellstone:{ID:3,WEIGHT:99,FRICTION:0.4,LUMINOSITY:255,BREAKTIME:10,PLACEABLE:True,DAMAGE:10,HEALTH:100,INFLAMMABLE:0,LTIMPERMEABILITY:0},
    unobtaniumOre:{ID:4,WEIGHT:85,FRICTION:0.7,LUMINOSITY:160,BREAKTIME:8,PLACEABLE:True,DAMAGE:10,HEALTH:90,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    diamondOre:{ID:5,WEIGHT:80,FRICTION:0.4,LUMINOSITY:175,BREAKTIME:7,PLACEABLE:True,DAMAGE:10,HEALTH:90,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    platinumOre:{ID:6,WEIGHT:75,FRICTION:0.4,LUMINOSITY:160,BREAKTIME:7,PLACEABLE:True,DAMAGE:10,HEALTH:80,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    goldOre:{ID:7,WEIGHT:70,FRICTION:0.4,LUMINOSITY:160,BREAKTIME:5,PLACEABLE:True,DAMAGE:10,HEALTH:70,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    ironOre:{ID:8,WEIGHT:65,FRICTION:0.4,LUMINOSITY:160,BREAKTIME:3,PLACEABLE:True,DAMAGE:10,HEALTH:70,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    granite:{ID:9,WEIGHT:60,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:55,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    quartz:{ID:10,WEIGHT:60,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:55,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    limestone:{ID:11,WEIGHT:55,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:55,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    copperOre:{ID:12,WEIGHT:65,FRICTION:0.4,LUMINOSITY:160,BREAKTIME:3,PLACEABLE:True,DAMAGE:10,HEALTH:60,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    greystone:{ID:13,WEIGHT:55,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:55,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    sandstone:{ID:14,WEIGHT:50,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:50,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    gravel:{ID:15,WEIGHT:45,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:50,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    coke:{ID:16,WEIGHT:40,FRICTION:0.4,LUMINOSITY:160,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:50,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    clay:{ID:17,WEIGHT:35,FRICTION:0.7,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:45,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    redClay:{ID:18,WEIGHT:35,FRICTION:0.7,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:45,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    sand:{ID:19,WEIGHT:20,FRICTION:0.6,LUMINOSITY:0,BREAKTIME:1,PLACEABLE:True,DAMAGE:10,HEALTH:15,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    browndirt:{ID:20,WEIGHT:25,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:30,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    grass:{ID:21,WEIGHT:25,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:30,INFLAMMABLE:3,LTIMPERMEABILITY:0},
    snowygrass:{ID:22,WEIGHT:30,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:30,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    snow:{ID:23,WEIGHT:30,FRICTION:0.6,LUMINOSITY:0,BREAKTIME:1,PLACEABLE:True,DAMAGE:10,HEALTH:15,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    ice:{ID:24,WEIGHT:25,FRICTION:0.2,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:30,INFLAMMABLE:None,LTIMPERMEABILITY:150},
    glass:{ID:25,WEIGHT:30,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:30,INFLAMMABLE:None,LTIMPERMEABILITY:200},
    junglewood:{ID:26,WEIGHT:35,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:35,INFLAMMABLE:4,LTIMPERMEABILITY:0},
    oakwood:{ID:27,WEIGHT:35,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:35,INFLAMMABLE:4,LTIMPERMEABILITY:0},
    borealwood:{ID:28,WEIGHT:35,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:35,INFLAMMABLE:4,LTIMPERMEABILITY:0},
    pinewood:{ID:29,WEIGHT:35,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:35,INFLAMMABLE:4,LTIMPERMEABILITY:0},
    cactuswood:{ID:30,WEIGHT:35,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:35,INFLAMMABLE:4,LTIMPERMEABILITY:0},
    palmwood:{ID:31,WEIGHT:35,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:35,INFLAMMABLE:4,LTIMPERMEABILITY:0},
    cosmoniumblock:{ID:32,WEIGHT:90,FRICTION:0.4,LUMINOSITY:150,BREAKTIME:8,PLACEABLE:True,DAMAGE:10,HEALTH:85,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    adamantiteblock:{ID:33,WEIGHT:90,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:8,PLACEABLE:True,DAMAGE:85,HEALTH:85,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    unobtaniumblock:{ID:34,WEIGHT:85,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:8,PLACEABLE:True,DAMAGE:10,HEALTH:80,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    diamondblock:{ID:35,WEIGHT:80,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:7,PLACEABLE:True,DAMAGE:10,HEALTH:80,INFLAMMABLE:None,LTIMPERMEABILITY:150},
    platinumblock:{ID:36,WEIGHT:75,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:7,PLACEABLE:True,DAMAGE:10,HEALTH:70,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    goldblock:{ID:37,WEIGHT:70,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:6,PLACEABLE:True,DAMAGE:10,HEALTH:65,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    ironblock:{ID:38,WEIGHT:70,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:6,PLACEABLE:True,DAMAGE:10,HEALTH:65,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    copperblock:{ID:39,WEIGHT:65,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:5,PLACEABLE:True,DAMAGE:10,HEALTH:60,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    torch:{ID:42,WEIGHT:20,FRICTION:None,LUMINOSITY:200,BREAKTIME:1,PLACEABLE:True,DAMAGE:10,HEALTH:15,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    door:{ID:43,WEIGHT:25,FRICTION:None,LUMINOSITY:0,BREAKTIME:1,PLACEABLE:True,DAMAGE:10,HEALTH:20,INFLAMMABLE:3,LTIMPERMEABILITY:0},
    bed:{ID:44,WEIGHT:30,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:1,PLACEABLE:True,DAMAGE:10,HEALTH:30,INFLAMMABLE:3,LTIMPERMEABILITY:0},
    bucket:{ID:45,WEIGHT:15,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    bow:{ID:46,WEIGHT:10,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    arrow:{ID:47,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    pickaxe:{ID:48,WEIGHT:15,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:40,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    battleaxe:{ID:49,WEIGHT:15,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:50,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    axe:{ID:50,WEIGHT:15,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:40,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    sword:{ID:51,WEIGHT:15,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:50,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    lighter:{ID:52,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    deerskin:{ID:53,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    rottenleather:{ID:54,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    chicken:{ID:55,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    deermeat:{ID:56,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    rottenmeat:{ID:57,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    berry:{ID:58,WEIGHT:2,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    apple:{ID:59,WEIGHT:2,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0}

}

ITEM_ATTR = {}

def loadImageTable():
    for key in TILE_TABLE:
        TILE_TABLE[key] = TILE_TABLE[key].convert_alpha()
    for key in ITEM_TABLE:
        ITEM_TABLE[key] = ITEM_TABLE[key].convert_alpha()