from constants import *

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

junglewood     =  25
oakwood        =  26
borealwood     =  27
pinewood       =  28
cactuswood     =  29
palmwood       =  30

cosmonium  =  31
adamantite =  32
unobtanium =  33
diamond    =  34
platinum   =  35
gold       =  36
iron       =  37
copper     =  38

glass           =  39
glasswindow     =  40

torch           =  41

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
    junglewood    : "jungle logs",
    oakwood       : "oak logs",
    borealwood    : "boreal logs",
    pinewood      : "pine logs",
    cactuswood    : "cactus",
    palmwood      : "palm logs",

    # mineral blocks
    cosmonium : "block of cosmonium",
    adamantite: "block of adamantite",
    unobtanium: "unobtanium block",
    diamond   : "diamond block",
    platinum  : "platinum block",
    gold      : "gold block",
    iron      : "iron block",
    copper    : "copper block",

    glass          : "block of glass",
    glasswindow    : "glass window",

    torch          : "torch",

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
    browndirt       :   pygame.image.load("Resources/Default/browndirt.png"),
}

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
    cosmonium:{ID:32,WEIGHT:90,FRICTION:0.4,LUMINOSITY:150,BREAKTIME:8,PLACEABLE:True,DAMAGE:10,HEALTH:85,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    adamantite:{ID:33,WEIGHT:90,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:8,PLACEABLE:True,DAMAGE:85,HEALTH:85,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    unobtanium:{ID:34,WEIGHT:85,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:8,PLACEABLE:True,DAMAGE:10,HEALTH:80,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    diamond:{ID:35,WEIGHT:80,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:7,PLACEABLE:True,DAMAGE:10,HEALTH:80,INFLAMMABLE:None,LTIMPERMEABILITY:150},
    platinum:{ID:36,WEIGHT:75,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:7,PLACEABLE:True,DAMAGE:10,HEALTH:70,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    gold:{ID:37,WEIGHT:70,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:6,PLACEABLE:True,DAMAGE:10,HEALTH:65,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    iron:{ID:38,WEIGHT:70,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:6,PLACEABLE:True,DAMAGE:10,HEALTH:65,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    copper:{ID:39,WEIGHT:65,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:5,PLACEABLE:True,DAMAGE:10,HEALTH:60,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    torch:{ID:42,WEIGHT:20,FRICTION:None,LUMINOSITY:200,BREAKTIME:1,PLACEABLE:True,DAMAGE:10,HEALTH:15,INFLAMMABLE:None,LTIMPERMEABILITY:0},
}

def loadImageTable():
    for key in TILE_TABLE:
        TILE_TABLE[key] = TILE_TABLE[key].convert_alpha()