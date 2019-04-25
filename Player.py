import settings
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse
from Block import *
import math
from Game import *
import decimal
import time
import os


#THIS FILE CONTROLS PLAYER ELEMENTS, I.E. MOVEMENT, POSITION, ROTATAION, COLLISIONS,
#AND ADDS/ REMOVES BLOCKS

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))


class Player(object):
    def __init__(self,x,z):
        self.blocks = Block()
        self.pos = [x,0+settings.playerHeight+5,z]
        self.rot = [0,0]
        self.block = 1


    def getSight(self):
        x, y = self.rot
        m = math.cos(math.radians(y))
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x-90)) * m
        dz = math.sin(math.radians(x-90)) * m
        return (dx, dy, dz)

    def blockInSight(self):
        m = 8
        maxDist = settings.reach
        x, y, z = self.pos
        dx, dy, dz = self.getSight()
        previous = None
        for _ in range(maxDist * m):
            check = self.makeInt(x,y,z)
            X,Y,Z = check
            if Y == 0:
                if check != previous and tuplePoints(X,Y,Z,1)[0] in settings.faces:
                    return check, previous
            elif check != previous and tuplePoints(X,Y,Z,1) in settings.faces:
                return check, previous
            previous = check
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return None, None
        
    def makeInt(self,x,y,z):
        if x >0:
            x = int(x+1)
        elif x:
            x = int(x)
        if y >0:
            y = int(y+1)
        elif y:
            y = int(y)
        if z >0:
            z = int(z+1)
        elif z:
            z = int(z)
        return (x,y,z)

    def collision(self,pos):
        x,y,z = self.makeInt(pos[0],pos[1],pos[2])
        for i in range(int(settings.playerHeight+1)):
            if (x,y-i,z) in settings.blockInit:
                return True
        return False

    def returnY(self,pos):
        x,y,z = self.makeInt(pos[0],pos[1],pos[2])
        if (x,y-settings.playerHeight,z) in settings.blockInit:
            return y+2
        return settings.playerHeight

    def update(self,dt,keys):
        m = 8
        dt = min(dt, 0.2)
        for _ in range(m):
            self._update(dt / m,keys)

    def _update(self,dt,keys):
        if self.pos[0]>=settings.mapSize-.1:
            self.pos[0] = settings.mapSize-.1

        elif self.pos[0]<0:
            self.pos[0] = 0.1

        if self.pos[2]>=settings.mapSize-.1:
            self.pos[2] = settings.mapSize-.1

        elif self.pos[2]<0:
            self.pos[2] = 0.1

        x,y,z = self.pos
        d = dt * settings.speed
        rad = math.radians(self.rot[0])
        dx,dz = d*math.sin(rad),d*math.cos(rad)
        if keys[key.W]:
            if not self.collision((x+dx,y,z-dz)):
                self.pos[0]+=dx 
                self.pos[2]-=dz

        if keys[key.A]:
            if not self.collision((x-dz,y,z-dx)):
                self.pos[0]-=dz 
                self.pos[2]-=dx

        if keys[key.S]:
            if not self.collision((x-dx,y,z+dz)):
                self.pos[0]-=dx 
                self.pos[2]+=dz

        if keys[key.D]:
            if not self.collision((x+dz,y,z+dx)):
                self.pos[0]+=dz 
                self.pos[2]+=dx

        if keys[key.SPACE]:
            if self.collision((x,y-settings.playerAccY,z)):
                self.pos[1] += settings.maxJump

        
        if not self.collision((x,y-settings.playerAccY/5,z)):
            self.pos[1] -= settings.playerAccY/5
            
        if keys[key._1]:
            self.block = 1
        if keys[key._2]:
            self.block = 2
        if keys[key._3]:
            self.block = 3
        if keys[key._4]:
            self.block = 4

            
        
    def mouse_press(self,x,y):
        if self.block == 1:
            block, previous = self.blockInSight()
            if previous:
                x,y,z = previous
                BlueBlock(x,y,z)
                if settings.multiplayer:
                    data = pickle.dumps(({(x,y,z):1},None))
                    settings.mySocket.sendall(data)

        elif self.block == 2:
            block, previous = self.blockInSight()
            if previous:
                x,y,z = previous
                RedBlock(x,y,z)
                if settings.multiplayer:
                    data = pickle.dumps(({(x,y,z):2},None))
                    settings.mySocket.sendall(data)

        elif self.block == 3:
            block, previous = self.blockInSight()
            if previous:
                x,y,z = previous
                PurpleBlock(x,y,z)
                if settings.multiplayer:
                    data = pickle.dumps(({(x,y,z):3},None))
                    settings.mySocket.sendall(data)

        elif self.block == 4:
            block, previous = self.blockInSight()
            if previous:
                x,y,z = previous
                OrangeBlock(x,y,z)
                if settings.multiplayer:
                    data = pickle.dumps(({(x,y,z):4},None))
                    settings.mySocket.sendall(data)

    def removeBlock(self,x,y):
        block, __ = self.blockInSight()
        if block:
            x,y,z = block
            if settings.blockInit[(x,y,z)]!= 0:
                del settings.blockInit[(x,y,z)]
                settings.faces.discard(tuplePoints(x,y,z,1))
                if settings.multiplayer:
                    data = pickle.dumps((None,(x,y,z)))
                    settings.mySocket.sendall(data)


        
    #Written based off of Tutorial
    def mouse_motion(self,dx,dy):
        m=.15
        x,y = self.rot[0],self.rot[1]
        x, y = x + dx * m, y + dy * m
        y = max(-90, min(90, y))
        self.rot = [x,y]


