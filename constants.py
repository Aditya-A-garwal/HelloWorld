import pygame

# Width of an individual tile unit (in points)
TILE_WIDTH      =   24

# Width, height of chunk (in tiles)
CHUNK_WIDTH         =   16
CHUNK_HEIGHT        =   512

# Width, height of chunk (in points)
CHUNK_HEIGHT_P      =   CHUNK_HEIGHT * TILE_WIDTH
CHUNK_WIDTH_P       =   CHUNK_WIDTH * TILE_WIDTH

# Constants for chunk generation
BEDROCK_LOWER_X     =   0.1
BEDROCK_LOWER_Y     =   0.2

BEDROCK_UPPER_X     =   0.1
BEDROCK_UPPER_Y     =   0.2