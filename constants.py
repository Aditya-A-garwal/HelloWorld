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
SCALE_SPEED         =  TILE_WIDTH * 12    # 6 is number of tiles to move
AIR_FRICTION        =  0.2
UP_ACC              =  0.8
DOWN_ACC            =  0.8
DEFAULT_FRICTION    =  0.5
DEFAULT_FRICTION    =  0.5
