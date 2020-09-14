import pyglet, numpy, sys, random, pickle
from pygame.locals import *
from opensimplex import OpenSimplex

from Tile import *
from Chunk import *
from Renderer import *

from databaseIO import *

# Screen variables
displaySize = [800,600]
framerate = 1

# Create variables to store Client actions
keyPress, keyRelease = None, None
secondaryPress, secondaryRelease = None, None

# create Pyglet Window
myScreen = pyglet.window.Window(width=displaySize[0], height=displaySize[1], resizable = True, caption="Hello World!")
myScreen.set_minimum_size(600, 450) 
myScreen.set_icon(pyglet.image.load("Resources/Mock/imgtester.png"))

# Temporary variables
myblit = [10, 10]
myIncrement = [0, 0]
image = pyglet.image.load("Resources/Mock/grass.png")  

# Camera variables
cam = [0,CHUNK_HEIGHT*16/2]

# Player variables
player = [0,CHUNK_HEIGHT*TILE_WIDTH*0.5]
playerInc = [0,0]
currChunk = prevChunk = deltaChunk = 0
speed = 6 * TILE_WIDTH #number of tiles to move per second

#Create noise object
gen = OpenSimplex()

# Create a database object
storage = DBIO("myWorld2")

# Create chunk buffer and chunk-position buffer
chunkBuff = ChunkBuffer(3, storage, 0, gen)

# Create a renderer
renderer = Renderer()

# Function to draw to screen (Client-side)
@myScreen.event
def on_draw():
    myScreen.clear()    
    image.blit(myblit[0], myblit[1])        

# Key press event handler (Client-side)
@myScreen.event
def on_key_press(symbol, modifiers):    
    global keyPress, secondaryPress
    keyPress, secondaryPress = symbol, modifiers

# Key Release event handler (Client-side)
@myScreen.event
def on_key_release(symbol, modifiers):
    global keyRelease, secondaryRelease
    keyRelease, secondaryRelease = symbol, modifiers

'''
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
'''

# Window Resize event handler (Client-side)
@myScreen.event
def on_resize(newWidth, newHeight):
    global displaySize
    displaySize[0] = newWidth
    displaySize[1] = newHeight

# Main function (Server-side)
def update(dt):        
    global keyPress, secondaryPress, keyRelease, secondaryRelease
    global framerate
    global player, camera, speed, playerInc
    global chunkBuff, deltaChunk, prevChunk, currChunk
    global renderer

    if(keyPress == pyglet.window.key.A): myIncrement[0] = -128
    elif(keyPress == pyglet.window.key.D): myIncrement[0] = 128
    elif(keyPress == pyglet.window.key.S): myIncrement[1] = -128    
    elif(keyPress == pyglet.window.key.W): myIncrement[1] = 128  

    if(keyRelease == pyglet.window.key.A or keyRelease == pyglet.window.key.D): myIncrement[0] = 0
    elif(keyRelease == pyglet.window.key.S or keyRelease == pyglet.window.key.W): myIncrement[1] = 0           

    myblit[0] += myIncrement[0]*dt
    myblit[1] += myIncrement[1]*dt       

    # Camera movement handling
    cam[0] += (player[0]-cam[0]) * 0.1
    cam[1] += (player[1]-cam[1]) * 0.1
    currChunk = int(cam[0]//(CHUNK_WIDTH*TILE_WIDTH))
    #renderer.render(chunkBuff, cam, player, displaySize, screen)

    # Player movement handling    
    player[0] += (speed/framerate) * playerInc[0]
    player[1] += (speed/framerate) * playerInc[1]
    if not(0 < player[1] < (CHUNK_HEIGHT*TILE_WIDTH)): player[1] -= (speed / framerate) * playerInc[1]    

    # Chunk movement handling
    deltaChunk = currChunk-prevChunk
    prevChunk = currChunk

    if(deltaChunk > 0): chunkBuff.shiftLeft() #Player has moved right
    elif(deltaChunk < 0): chunkBuff.shiftRight() #Player has moved left

    # Framerate calculation    
    framerate = 1/dt
    print(1/dt)
    keyPress, keyRelease, secondaryPress, secondaryrelease = None, None, None, None

pyglet.clock.schedule_interval(update, 1/240) # Main function is called a maximum of 240 times every second
pyglet.app.run() # Start running the app

chunkBuff.storage.stop()