import pyglet

TILE_WIDTH = 24
texturePack = "Default"

class Tile:

    def __init__(self, texture, rect=(0,0,TILE_WIDTH,TILE_WIDTH)):
        self.rect = rect
        self.texture = pyglet.image.load("Resources/Mock/"+texture) #.get_region(rect[0], rect[1], rect[2], rect[3])

class Grass(Tile):

    def __init__(self):
        super().__init__("grass.png")

class Stone(Tile):

    def __init__(self):
        super().__init__("stone.png")

class Bedrock(Tile):

    def __init__(self):
        super().__init__("bedrock.png")


TILE_NAMES = {1: "dirt", 2: "grass", 3: "sand"}
TILE_TABLE = {}

for key in TILE_NAMES.keys(): TILE_TABLE[key] = pyglet.image.load("Resources/" + texturePack + "/" + TILE_NAMES[key] + ".png")