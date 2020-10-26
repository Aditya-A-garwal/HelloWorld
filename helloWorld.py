import sys, time
from pygame.locals import *
from Renderer import *

import entity

# Screen variables
displaySize = [400, 300]
framerate = 0

# Camera variables
#camera = pygame.math.Vector2([0, CHUNK_HEIGHT_P//2])
camera = [0, CHUNK_HEIGHT_P//2]
prevCamera = [0, 0]
cameraBound = True

# Initialize pygame and start clock
pygame.init()
clock = pygame.time.Clock()

# Create chunk buffer and chunk-position buffer
chunkBuffer = ChunkBuffer(11, 0, "world1")

# Player variables
player = entity.Player(0, [0, 0], [0, 0], chunkBuffer, DEFAULT_FRICTION)
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

keyPress = { pygame.K_w : False, pygame.K_a : False, pygame.K_s : False, pygame.K_d : False }
dt = 0

mousePress = { 1 : False, 2 : False, 3 : False, 4 : False, 5 : False }
mousePos = [-1, -1]
mouseWorldPos = [-1, -1]

# game loop

running = True
while running:

    # Client-side
    keyFlag = False
    mouseFlag = False

    # event handling loop
    for event in pygame.event.get():

        if(event.type == pygame.QUIT):
            running = False

        elif(event.type == pygame.KEYDOWN):

            if(event.key in keyPress):
                keyFlag = True
                keyPress[event.key] = True

            elif(event.key is pygame.K_c):
                Renderer.setShaders()
            elif(event.key is pygame.K_n):
                cameraBound = not cameraBound # This should free the camera from being fixed to the player
            elif(event.key is pygame.K_SLASH):
                plc = input(">> ")
                # processPLC(plc)

        elif event.type == pygame.KEYUP:
            if( event.key in keyPress):
                keyFlag = True
                keyPress[event.key] = False

        # i for left, 2 for middle, 3 for right, 4 for scroll up and 5 for scroll down
        elif(event.type == pygame.MOUSEMOTION):
            mousePos = event.pos[0], event.pos[1]
            mouseWorldPos = int(camera[0]) + mousePos[0] - displaySize[0]//2, int(camera[1]) + displaySize[1]//2 - mousePos[1]

        elif(event.type == pygame.MOUSEBUTTONDOWN):
            mouseFlag = True
            mousePress[event.button] = True

        elif(event.type == pygame.MOUSEBUTTONUP):
            mouseFlag = True
            mousePress[event.button] = False

        elif(event.type == pygame.VIDEORESIZE):
            displaySize[0], displaySize[1] = screen.get_width(), screen.get_height()

            Renderer.updateRefs()
            Renderer.render()

    # camera movement handling
    if( cameraBound ):
        camera[0] += ( player.pos[0] - camera[0] ) * LERP_C
        camera[1] += ( player.pos[1] - camera[1] ) * LERP_C

    else:
        if( keyPress[pygame.K_a] ): camera[0] -= SCALE_VEL * dt
        elif( keyPress[pygame.K_d] ): camera[0] += SCALE_VEL * dt

        if( keyPress[pygame.K_w] ): camera[1] += SCALE_VEL * dt
        elif( keyPress[pygame.K_s] ): camera[1] -= SCALE_VEL * dt

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
    #framerate = 1 / min(dt, 0.001)

    # Player movement handling
    if(cameraBound):
        if(mouseFlag):
            updatedIndex = player.runMouse(mousePress, mouseWorldPos)
            if(updatedIndex is not None):
                Renderer.renderChunk(updatedIndex)
                Renderer.render()
        if(keyFlag):
            player.run(keyPress)


    player.update(dt)

    deltaChunk = currChunk - prevChunk
    prevChunk = currChunk

    if(deltaChunk != 0):        # Player has moved
        loadedIndex = chunkBuffer.shiftBuffer(deltaChunk)
        Renderer.renderChunk(loadedIndex)
        # Renderer.renderLightmap(loadedIndex)
        Renderer.renderLightmap(loadedIndex - deltaChunk)


chunkBuffer.saveComplete()
chunkBuffer.serializer.stop()
pygame.display.quit()
