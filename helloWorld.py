import sys, time
from pygame.locals import *
from Renderer import *

import entity

# Screen variables
displaySize = [400, 300]
framerate = 0

# Camera variables
camera = pygame.math.Vector2([0, CHUNK_HEIGHT_P//2])
prevCamera = [0, 0]
cameraBound = True

# Initialize pygame and start clock
pygame.init()
clock = pygame.time.Clock()

# Create chunk buffer and chunk-position buffer
chunkBuffer = ChunkBuffer(11, 0, "world1")

# Player variables
player = entity.Entity(0, [0, 0], [0, 0], chunkBuffer, DEFAULT_FRICTION)
currChunk = prevChunk = deltaChunk = 0

# Create and display window
screen = pygame.display.set_mode(displaySize, pygame.RESIZABLE)
pygame.display.set_caption("Hello World!")
pygame.display.set_icon(pygame.image.load("Resources/Default/gameIcon.png"))

# Convert all images to optimized form
tiles.loadImageTable()
items.loadImageTable()

# Initialize the renderer
Renderer.initialize(chunkBuffer, camera, player, displaySize, screen)

keyPress = []
dt = 0
# game loop

running = True
while running:

    # Client-side
    keyFlag = False

    # event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #quit game if user leaves

        elif event.type == pygame.KEYDOWN:
            if(event.key is pygame.K_c):
                Renderer.setShaders()
            elif(event.key is pygame.K_n):
                # This should free the camera from being fixed to the player
                cameraBound = not cameraBound
            elif(event.key is pygame.K_SLASH):
                pass # This should open the terminal for issuing text commands
            else:
                if event.key not in keyPress:
                    keyPress.append(event.key)
                    keyFlag = True

        elif event.type == pygame.KEYUP:
            if(event.key is not pygame.K_c):
                if event.key in keyPress:
                    keyPress.remove(event.key)
                    keyFlag = True

        elif event.type == pygame.VIDEORESIZE:
            displaySize[0], displaySize[1] = screen.get_width(), screen.get_height()

            Renderer.updateRefs()
            Renderer.render()

    # camera movement handling
    if( cameraBound ):
        camera[0] += ( player.pos[0] - camera[0] ) * LERP_C
        camera[1] += ( player.pos[1] - camera[1] ) * LERP_C

    else:
        if( pygame.K_a in keyPress ): camera[0] -= SCALE_VEL * dt
        elif( pygame.K_d in keyPress ): camera[0] += SCALE_VEL * dt

        if( pygame.K_w in keyPress ): camera[1] += SCALE_VEL * dt
        elif( pygame.K_s in keyPress ): camera[1] -= SCALE_VEL * dt

    if(int(prevCamera[0]) != int(camera[0]) or int(prevCamera[1]) != int(camera[1])):
        Renderer.updateCam()
        Renderer.render()

    prevCamera[0], prevCamera[1] = camera
    currChunk = math.floor(camera[0]/CHUNK_WIDTH_P)

    # Updating screen
    pygame.display.update()


    # Server-side

    # Framerate calculation
    dt = clock.tick(0) / 1000
    framerate = 1 / (dt + 1)

    # Player movement handling
    if(keyFlag and cameraBound):
        player.run(keyPress)


    player.update(dt)

    deltaChunk = currChunk-prevChunk
    prevChunk = currChunk

    if(deltaChunk != 0):        # Player has moved
        loadedIndex = chunkBuffer.shiftBuffer(deltaChunk)
        Renderer.renderChunk(loadedIndex)
        Renderer.renderLightmap(loadedIndex - deltaChunk)


chunkBuffer.saveComplete()
chunkBuffer.serializer.stop()
pygame.display.quit()
