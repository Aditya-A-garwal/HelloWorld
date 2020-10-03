import pygame

# List of attributes (constants)
ID              =   0
HEALTH          =   1
LUMINOSITY      =   2
WEIGHT               =   3
FRICTION             =   4
BREAKTIME            =   5
PLACEABLE            =   6
DAMAGE               =   7
INFLAMMABLE          =   8
LIGHTPERMEABILITY    =   9
ILLUMINATION         =   10


# Tile names along with their IDs

air             =   0

bedrock         =   1
obsidian        =   2
hellstone       =   3

unobtaniumOre   =   4
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

brownClay       =   17
redClay         =   18
sand            =   19
browndirt       =   20
grass           =   21
snowygrass      =   22
snow            =   23
ice             =   24
glass           =   25
junglewood      =   26
oakwood         =   27
borealwood      =   28
pinewood        =   29
cactuswood      =   30
palmwood        =   31
cosmonium       =   32
adamantite      =   33
unobtaniumblock =   34
diamondblock    =   35
platinumblock   =   36
goldblock       =   37
ironblock       =   38
copperblock     =   39

water           =   40
lava            =   41

torch           =   42
door            =   43
bed             =   44
bucket          =   45

bow             =   46
arrow           =   47
pickaxe         =   48
battleaxe       =   49
axe             =   50
sword           =   51
lighter         =   52

deerskin        =   53
rottenleather   =   54

chicken         =   55
deermeat        =   56
rottenmeat      =   57

berry           =   58
apple           =   59
brownDirt       =   19

# Tile table with names
TILE_NAMES = {

    # air
    air            : "air",

    # bedrock wastes blocks
    bedrock        : "bedrock",
    obsidian       : "obsidian",
    hellstone      : "hellstone",

    # ores
    unobtaniumOre   : "unobtanium",
    diamondOre      : "diamond ore",
    platinumOre     : "platinum ore",
    goldOre         : "gold ore",
    ironOre         : "iron ore",
    copperOre       : "copper ore",


    # stones
    granite        : "granite",
    quartz         : "quartz",
    limestone      : "limestone",
    greystone      : "stone",
    sandstone      : "sandstone",

    # transition blocks
    gravel         : "gravel",
    coke           : "coke",

    # clays
    brownClay      : "clay",
    redClay        : "red clay",
    sand           : "sand",
    browndirt      : "dirt",
    grass          : "grass",
    snowygrass     : "snowy grass",
    snow           : "snow",
    ice            : "ice",
    glass          : "glass",
    junglewood     : "jungle wood",
    oakwood        : "oak wood",
    borealwood     : "boreal wood",
    pinewood       : "pine wood",
    cactuswood     : "cactus",
    palmwood       : "palm wood",
    cosmonium      : "cosmonium",
    adamantite     : "adamantite",
    unobtaniumblock: "unobtanium block",
    diamondblock   : "diamond block",
    platinumblock  : "platinum block",
    goldblock      : "gold block",
    ironblock      : "iron block",
    copperblock    : "copper block",
    water          : "water",
    lava           : "lave",
    torch          : "torch",
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

    brownClay        :   pygame.image.load("Resources/Default/clay.png"),
    redClay         :   pygame.image.load("Resources/Default/redClay.png"),
    brownDirt       :   pygame.image.load("Resources/Default/brownDirt.png")
}
LIGHT_TABLE = {


}

def loadImageTable():
    for key in TILE_TABLE:
        TILE_TABLE[key] = TILE_TABLE[key].convert_alpha()
TILE_ATTR={
    bedrock:{ID:1,WEIGHT:100,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:None,HEALTH:10**10,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    obsidian:{ID:2,WEIGHT:99,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:10,PLACEABLE:True,DAMAGE:10,HEALTH:100,INFLAMMABLE:0,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    hellstone:{ID:3,WEIGHT:99,FRICTION:0.4,LUMINOSITY:150,BREAKTIME:10,PLACEABLE:True,DAMAGE:10,HEALTH:100,INFLAMMABLE:0,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    unobtaniumOre:{ID:4,WEIGHT:85,FRICTION:0.7,LUMINOSITY:0,BREAKTIME:8,PLACEABLE:True,DAMAGE:10,HEALTH:90,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    diamondOre:{ID:5,WEIGHT:80,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:7,PLACEABLE:True,DAMAGE:10,HEALTH:90,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    platinumOre:{ID:6,WEIGHT:75,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:7,PLACEABLE:True,DAMAGE:10,HEALTH:80,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    goldOre:{ID:7,WEIGHT:70,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:5,PLACEABLE:True,DAMAGE:10,HEALTH:70,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    ironOre:{ID:8,WEIGHT:65,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:3,PLACEABLE:True,DAMAGE:10,HEALTH:70,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    granite:{ID:9,WEIGHT:60,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:55,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    quartz:{ID:10,WEIGHT:60,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:55,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    limestone:{ID:11,WEIGHT:55,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:55,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    copperOre:{ID:12,WEIGHT:65,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:3,PLACEABLE:True,DAMAGE:10,HEALTH:60,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    greystone:{ID:13,WEIGHT:55,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:55,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    sandstone:{ID:14,WEIGHT:50,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:50,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    gravel:{ID:15,WEIGHT:45,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:50,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    coke:{ID:16,WEIGHT:40,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:50,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    brownClay:{ID:17,WEIGHT:35,FRICTION:0.7,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:45,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    redClay:{ID:18,WEIGHT:35,FRICTION:0.7,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:45,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    sand:{ID:19,WEIGHT:20,FRICTION:0.6,LUMINOSITY:0,BREAKTIME:1,PLACEABLE:True,DAMAGE:10,HEALTH:15,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    browndirt:{ID:20,WEIGHT:25,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:30,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    grass:{ID:21,WEIGHT:25,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:30,INFLAMMABLE:3,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    snowygrass:{ID:22,WEIGHT:30,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:30,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    snow:{ID:23,WEIGHT:30,FRICTION:0.6,LUMINOSITY:0,BREAKTIME:1,PLACEABLE:True,DAMAGE:10,HEALTH:15,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    ice:{ID:24,WEIGHT:25,FRICTION:0.2,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:30,INFLAMMABLE:None,LIGHTPERMEABILITY:150,ILLUMINATION:0},
    glass:{ID:25,WEIGHT:30,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:30,INFLAMMABLE:None,LIGHTPERMEABILITY:200,ILLUMINATION:0},
    junglewood:{ID:26,WEIGHT:35,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:35,INFLAMMABLE:4,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    oakwood:{ID:27,WEIGHT:35,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:35,INFLAMMABLE:4,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    borealwood:{ID:28,WEIGHT:35,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:35,INFLAMMABLE:4,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    pinewood:{ID:29,WEIGHT:35,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:35,INFLAMMABLE:4,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    cactuswood:{ID:30,WEIGHT:35,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:35,INFLAMMABLE:4,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    palmwood:{ID:31,WEIGHT:35,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:2,PLACEABLE:True,DAMAGE:10,HEALTH:35,INFLAMMABLE:4,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    cosmonium:{ID:32,WEIGHT:90,FRICTION:0.4,LUMINOSITY:150,BREAKTIME:8,PLACEABLE:True,DAMAGE:10,HEALTH:85,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    adamantite:{ID:33,WEIGHT:90,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:8,PLACEABLE:True,DAMAGE:85,HEALTH:85,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    unobtaniumblock:{ID:34,WEIGHT:85,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:8,PLACEABLE:True,DAMAGE:10,HEALTH:80,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    diamondblock:{ID:35,WEIGHT:80,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:7,PLACEABLE:True,DAMAGE:10,HEALTH:80,INFLAMMABLE:None,LIGHTPERMEABILITY:150,ILLUMINATION:0},
    platinumblock:{ID:36,WEIGHT:75,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:7,PLACEABLE:True,DAMAGE:10,HEALTH:70,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    goldblock:{ID:37,WEIGHT:70,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:6,PLACEABLE:True,DAMAGE:10,HEALTH:65,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    ironblock:{ID:38,WEIGHT:70,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:6,PLACEABLE:True,DAMAGE:10,HEALTH:65,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    copperblock:{ID:39,WEIGHT:65,FRICTION:0.3,LUMINOSITY:0,BREAKTIME:5,PLACEABLE:True,DAMAGE:10,HEALTH:60,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    water:{ID:40,WEIGHT:35,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:True,DAMAGE:None,HEALTH:None,INFLAMMABLE:None,LIGHTPERMEABILITY:150,ILLUMINATION:0},
    lava:{ID:41,WEIGHT:40,FRICTION:None,LUMINOSITY:150,BREAKTIME:None,PLACEABLE:True,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    torch:{ID:42,WEIGHT:20,FRICTION:None,LUMINOSITY:200,BREAKTIME:1,PLACEABLE:True,DAMAGE:10,HEALTH:15,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    door:{ID:43,WEIGHT:25,FRICTION:None,LUMINOSITY:0,BREAKTIME:1,PLACEABLE:True,DAMAGE:10,HEALTH:20,INFLAMMABLE:3,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    bed:{ID:44,WEIGHT:30,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:1,PLACEABLE:True,DAMAGE:10,HEALTH:30,INFLAMMABLE:3,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    bucket:{ID:45,WEIGHT:15,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    bow:{ID:46,WEIGHT:10,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    arrow:{ID:47,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    pickaxe:{ID:48,WEIGHT:15,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:40,HEALTH:None,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    battleaxe:{ID:49,WEIGHT:15,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:50,HEALTH:None,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    axe:{ID:50,WEIGHT:15,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:40,HEALTH:None,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    sword:{ID:51,WEIGHT:15,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:50,HEALTH:None,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    lighter:{ID:52,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    deerskin:{ID:53,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    rottenleather:{ID:54,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    chicken:{ID:55,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    deermeat:{ID:56,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    rottenmeat:{ID:57,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    berry:{ID:58,WEIGHT:2,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0},
    apple:{ID:59,WEIGHT:2,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LIGHTPERMEABILITY:0,ILLUMINATION:0}

}

