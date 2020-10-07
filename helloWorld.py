import sys, time
from pygame.locals import *

from Renderer import *
from Serializer import *

import entity

# Screen variables
displaySize = [400, 300]
prevFramerate = framerate = 0

# Camera variables
camera = pygame.math.Vector2([0, CHUNK_HEIGHT_P//2])
prevCamera = [0, 0]

# Player variables
player = entity.Entity(0, [0, 0], [0, 0], DEFAULT_FRICTION)
currChunk = prevChunk = deltaChunk = 0

# Initialize pygame and start clock
pygame.init()
clock = pygame.time.Clock()

# Create chunk buffer and chunk-position buffer
chunkBuffer = ChunkBuffer(13, 0, Serializer("world1"), chunkGenerator())

# Create and display window
screen = pygame.display.set_mode(displaySize, pygame.RESIZABLE)
pygame.display.set_caption("Hello World!")
pygame.display.set_icon(pygame.image.load("Resources/Default/gameIcon.png"))

# Convert all images to optimize for blitting
loadImageTable()

# Initialize the renderer
Renderer.initialize(chunkBuffer, camera, player, displaySize, screen)

keyRelease = keyPress = None

# game loop

running = True
while running:

    # Client-side


    # event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #quit game if user leaves

        elif event.type == pygame.KEYDOWN:
            if(event.key is pygame.K_c):
                Renderer.setShaders()
            else:
                keyPress = event.key

        elif event.type == pygame.KEYUP:
            if(event.key is not pygame.K_c):
                keyRelease = event.key

        elif event.type == pygame.VIDEORESIZE:
            displaySize[0], displaySize[1] = screen.get_width(), screen.get_height()

            Renderer.updateRefs()
            Renderer.render()

    # camera movement handling
    camera[0] += (player.pos[0]-camera[0]) * 0.05
    camera[1] += (player.pos[1]-camera[1]) * 0.05

    if(int(prevCamera[0]) != int(camera[0]) or int(prevCamera[1]) != int(camera[1])):
        Renderer.updateCam()
        Renderer.render()

    prevCamera[0], prevCamera[1] = camera
    currChunk = math.floor(camera[0]/CHUNK_WIDTH_P)

    # Updating screen
    pygame.display.update()


    # Server-side

    # Framerate calculation
    frameTime = clock.tick(framerate) + 1
    prevFramerate = 1000 / frameTime

    # Player movement handling
    #player.run(keyPress, keyRelease, frameTime)

    if(keyPress is not None):
        player.keyPress(keyPress)
        keyPress = None

    if(keyRelease is not None):
        player.keyRelease(keyRelease)
        keyRelease = None

    player.update(frameTime)

    deltaChunk = currChunk-prevChunk
    prevChunk = currChunk

    if(deltaChunk > 0):
        # Player has moved right
        #chunkBuffer.shiftLeft()
        chunkBuffer.shiftBuffer(deltaChunk)
        for i in range(0, 13): print(chunkBuffer.chunks[i].index, end='    ')
        print()
        Renderer.renderChunk(-1)

    elif(deltaChunk < 0):
        # Player has moved left
        #chunkBuffer.shiftRight()
        chunkBuffer.shiftBuffer(deltaChunk)
        for i in range(0, 13): print(chunkBuffer.chunks[i].index, end='    ')
        print()
        Renderer.renderChunk(0)

chunkBuffer.saveComplete()
chunkBuffer.serializer.stop()
pygame.display.quit()