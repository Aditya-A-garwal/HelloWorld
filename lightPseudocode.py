def driveProp():
    chunk = []
    luminous = None#the luminosity of the block
    for y in range(CHUNK_HEIGHT):
        for x in range(CHUNK_WIDTH):
            if chunk[x][y] is luminous:
                propagate(chunk,x,y,True,True,True,True)
                while(y-1-i>0 and x-1-i>0):#up diagonal left
                    propagate(chunk,x-1-i,y-1-i,up=True,left=True)
                while(y-1-i>0 and x+1+i<CHUNK_WIDTH):#up diagonal right
                    propagate(chunk,x+1+i,y-1-i,up=True,right=True)
                while(y+1+i<CHUNK_HEIGHT and x-1-i>0):#down diagonal left
                    propagate(chunk,x-1-i,y+1+i,down=True,left=True)
                while(y+1+i<CHUNK_HEIGHT and x+1+i<CHUNK_WIDTH):#down diagonal right
                    propagate(chunk,x+1+i,y+1+i,down=True,right=True)

def propagate(l, x, y, up=False, down=False, left=False, right=False):
    valid = True#check if valid
    if valid and lightval != 0:
        if up:
            l[y+1][x].lightval = 0.5#some value
            propagate(y+1, x, up=True)
        if down:
            l[y-1][x].lightval = 0.5#some value
            propagate(y-1, x, down=True)
        if right:
            l[y][x+1].lightval = 0.5#some value
            propagate(y, x+1, right=True)
        if left:
            l[y][x-1]lightval = 0.5#some value
            propagate(y, x-1, left=True)
    else:
        return
