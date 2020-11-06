import sys
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

# Input handling containers
eventHandler = entity.ClientEventHandler()

# Player variables
player = entity.Player([0, 0], chunkBuffer, eventHandler.keyStates, eventHandler.mouseState, eventHandler.cursorPos, DEFAULT_FRICTION)
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
dt = 0

# game loop

running = True
while running:

    # event handling loop
    for event in pygame.event.get():

        if(event.type == pygame.QUIT):
            running = False

        elif(event.type == pygame.KEYDOWN):

            if  event.key is pygame.K_c :                Renderer.setShaders()
            elif    event.key is pygame.K_n :              cameraBound = not cameraBound # This should free the camera from being fixed to the player
            elif    event.key is pygame.K_SLASH :          pass
            elif cameraBound :                                       eventHandler.addKey( event.key )

        elif    event.type == pygame.KEYUP and cameraBound :                eventHandler.remKey( event.key )

        elif    event.type == pygame.MOUSEMOTION and cameraBound :         eventHandler.addMouseMotion( event, camera, displaySize )

        elif    event.type == pygame.MOUSEBUTTONDOWN and cameraBound :     eventHandler.addMouseButton( event.button )

        elif    event.type == pygame.MOUSEBUTTONUP and cameraBound :       eventHandler.remMouseButton( event.button )

        elif    event.type == pygame.VIDEORESIZE :         eventHandler.addWindowResize( )

    # camera movement handling
    if  cameraBound :
        camera[0] += ( player.pos[0] - camera[0] ) * LERP_C
        camera[1] += ( player.pos[1] - camera[1] ) * LERP_C

    elif    eventHandler.keyInFlag  :
        if      eventHandler.keyStates[pygame.K_a]  : camera[0] -= SCALE_VEL * dt
        elif    eventHandler.keyStates[pygame.K_d]  : camera[0] += SCALE_VEL * dt

        if      eventHandler.keyStates[pygame.K_w]  : camera[1] += SCALE_VEL * dt
        elif    eventHandler.keyStates[pygame.K_s]  : camera[1] -= SCALE_VEL * dt

    if(int(prevCamera[0]) != int(camera[0]) or int(prevCamera[1]) != int(camera[1])):   eventHandler.addCameraMotion( )

    if(eventHandler.cameraMovementFlag):

        Renderer.updateCam()
        Renderer.render()

        prevCamera[0], prevCamera[1] = camera[0], camera[1]

        currChunk = math.floor(camera[0]/CHUNK_WIDTH_P)
        deltaChunk = currChunk - prevChunk
        prevChunk = currChunk

        if(deltaChunk != 0):

            loadedIndex = chunkBuffer.shiftBuffer(deltaChunk)
            Renderer.renderChunk(loadedIndex)

        eventHandler.cameraMovementFlag = False

    if(eventHandler.windowResizeFlag):

        displaySize[0] = screen.get_width()
        displaySize[1] = screen.get_height()

        Renderer.updateRefs()
        Renderer.render()

        eventHandler.windowResizeFlag = False

    # Player movement handling
    if  eventHandler.keyInFlag or eventHandler.mouseInFlag :

        player.run()
        if(player.inventory.isEnabled): Renderer.renderInv()
        eventHandler.mouseInFlag, eventHandler.keyinFlag = False, False

    updatedIndex = player.update( dt )

    if(updatedIndex is not None):
        Renderer.renderChunkOnly( updatedIndex )
        Renderer.render()

    # Updating screen
    pygame.display.update()

    # Framerate calculation
    dt = clock.tick(0) / 1000
    #framerate = 1 / min(dt, 0.001)


chunkBuffer.saveComplete()
chunkBuffer.serializer.stop()
pygame.display.quit()
