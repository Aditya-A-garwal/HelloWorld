import pygame, numpy, sys, random, pickle
from pygame.locals import *
from opensimplex import OpenSimplex

from Tile import *
from Chunk import *
from Renderer import *

from databaseIO import *

# Screen variables
displaySize = [0,0]
prevFramerate = framerate = 0

# Camera variables
cam = [0,CHUNK_HEIGHT*16/2]

# Player variables
player = [0,CHUNK_HEIGHT*TILE_WIDTH*0.5]
playerInc = [0,0]
speed = currChunk = prevChunk = deltaChunk = 0
movementDict = [{pygame.K_a: -1, pygame.K_d: 1}, {pygame.K_w: 1, pygame.K_s: -1}]

#Create noise object
gen = OpenSimplex()

# Initialize pygame and start clock
pygame.init()
clock = pygame.time.Clock()
displaySize = [pygame.display.Info().current_w//2, pygame.display.Info().current_h//2]

# Create and display window
screen = pygame.display.set_mode(displaySize, pygame.RESIZABLE)
pygame.display.set_caption("Hello World!")
pygame.display.set_icon(pygame.image.load("Assets/imgtester.png"))

# Create a database object
storage = DBIO("myWorld2")

# Create chunk buffer and chunk-position buffer
chunkBuff = ChunkBuffer(5, storage, 0, gen)

# Create a renderer
renderer = Renderer()

# game loop
running = True
while running:

    # event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False #quit game if user leaves

        elif event.type == pygame.KEYDOWN:
            if event.key in movementDict[0]: playerInc[0] = movementDict[0][event.key]
            if event.key in movementDict[1]: playerInc[1] = movementDict[1][event.key]

        elif event.type == pygame.KEYUP:
            if event.key in movementDict[0]: playerInc[0] = 0
            if event.key in movementDict[1]: playerInc[1] = 0

        elif event.type == pygame.VIDEORESIZE:
            pygame.display.Info()
            displaySize = [screen.get_width(), screen.get_height()]


    screen.fill((30, 175, 250))
    renderer.render(chunkBuff, cam, player, displaySize, screen)

    # Framerate calculation
    pygame.display.update()
    frameTime = clock.tick(framerate) + 1
    prevFramerate = 1000 / frameTime

    # Player movement handling
    speed = 128  # Number of pixels to move per-second
    player[0] += (speed/prevFramerate) * playerInc[0]
    player[1] += (speed/prevFramerate) * playerInc[1]
    if not(0 < player[1] < (CHUNK_HEIGHT*16)): player[1] -= (speed / prevFramerate) * playerInc[1]

    # Camera movement handling
    cam[0] += (player[0]-cam[0]) * 0.1
    cam[1] += (player[1]-cam[1]) * 0.1
    currChunk = int(cam[0]//(CHUNK_WIDTH*16))

    deltaChunk = currChunk-prevChunk
    prevChunk = currChunk

    if(deltaChunk > 0): chunkBuff.shiftLeft() #Player has moved right
    elif(deltaChunk < 0): chunkBuff.shiftRight() #Player has moved left

    # print(int(cam[0]), int(cam[1])//TILE_WIDTH, int(currChunk), int(prevFramerate), sep="\t")

chunkBuff.storage.stop()
pygame.display.quit()
