import pygame

TILE_WIDTH = 16

class Tile:

    def __init__(self, texture, rect=(0,0,TILE_WIDTH,TILE_WIDTH)):
        self.rect = rect
        self.texture = pygame.image.load("Resources/Mock/"+texture)

class Grass(Tile):

    def __init__(self):
        super().__init__("grass.png")

class Stone(Tile):

    def __init__(self):
        super().__init__("stone.png")

class Bedrock(Tile):

    def __init__(self):
        super().__init__("bedrock.png")

TILE_TABLE = {1:Grass(), 2:Stone(), 3:Bedrock()}