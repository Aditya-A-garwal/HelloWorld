import sys
from pygame.locals import *

from Renderer import *
from noiseGenerator import *
from Serializer import *

# Screen variables
displaySize = [400, 300]  #[pygame.display.Info().current_w//2, pygame.display.Info().current_h//2]
prevFramerate = framerate = 0

# Camera variables
camera = pygame.math.Vector2([0, CHUNK_HEIGHT_P//2])
prevCamera = [0, 0]

# Player variables
player = pygame.math.Vector2([0, 0])
playerInc = [0,0]
currChunk = prevChunk = deltaChunk = 0
speed = 20 * TILE_WIDTH #number of tiles to move per second

#Create noise object
gen = OpenSimplex()

# Create a database object
serializer = Serializer("world1")

# Initialize pygame and start clock
pygame.init()
clock = pygame.time.Clock()

# Create chunk buffer and chunk-position buffer
bufferSize = int(pygame.display.Info().current_w/CHUNK_WIDTH_P)+2
if(bufferSize % 2 == 0): bufferSize += 1
chunkBuffer = ChunkBuffer(bufferSize, 0, serializer, gen)
del bufferSize

# Create and display window
screen = pygame.display.set_mode(displaySize, pygame.RESIZABLE)
pygame.display.set_caption("Hello World!")
pygame.display.set_icon(pygame.image.load("Resources/Default/gameIcon.png"))
loadImageTable()

# Initialize the renderer
Renderer.initialize(chunkBuffer, camera, player, displaySize, screen)

# game loop
running = True
while running:

    # Client-side

    keyRelease, keyPress = None, None

    # event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #quit game if user leaves

        elif event.type == pygame.KEYDOWN: keyPress = event.key
        elif event.type == pygame.KEYUP: keyRelease = event.key

        elif event.type == pygame.VIDEORESIZE:
            displaySize[0], displaySize[1] = screen.get_width(), screen.get_height()

            Renderer.updateRefs()
            Renderer.render()

    # camera movement handling
    # camera[0] += (player[0]-camera[0]) * 0.05
    # camera[1] += (player[1]-camera[1]) * 0.05
    camera[0], camera[1] = camera.lerp(player, 0.05)

    if(int(prevCamera[0]) != int(camera[0]) or int(prevCamera[1]) != int(camera[1])):
        Renderer.updateCam()
        Renderer.render()

    prevCamera[0], prevCamera[1] = camera
    currChunk = math.floor(camera[0]/CHUNK_WIDTH_P)

    # Updating screen
    pygame.display.update()


    # Server-side

    # Key to movement translation
    if(keyPress is pygame.K_a): playerInc[0] = -1
    elif(keyPress is pygame.K_d): playerInc[0] = 1

    if(keyPress is pygame.K_w): playerInc[1] = 1
    elif(keyPress is pygame.K_s): playerInc[1] = -1

    if(keyRelease is pygame.K_a or keyRelease is pygame.K_d): playerInc[0] = 0
    elif(keyRelease is pygame.K_w or keyRelease is pygame.K_s): playerInc[1] = 0

    # Framerate calculation
    frameTime = clock.tick(framerate) + 1
    prevFramerate = 1000 / frameTime

    # Player movement handling
    player[0] += (speed / prevFramerate) * playerInc[0]
    player[1] += (speed / prevFramerate) * playerInc[1]
    if not(0 < player[1] < CHUNK_HEIGHT_P): player[1] -= (speed / prevFramerate) * playerInc[1]

    deltaChunk = currChunk-prevChunk
    prevChunk = currChunk

    if(deltaChunk > 0):
        # Player has moved right
        chunkBuffer.shiftLeft()
        Renderer.renderChunk(-1)

    elif(deltaChunk < 0):
        # Player has moved left
        chunkBuffer.shiftRight()
        Renderer.renderChunk(0)

chunkBuffer.saveComplete()
chunkBuffer.serializer.stop()
pygame.display.quit()