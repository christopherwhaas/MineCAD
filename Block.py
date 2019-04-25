import settings
from pyglet.gl import *
from pyglet.window import key
import math
import os
import copy

#THIS FILE ADDS A BLOCK TO THE DICTIONARY OF BLOCKS AND ADDS EACH FACE, ALSO DRAWS BLOCKS WHEN CALLED


def cubePoints(x, y, z, n):
    return [
        (x-n,y,z-n, x-n,y,z, x,y,z, x,y,z-n), # top
        (x-n,y-n,z-n, x,y-n,z-n, x,y-n,z, x-n,y-n,z), # bottom
        (x-n,y-n,z-n, x-n,y-n,z, x-n,y,z, x-n,y,z-n), # left
        (x,y-n,z, x,y-n,z-n, x,y,z-n, x,y,z), # right
        (x-n,y-n,z, x,y-n,z, x,y,z, x-n,y,z), # front
        (x,y-n,z-n, x-n,y-n,z-n, x-n,y,z-n, x,y,z-n), # back
        ]
def tuplePoints(x, y, z, n):
    return (
        (x-n,y,z-n, x-n,y,z, x,y,z, x,y,z-n), # top
        (x-n,y-n,z-n, x,y-n,z-n, x,y-n,z, x-n,y-n,z), # bottom
        (x-n,y-n,z-n, x-n,y-n,z, x-n,y,z, x-n,y,z-n), # left
        (x,y-n,z, x,y-n,z-n, x,y,z-n, x,y,z), # right
        (x-n,y-n,z, x,y-n,z, x,y,z, x-n,y,z), # front
        (x,y-n,z-n, x-n,y-n,z-n, x-n,y,z-n, x,y,z-n), # back
        )

def getTopFace(x,y,z,n):
    return (x-n,y,z-n, x-n,y,z, x,y,z, x,y,z-n)

def getTexture(file):
    tex = pyglet.image.load(file).get_texture()
    glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
    return pyglet.graphics.TextureGroup(tex)

class Block(object):

    def __init__(self):
        self.blue = getTexture(os.path.join(settings.texturesFolder,'BlueTex.png'))
        self.red = getTexture(os.path.join(settings.texturesFolder,'RedTex.png'))
        self.orange = getTexture(os.path.join(settings.texturesFolder,'OrangeTex.png'))
        self.purple = getTexture(os.path.join(settings.texturesFolder,'PurpleTex.png'))
        self.texCoords = ('t2f',(0,0,.781,0,.781,.781,0,.781))

    def drawBlocks(self,blockDict):
        blockDict = copy.copy(blockDict)
        self.blocks = pyglet.graphics.Batch()
        color = ('c3f',(26/255,124/255,6/255)*4)
        self.blocks.add(4,GL_QUADS,None,('v3f',(0,0,0, 0,0,settings.mapSize, settings.mapSize,0,settings.mapSize ,settings.mapSize, 0 ,0)),color)
        for block in blockDict:
            if blockDict[block] == 1:
                x,y,z = block
                blockCoords = cubePoints(x,y,z,1)
                for face in range(0,6):
                    self.blocks.add(4,GL_QUADS,self.blue,('v3f',blockCoords[face]),self.texCoords)
            if blockDict[block] == 2:
                x,y,z = block
                blockCoords = cubePoints(x,y,z,1)
                for face in range(0,6):
                    self.blocks.add(4,GL_QUADS,self.red,('v3f',blockCoords[face]),self.texCoords)
            if blockDict[block] == 3:
                x,y,z = block
                blockCoords = cubePoints(x,y,z,1)
                for face in range(0,6):
                    self.blocks.add(4,GL_QUADS,self.purple,('v3f',blockCoords[face]),self.texCoords)
            if blockDict[block] == 4:
                x,y,z = block
                blockCoords = cubePoints(x,y,z,1)
                for face in range(0,6):
                    self.blocks.add(4,GL_QUADS,self.orange,('v3f',blockCoords[face]),self.texCoords)
        self.blocks.draw()


class OrangeBlock(object):
    def __init__(self,x,y,z):
        X,Y,Z = x,y,z
        if settings.blockInit.get((X,Y,Z),None) == None:
            settings.blockInit[(X,Y,Z)] = 4
        if tuplePoints(X,Y,Z,1) not in settings.faces:
            settings.faces.add(tuplePoints(X,Y,Z,1))
        

class BlueBlock(object):
    def __init__(self,x,y,z):
        X,Y,Z = x,y,z
        if settings.blockInit.get((X,Y,Z),None) == None:
            settings.blockInit[(X,Y,Z)] = 1
        if tuplePoints(X,Y,Z,1) not in settings.faces:
            settings.faces.add(tuplePoints(X,Y,Z,1))

class RedBlock(object):
    def __init__(self,x,y,z):
        X,Y,Z = x,y,z
        if settings.blockInit.get((X,Y,Z),None) == None:
            settings.blockInit[(X,Y,Z)] = 2
        if tuplePoints(X,Y,Z,1) not in settings.faces:
            settings.faces.add(tuplePoints(X,Y,Z,1))
        

class PurpleBlock(object):
    def __init__(self,x,y,z):
        X,Y,Z = x,y,z
        if settings.blockInit.get((X,Y,Z),None) == None:
            settings.blockInit[(X,Y,Z)] =3
        if tuplePoints(X,Y,Z,1) not in settings.faces:
            settings.faces.add(tuplePoints(X,Y,Z,1))

class GroundBlock(object):
    def __init__(self,x,z):
        X,Y,Z = x,0,z
        if settings.blockInit.get((X,Y,Z),None) == None:
            settings.blockInit[(X,Y,Z)] =0
        if tuplePoints(X,Y,Z,1) not in settings.faces:
            settings.faces.add(tuplePoints(X,Y,Z,1)[0])
