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


ITEM_ATTR = {}

def loadImageTable():
    for key in ITEM_TABLE:
        ITEM_TABLE[key] = ITEM_TABLE[key].convert_alpha()