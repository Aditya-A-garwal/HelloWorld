from constants import *

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

ITEM_TABLE = {}

ITEM_ATTR = {
    # door:{ID:43,WEIGHT:25,FRICTION:None,LUMINOSITY:0,BREAKTIME:1,PLACEABLE:True,DAMAGE:10,HEALTH:20,INFLAMMABLE:3,LTIMPERMEABILITY:0},
    # bed:{ID:44,WEIGHT:30,FRICTION:0.4,LUMINOSITY:0,BREAKTIME:1,PLACEABLE:True,DAMAGE:10,HEALTH:30,INFLAMMABLE:3,LTIMPERMEABILITY:0},
    # bucket:{ID:45,WEIGHT:15,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    # bow:{ID:46,WEIGHT:10,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    # arrow:{ID:47,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    # pickaxe:{ID:48,WEIGHT:15,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:40,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    # battleaxe:{ID:49,WEIGHT:15,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:50,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    # axe:{ID:50,WEIGHT:15,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:40,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    # sword:{ID:51,WEIGHT:15,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:50,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    # lighter:{ID:52,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    # deerskin:{ID:53,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    # rottenleather:{ID:54,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    # chicken:{ID:55,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    # deermeat:{ID:56,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    # rottenmeat:{ID:57,WEIGHT:5,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    # berry:{ID:58,WEIGHT:2,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0},
    # apple:{ID:59,WEIGHT:2,FRICTION:None,LUMINOSITY:0,BREAKTIME:None,PLACEABLE:False,DAMAGE:10,HEALTH:None,INFLAMMABLE:None,LTIMPERMEABILITY:0}
}

def loadImageTable():
    for key in ITEM_TABLE:
        ITEM_TABLE[key] = ITEM_TABLE[key].convert_alpha()