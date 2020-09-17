import pygame, numpy, sys, random, pickle
from pygame.locals import *
from opensimplex import OpenSimplex

from Tile import *
from Chunk import *
from Renderer import *

from Serializer import *

# Screen variables
displaySize = [0,0]
prevFramerate = framerate = 0

# Camera variables
cam = [0,CHUNK_HEIGHT*16/2]

# Player variables
player = [0,CHUNK_HEIGHT*TILE_WIDTH*0.5]
playerInc = [0,0]
currChunk = prevChunk = deltaChunk = 0
speed = 55 * TILE_WIDTH #number of tiles to move per second

#Create noise object
gen = OpenSimplex()

# Initialize pygame and start clock
pygame.init()
clock = pygame.time.Clock()
displaySize = [400, 300] #[pygame.display.Info().current_w//2, pygame.display.Info().current_h//2]

# Create and display window
screen = pygame.display.set_mode(displaySize, pygame.RESIZABLE)
pygame.display.set_caption("Hello World!")
pygame.display.set_icon(pygame.image.load("Resources/Default/gameIcon.png"))

# Create a database object
storage = Serializer("world1")

# Create chunk buffer and chunk-position buffer
chunkBuff = ChunkBuffer(211, storage, 0, gen)

# Create a renderer
Renderer.initialize(chunkBuff, cam, player, displaySize, screen)

# game loop
running = True
while running:

    # Client-side

    keyUp, keyDown = None, None    

    # event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            chunkBuff.saveComplete()
            running = False #quit game if user leaves

        elif event.type == pygame.KEYDOWN: keyDown = event.key            
        elif event.type == pygame.KEYUP: keyUp = event.key            

        elif event.type == pygame.VIDEORESIZE:
            pygame.display.Info()
            displaySize[0] = screen.get_width()
            displaySize[1] = screen.get_height()

    # Camera movement handling
    cam[0] += (player[0]-cam[0]) * 0.075
    cam[1] += (player[1]-cam[1]) * 0.075 
    currChunk = int(cam[0]//(CHUNK_WIDTH*TILE_WIDTH))

    # Rendering and updating screen
    screen.fill((30, 175, 250))
    Renderer.render()
    pygame.display.update()


    # Server-side    

    # Key to movement translation
    if(keyDown == pygame.K_a): playerInc[0] = -1
    elif(keyDown == pygame.K_d): playerInc[0] = 1

    if(keyDown == pygame.K_w): playerInc[1] = 1
    elif(keyDown == pygame.K_s): playerInc[1] = -1

    if(keyUp == pygame.K_a or keyUp == pygame.K_d): playerInc[0] = 0    
    elif(keyUp == pygame.K_w or keyUp == pygame.K_s): playerInc[1] = 0    

    # Framerate calculation
    frameTime = clock.tick(framerate) + 1
    prevFramerate = 1000 / frameTime

    # Player movement handling    
    player[0] += (speed/prevFramerate) * playerInc[0]
    player[1] += (speed/prevFramerate) * playerInc[1]    
    if not(0 < player[1] < (CHUNK_HEIGHT*TILE_WIDTH)): player[1] -= (speed / prevFramerate) * playerInc[1]    

    deltaChunk = currChunk-prevChunk
    prevChunk = currChunk

    if(deltaChunk > 0): chunkBuff.shiftLeft() #Player has moved right
    elif(deltaChunk < 0): chunkBuff.shiftRight() #Player has moved left
    print(prevFramerate)


chunkBuff.storage.stop()
pygame.display.quit()
