import pygame

# Width of an individual tile unit (in points)
TILE_WIDTH      =   24

# Width, height of chunk (in tiles)
CHUNK_WIDTH         =   16
CHUNK_HEIGHT        =   512

# Width, height of chunk (in points)
CHUNK_HEIGHT_P      =   CHUNK_HEIGHT * TILE_WIDTH
CHUNK_WIDTH_P       =   CHUNK_WIDTH * TILE_WIDTH

# Arbitrary constant for chunk generation
WALKING_CONSTANT    =   0.0075