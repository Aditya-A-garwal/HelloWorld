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

# cameraera variables
camera = [0,CHUNK_HEIGHT*TILE_WIDTH*0.5]

# Player variables
player = [0,CHUNK_HEIGHT*TILE_WIDTH*0.5]
playerInc = [0,0]
currChunk = prevChunk = deltaChunk = 0
speed = 24 * TILE_WIDTH #number of tiles to move per second

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
serializer = Serializer("world1")

# Create chunk buffer and chunk-position buffer
chunkBuff = ChunkBuffer(211, serializer, 0, gen)

# Create a renderer
Renderer.initialize(chunkBuff, camera, player, displaySize, screen)

# game loop
running = True
while running:

    # Client-side

    keyRelease, keyPress = None, None    

    # event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            chunkBuff.saveComplete()
            chunkBuff.serializer.stop()
            running = False #quit game if user leaves

        elif event.type == pygame.KEYDOWN: keyPress = event.key            
        elif event.type == pygame.KEYUP: keyRelease = event.key            

        elif event.type == pygame.VIDEORESIZE:
            pygame.display.Info()
            displaySize[0] = screen.get_width()
            displaySize[1] = screen.get_height()
            Renderer.updateSize()

    # cameraera movement handling
    camera[0] += (player[0]-camera[0]) * 0.075
    camera[1] += (player[1]-camera[1]) * 0.075 
    currChunk = int(camera[0]//(CHUNK_WIDTH*TILE_WIDTH))
    Renderer.updateCam()

    # Rendering and updating screen
    screen.fill((30, 175, 250))        
    pygame.display.update(Renderer.render())


    # Server-side    

    # Key to movement translation
    if(keyPress == pygame.K_a): playerInc[0] = -1
    elif(keyPress == pygame.K_d): playerInc[0] = 1

    if(keyPress == pygame.K_w): playerInc[1] = 1
    elif(keyPress == pygame.K_s): playerInc[1] = -1

    if(keyRelease == pygame.K_a or keyRelease == pygame.K_d): playerInc[0] = 0    
    elif(keyRelease == pygame.K_w or keyRelease == pygame.K_s): playerInc[1] = 0    

    # Framerate calculation
    frameTime = clock.tick(framerate) + 1
    prevFramerate = 1000 / frameTime

    # Player movement handling    
    player[0] += (speed / prevFramerate) * playerInc[0]
    player[1] += (speed / prevFramerate) * playerInc[1]    
    if not(0 < player[1] < (CHUNK_HEIGHT*TILE_WIDTH)): player[1] -= (speed / prevFramerate) * playerInc[1]    

    deltaChunk = currChunk-prevChunk
    prevChunk = currChunk

    if(deltaChunk > 0): chunkBuff.shiftLeft() #Player has moved right
    elif(deltaChunk < 0): chunkBuff.shiftRight() #Player has moved left
    print(prevFramerate)

pygame.display.quit()
