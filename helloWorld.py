import pyglet, pygame, numpy, sys, random, pickle
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
currChunk = prevChunk = deltaChunk = 0
speed = 5.5 * TILE_WIDTH #number of tiles to move per second

#Create noise object
gen = OpenSimplex()

# Initialize pygame and start clock
pygame.init()
clock = pygame.time.Clock()
displaySize = [pygame.display.Info().current_w//2, pygame.display.Info().current_h//2]

myScreen = pyglet.window.Window()
image = pyglet.image.load("Resources/Mock/grass.png")     
myblit = [10, 10]
myIncrement = [0, 0]

# Create and display window
screen = pygame.display.set_mode(displaySize, pygame.RESIZABLE)
pygame.display.set_caption("Hello World!")
pygame.display.set_icon(pygame.image.load("Resources/Mock/imgtester.png"))

# Create a database object
storage = DBIO("myWorld2")

# Create chunk buffer and chunk-position buffer
chunkBuff = ChunkBuffer(3, storage, 0, gen)

# Create a renderer
renderer = Renderer()

# game loop
running = False
while running:

    # Client-side

    keyUp, keyDown = None, None    

    # event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False #quit game if user leaves

        elif event.type == pygame.KEYDOWN: keyDown = event.key            
        elif event.type == pygame.KEYUP: keyUp = event.key            

        elif event.type == pygame.VIDEORESIZE:
            pygame.display.Info()
            displaySize = [screen.get_width(), screen.get_height()]

    # Camera movement handling
    cam[0] += (player[0]-cam[0]) * 0.1
    cam[1] += (player[1]-cam[1]) * 0.1
    currChunk = int(cam[0]//(CHUNK_WIDTH*TILE_WIDTH))

    # Rendering and updating screen
    screen.fill((30, 175, 250))
    renderer.render(chunkBuff, cam, player, displaySize, screen)
    pygame.display.update()


    # Server-side         

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


chunkBuff.storage.stop()
pygame.display.quit()

# Function to draw to screen (Client-side)
@myScreen.event
def on_draw():
    myScreen.clear()    
    image.blit(myblit[0], myblit[1])        

# Key press event handler (Client-side)
@myScreen.event
def on_key_press(symbol, modifiers):
    if(symbol == pyglet.window.key.A): myIncrement[0] = -128
    if(symbol == pyglet.window.key.D): myIncrement[0] = 128
    if(symbol == pyglet.window.key.S): myIncrement[1] = -128    
    if(symbol == pyglet.window.key.W): myIncrement[1] = 128  

# Key Release event handler (Client-side)
@myScreen.event
def on_key_release(symbol, modifiers):
    if(symbol == pyglet.window.key.A or symbol == pyglet.window.key.D): myIncrement[0] = 0
    elif(symbol == pyglet.window.key.S or symbol == pyglet.window.key.W): myIncrement[1] = 0           

# Mouse Press event handler (Client-side)
@myScreen.event
def on_mouse_press(x, y, button, modifiers):
    pass

# Mouse Release event handler (Client-side)
@myScreen.event
def on_mouse_release(x, y, button, modifiers):
    pass

# Mouse Drag event handler (Client-side)
@myScreen.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    pass

# Mouse Enter event handler (Client-side)
@myScreen.event
def on_mouse_enter(x, y):
    pass

# Mouse Leave event handler (Client-side)
@myScreen.event
def on_mouse_leave(x, y):
    pass

# Main function (Server-side)
def update(dt):
    myblit[0] += myIncrement[0]*dt
    myblit[1] += myIncrement[1]*dt   

    print(1/dt)

pyglet.clock.schedule_interval(update, 1/240) # Main function is called a maximum of 240 times every second
pyglet.app.run() # Start running the app
