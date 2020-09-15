import pyglet, numpy, sys, random, pickle
from opensimplex import OpenSimplex

from Tile import *
from Chunk import *
from Renderer import *

from Serializer import *

# Create Pyglet Window
displaySize = [400, 300]
myScreen = pyglet.window.Window(width=displaySize[0], height=displaySize[1], resizable = True, caption="Hello World!")
myScreen.set_minimum_size(displaySize[0], displaySize[1]) 
myScreen.set_icon(pyglet.image.load("Resources/Mock/imgtester.png"))

# Variables to store Client actions
keyPress, keyRelease = None, None
secondaryPress, secondaryRelease = None, None

# Camera variables
camera = [0,CHUNK_HEIGHT*TILE_WIDTH*0.5]

# Player variables
player = [0,CHUNK_HEIGHT*TILE_WIDTH*0.5]
playerInc = [0,0]
currChunk = prevChunk = deltaChunk = 0
framerate = 1
speed = 8 * TILE_WIDTH #number of tiles to move per second

#Create noise object
gen = OpenSimplex()

# Create a derializer object
serializer = Serializer("myWorld2")

# Create chunk buffer and chunk-position buffer
chunkBuffer = ChunkBuffer(5, serializer, 0, gen)

# Initialize the renderer by giving it references to all necessary objects
Renderer.initialize(chunkBuffer, camera, player, displaySize)

# Create a background batch
backgroundBatch = pyglet.graphics.Batch() 
background = pyglet.shapes.Rectangle(x=0, y=0, width=displaySize[0], height=displaySize[1], color=(100,175,250), batch=backgroundBatch)

@myScreen.event
def on_draw():
    # Function to draw to screen (Client-side)
    global framerate
    global player, camera, speed, playerInc
    global chunkBuffer, deltaChunk, prevChunk, currChunk
    global renderer
    global displaySize
    global background, backgroundBatch

    backgroundBatch.draw()
    Renderer.render()

@myScreen.event
def on_key_press(symbol, modifiers):    
    # Key press event handler (Client-side)
    global keyPress, secondaryPress
    keyPress, secondaryPress = symbol, modifiers

@myScreen.event
def on_key_release(symbol, modifiers):
    # Key Release event handler (Client-side)
    global keyRelease, secondaryRelease
    keyRelease, secondaryRelease = symbol, modifiers

# @myScreen.event
# def on_mouse_press(x, y, button, modifiers):
#     # Mouse Press event handler (Client-side)
#     pass

# @myScreen.event
# def on_mouse_release(x, y, button, modifiers):
#     # Mouse Release event handler (Client-side)
#     pass

# @myScreen.event
# def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
#     # Mouse Drag event handler (Client-side)
#     pass

# @myScreen.event
# def on_mouse_enter(x, y):
#     # Mouse Enter event handler (Client-side)
#     pass

# @myScreen.event
# def on_mouse_leave(x, y):
#     # Mouse Leave event handler (Client-side)
#     pass

@myScreen.event
def on_resize(newWidth, newHeight):
    # Window Resize event handler (Client-side)
    global displaySize
    global background, backgroundBatch

    displaySize[0] = newWidth
    displaySize[1] = newHeight

    background.width, background.height = displaySize


# Main function (Server-side)
def update(dt):        
    global keyPress, secondaryPress, keyRelease, secondaryRelease
    global framerate
    global player, camera, speed, playerInc
    global chunkBuffer, deltaChunk, prevChunk, currChunk
    global renderer
    global displaySize

    if(keyPress == pyglet.window.key.A): playerInc[0] = -1
    elif(keyPress == pyglet.window.key.D): playerInc[0] = 1
    elif(keyPress == pyglet.window.key.S): playerInc[1] = -1    
    elif(keyPress == pyglet.window.key.W): playerInc[1] = 1  

    if(keyRelease == pyglet.window.key.A or keyRelease == pyglet.window.key.D): playerInc[0] = 0
    elif(keyRelease == pyglet.window.key.S or keyRelease == pyglet.window.key.W): playerInc[1] = 0                   

    # Camera movement handling
    camera[0] += (player[0]-camera[0]) * 0.25
    camera[1] += (player[1]-camera[1]) * 0.25

    # Player movement handling    
    player[0] += (speed*dt) * playerInc[0]
    player[1] += (speed*dt) * playerInc[1]
    currChunk = int(player[0]//(CHUNK_WIDTH*TILE_WIDTH))    
    if not(0 < player[1] < (CHUNK_HEIGHT*TILE_WIDTH)): player[1] -= (speed*dt) * playerInc[1]    

    # Chunk movement handling
    deltaChunk = currChunk-prevChunk
    prevChunk = currChunk

    if(deltaChunk > 0): chunkBuffer.shiftLeft() #Player has moved right
    elif(deltaChunk < 0): chunkBuffer.shiftRight() #Player has moved left

    # Framerate calculation    
    framerate = 1/dt    
    keyPress, keyRelease, secondaryPress, secondaryRelease = None, None, None, None

pyglet.clock.schedule_interval(update, 0.01) # Main function is called a maximum of 100 times every second
pyglet.app.run() # Start running the program

chunkBuffer.serializer.stop()