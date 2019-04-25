import settings
import os
from pyglet.gl import *
from pyglet.window import key
from Player import *
from Block import *
from StartScreen import *
from Screen import *
from SaveMap import *
from LoadMap import *
from stlConvert import *
from pyglet.window import mouse
from pyglet import image
import _thread
import ast
import math
import pickle
import sys
from socket import socket, AF_INET, SOCK_DGRAM


#THIS IS THE GAME CLIENT WHICH IS RUN TO START THE GAME.

def handleData(mySocket):
    while True:
        data = mySocket.recv(2048)
        d = pickle.loads(data)
        if d!='':
            if d[0]!=None:
                x,y,z = list(d[0])[0]
                settings.blockInit.update(d[0])
                settings.faces.add(tuplePoints(x,y,z,1))
            if d[1]!=None:
                x,y,z = d[1]
                del settings.blockInit[d[1]]
                settings.faces.discard(tuplePoints(x,y,z,1))

#Written based off of Documentation of Sockets Example 18.1.15 https://docs.python.org/3/library/socket.html#timeouts-and-the-accept-method
def initClient():
    SERVER_IP   = settings.HostIP
    PORT_NUMBER = 5009
    SIZE = 4096
    mySocket = socket( AF_INET, SOCK_DGRAM )
    mySocket.connect((SERVER_IP, PORT_NUMBER))
    mySocket.sendall(pickle.dumps(''))
    settings.mySocket = mySocket
    _thread.start_new_thread(handleData,(mySocket,))
    return mySocket


#General Structure was written based off of initial tutorial(https://www.youtube.com/watch?v=Hqg4qePJV2U)
# and 'Minecraft in 500 Lines of Python' by Richard Donkin 
#(https://www.slideshare.net/rdonkin/minecraft-in-500-lines-with-pyglet-pycon-uk)
# all code was written by myself (Not copied and pasted)


def listCubePoints(x, y, z, n):
        return [
        x-n,y,z-n, x-n,y,z, x,y,z, x,y,z-n, # top
        x-n,y-n,z-n, x,y-n,z-n, x,y-n,z, x-n,y-n,z, # bottom
        x-n,y-n,z-n, x-n,y-n,z, x-n,y,z, x-n,y,z-n, # left
        x,y-n,z, x,y-n,z-n, x,y,z-n, x,y,z, # right
        x-n,y-n,z, x,y-n,z, x,y,z, x-n,y,z, # front
        x,y-n,z-n, x-n,y-n,z-n, x-n,y,z-n, x,y,z-n, # back
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


class Window(pyglet.window.Window):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        settings.multiplayer = False
        self.fpsDisplay = pyglet.clock.ClockDisplay()
        self.clear()
        self.startScreen = True
        self.startScreenDisplay = StartScreen()
        self.pauseScreenDisplay = PauseScreen()
        self.saveScreenDisplay = SaveScreen()
        self.loadScreenDisplay = LoadScreen()
        self.helpScreenDisplay = HelpScreen()
        self.stlSelectionScreenDisplay = StlSelectionScreen()
        self.playTypeScreenDisplay = PlayTypeScreen()
        self.ipSelectionScreenDisplay = IpSelectionScreen()
        self.stlCompleteScreenDisplay = StlCompleteScreen()
        self.stlConversion = stlConvert()
        self.player = Player(29,29)
        self.blocks = Block()
        self.save= SaveMap()
        self.load = LoadMap()
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.set_exclusive_mouse(False)
        self.mouse = [0,0]
        self.loadScreen = False
        self.playing= False
        self.pauseScreen = False
        self.saveScreen=False
        self.helpScreen = False
        self.stlSelectionScreen = False
        self.playTypeScreen = False
        self.ipSelectionScreen = False
        self.stlCompleteScreen=False
        pyglet.clock.schedule_interval(self.update,1/settings.FPS)

        
    def multiplayerOn(self):
        self.mySocket = initClient()
        settings.multiplayer = True
    

    def initWorld(self, worldSize=100):
        for x in range (1,(worldSize)+1):
            for z in range (1,(worldSize)+1):
                GroundBlock(x,z)

    def listFilesInSaves(self):
        fileList = []
        for file in os.listdir(os.path.join(settings.gameFolder,'saves')):
            if file.endswith(".txt"):
                fileList.append(file)
        return fileList
    #Written based off of Tutorial
    def getSight(self):
        x, y = self.player.rot
        m = math.cos(math.radians(y))
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return (dx, dy, dz)

        
    #Written based off of Tutorial
    def setLock(self,state):
        self.lock = state
        self.set_exclusive_mouse(state)
    lock = False   
    mouse_lock = property(lambda self:self.lock,setLock)


    #Written based off of Tutorial
    def set3d(self):
        glClearColor(.4,.6,1,1)
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width*2, height*2)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        renderDist = int(1+(2*(settings.mapSize**2)))
        gluPerspective(65.0, self.width / float(self.height), 0.05, renderDist)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.player.rot
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.player.pos
        glTranslatef(-x, -y, -z)
        

        #Written based off of Tutorial
    def set2d(self):
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, width*2, height*2)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()


    def on_mouse_motion(self,x,y,dx,dy):
        self.mouse = (x,y)
        if self.mouse_lock: 
            if self.playing:
                self.player.mouse_motion(dx,dy)


    def on_mouse_press(self,x, y, button, modifiers):
        if button == mouse.LEFT and not (modifiers & key.MOD_CTRL):

            if self.startScreen:
                if 406/1280*settings.WIDTH<=x<=874/1280*settings.WIDTH and 369/800*settings.HEIGHT<=y<=457/800*settings.HEIGHT:
                    self.playTypeScreen = True
                    self.startScreen = False
                elif 406/1280*settings.WIDTH<=x<=874/1280*settings.WIDTH and 225/800*settings.HEIGHT<=y<=313/800*settings.HEIGHT:
                    self.startScreen = False
                    self.loadScreen = True

            elif self.playTypeScreen:
                if 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 504/800*settings.HEIGHT<=y<=593/800*settings.HEIGHT:
                    self.player = Player(29,29)
                    settings.blockInit = {}
                    settings.faces=set()
                    self.initWorld(settings.mapSize)
                    self.playing = True
                    self.playTypeScreen = False
                    self.mouse_lock = not self.mouse_lock
                elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 361/800*settings.HEIGHT<=y<=450/800*settings.HEIGHT:
                    settings.HostIP = ''
                    self.ipSelectionScreen = True
                    self.playTypeScreen = False
                elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 71/800*settings.HEIGHT<=y<=160/800*settings.HEIGHT:
                    self.playTypeScreen = False
                    self.startScreen = True

            elif self.ipSelectionScreen:
                if 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 361/800*settings.HEIGHT<=y<=450/800*settings.HEIGHT:
                    self.ipSelectionScreen = False
                    self.player = Player(29,29)
                    settings.blockInit = {}
                    settings.faces=set()
                    self.initWorld(settings.mapSize)
                    self.playing = True
                    self.mouse_lock = not self.mouse_lock
                    self.multiplayerOn()
                elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 71/800*settings.HEIGHT<=y<=160/800*settings.HEIGHT:
                    self.ipSelectionScreen = False
                    self.playTypeScreen = True

            elif self.stlCompleteScreen:
                if 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 71/800*settings.HEIGHT<=y<=160/800*settings.HEIGHT:
                    self.stlCompleteScreen = False
                    self.pauseScreen = True
            elif self.pauseScreen:
                if 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 643/800*settings.HEIGHT<=y<=732/800*settings.HEIGHT:
                    self.playing = True
                    self.pauseScreen = False
                    self.mouse_lock = not self.mouse_lock
                elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 500/800*settings.HEIGHT<=y<=589/800*settings.HEIGHT:
                    self.pauseScreen= False
                    self.saveScreen=True
                elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 357/800*settings.HEIGHT<=y<=446/800*settings.HEIGHT:
                    self.pauseScreen = False
                    self.stlSelectionScreen = True
                elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 214/800*settings.HEIGHT<=y<=303/800*settings.HEIGHT:
                    self.pauseScreen = False
                    self.startScreen = True
                elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 71/800*settings.HEIGHT<=y<=160/800*settings.HEIGHT:
                    self.set_exclusive_mouse(False)
                    self.close()

            elif self.saveScreen:
                if 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 357/800*settings.HEIGHT<=y<=446/800*settings.HEIGHT:
                    fileName = settings.saveName+'.txt'
                    self.save.saveFile(fileName,settings.blockInit)
                    settings.saveName = ''
                    self.saveScreen=False
                    self.pauseScreen = True
                elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 71/800*settings.HEIGHT<=y<=160/800*settings.HEIGHT:
                    self.saveScreen = False
                    settings.saveName = ''
                    self.pauseScreen = True

            elif self.loadScreen:
                fileList = self.listFilesInSaves()
                fileList=sorted(fileList)
                if 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 643/800*settings.HEIGHT<=y<=732/800*settings.HEIGHT:
                    if settings.fileCount < len(fileList):
                        settings.blockInit={}
                        settings.faces = set()
                        self.initWorld(settings.mapSize)
                        settings.blockInit.update(self.load.loadFile(fileList[settings.fileCount]))
                        for coord in settings.blockInit:
                            X,Y,Z = coord
                            if tuplePoints(X,Y,Z,1) not in settings.faces:
                                settings.faces.add(tuplePoints(X,Y,Z,1))
                        self.loadScreen = False
                        self.playing = True
                        settings.fileCount=0
                        self.mouse_lock = not self.mouse_lock

                elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 500/800*settings.HEIGHT<=y<=589/800*settings.HEIGHT:
                    if settings.fileCount+1 < len(fileList):
                        settings.blockInit={}
                        settings.faces = set()
                        self.initWorld(settings.mapSize)
                        settings.blockInit.update(self.load.loadFile(fileList[settings.fileCount+1]))
                        for coord in settings.blockInit:
                            X,Y,Z = coord
                            if tuplePoints(X,Y,Z,1) not in settings.faces:
                                settings.faces.add(tuplePoints(X,Y,Z,1))
                        self.loadScreen = False
                        self.playing = True
                        settings.fileCount=0
                        self.mouse_lock = not self.mouse_lock

                elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 357/800*settings.HEIGHT<=y<=446/800*settings.HEIGHT:
                    if settings.fileCount+2 < len(fileList):
                        settings.blockInit={}
                        settings.faces = set()
                        self.initWorld(settings.mapSize)
                        settings.blockInit.update(self.load.loadFile(fileList[settings.fileCount+2]))
                        for coord in settings.blockInit:
                            X,Y,Z = coord
                            if tuplePoints(X,Y,Z,1) not in settings.faces:
                                settings.faces.add(tuplePoints(X,Y,Z,1))
                        self.loadScreen = False
                        self.playing = True
                        settings.fileCount = 0
                        self.mouse_lock = not self.mouse_lock

                elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 214/800*settings.HEIGHT<=y<=303/800*settings.HEIGHT:
                    if settings.fileCount+3 < len(fileList):
                        settings.blockInit={}
                        settings.faces = set()
                        self.initWorld(settings.mapSize)
                        settings.blockInit.update(self.load.loadFile(fileList[settings.fileCount+3]))
                        for coord in settings.blockInit:
                            X,Y,Z = coord
                            if tuplePoints(X,Y,Z,1) not in settings.faces:
                                settings.faces.add(tuplePoints(X,Y,Z,1))
                        self.loadScreen = False
                        self.playing = True
                        settings.fileCount=0
                        self.mouse_lock = not self.mouse_lock

                elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 71/800*settings.HEIGHT<=y<=160/800*settings.HEIGHT:
                    self.loadScreen = False
                    settings.fileCount = 0
                    self.startScreen=True
                elif 959/1280*settings.WIDTH<=x<=1052/1280*settings.WIDTH and 370/800*settings.HEIGHT<=y<=491/800*settings.HEIGHT:
                    if settings.fileCount+4 < len(fileList):
                        settings.fileCount+=4
                elif 225/1280*settings.WIDTH<=x<=317/1280*settings.WIDTH and 370/800*settings.HEIGHT<=y<=491/800*settings.HEIGHT:
                    if settings.fileCount-4 >=0:
                        settings.fileCount-=4

            elif self.helpScreen:
                if 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 48/800*settings.HEIGHT<=y<=137/800*settings.HEIGHT:
                    self.helpScreen = False
                    self.startScreen = True

            elif self.stlSelectionScreen:
                fileList = self.listFilesInSaves()
                fileList=sorted(fileList)
                if 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 643/800*settings.HEIGHT<=y<=732/800*settings.HEIGHT:
                    if settings.fileCount < len(fileList):
                        self.stlConversion.convert(fileList[settings.fileCount])
                        self.stlSelectionScreen = False
                        settings.fileCount=0
                        self.stlCompleteScreen = True
                elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 500/800*settings.HEIGHT<=y<=589/800*settings.HEIGHT:
                    if settings.fileCount+1 < len(fileList):
                        self.stlConversion.convert(fileList[settings.fileCount+1])
                        self.stlSelectionScreen = False
                        settings.fileCount=0
                        self.stlCompleteScreen = True
                elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 357/800*settings.HEIGHT<=y<=446/800*settings.HEIGHT:
                    if settings.fileCount+2 < len(fileList):
                        self.stlConversion.convert(fileList[settings.fileCount+2])
                        self.stlSelectionScreen = False
                        settings.fileCount=0
                        self.stlCompleteScreen = True
                elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 214/800*settings.HEIGHT<=y<=303/800*settings.HEIGHT:
                    if settings.fileCount+3 < len(fileList):
                        self.stlConversion.convert(fileList[settings.fileCount+3])
                        self.stlSelectionScreen = False
                        settings.fileCount=0
                        self.stlCompleteScreen = True
                elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 71/800*settings.HEIGHT<=y<=160/800*settings.HEIGHT:
                    self.stlSelectionScreen = False
                    settings.fileCount=0
                    self.pauseScreen = True
                elif 959/1280*settings.WIDTH<=x<=1052/1280*settings.WIDTH and 370/800*settings.HEIGHT<=y<=491/800*settings.HEIGHT:
                    if settings.fileCount+4 < len(fileList):
                        settings.fileCount+=4
                elif 225/1280*settings.WIDTH<=x<=317/1280*settings.WIDTH and 370/800*settings.HEIGHT<=y<=491/800*settings.HEIGHT:
                    if settings.fileCount-4 >=0:
                        settings.fileCount-=4

            elif self.playing:
                self.player.mouse_press(x,y)

        if button == mouse.RIGHT or ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
            if self.playing:
                self.player.removeBlock(x,y)

        
    def on_key_press(self,KEY,MOD):
        if self.saveScreen:
            if 97<=KEY<=122 or 48<=KEY<=57:
                if len(settings.saveName)<=10:
                    if KEY>57:
                        settings.saveName+=chr(KEY)
                    else:
                        settings.saveName+=str(KEY-48)
            elif KEY == key.BACKSPACE:
                settings.saveName = settings.saveName[:len(settings.saveName)-1]
        elif self.ipSelectionScreen:
            if KEY == key._1:
                if len(settings.HostIP)<=14:
                    settings.HostIP += '1'
            elif KEY == key._2:
                if len(settings.HostIP)<=14:
                    settings.HostIP += '2'
            elif KEY == key._3:
                if len(settings.HostIP)<=14:
                    settings.HostIP += '3'
            elif KEY == key._4:
                if len(settings.HostIP)<=14:
                    settings.HostIP += '4'
            elif KEY == key._5:
                if len(settings.HostIP)<=14:
                    settings.HostIP += '5'
            elif KEY == key._6:
                if len(settings.HostIP)<=14:
                    settings.HostIP += '6'
            elif KEY == key._7:
                if len(settings.HostIP)<=14:
                    settings.HostIP += '7'
            elif KEY == key._8:
                if len(settings.HostIP)<=14:
                    settings.HostIP += '8'
            elif KEY == key._9:
                if len(settings.HostIP)<=14:
                    settings.HostIP += '9'
            elif KEY == key._0:
                if len(settings.HostIP)<=14:
                    settings.HostIP += '0'
            elif KEY == key.BACKSPACE:
                settings.HostIP = settings.HostIP[:len(settings.HostIP)-1]
            elif KEY == key.PERIOD:
                if len(settings.HostIP)<=14:
                    settings.HostIP += '.'

        elif self.playing:
            if KEY == key.ESCAPE:
                self.playing = False
                self.pauseScreen = True
                self.mouse_lock = not self.mouse_lock
        elif self.startScreen:
            if KEY == key.H:
                self.startScreen = False
                self.helpScreen = True



    #Written based off of Tutorial
    def update(self,dt):
        
        if self.startScreen:
            x,y = self.mouse
            self.startScreenDisplay.checkSelection(x,y)

        elif self.pauseScreen:
            x,y = self.mouse
            self.pauseScreenDisplay.checkSelection(x,y)

        elif self.playTypeScreen:
            x,y = self.mouse
            self.playTypeScreenDisplay.checkSelection(x,y)

        elif self.ipSelectionScreen:
            x,y = self.mouse
            self.ipSelectionScreenDisplay.checkSelection(x,y)

        elif self.saveScreen:
            x,y = self.mouse
            self.saveScreenDisplay.checkSelection(x,y)

        elif self.loadScreen:
            x,y = self.mouse
            self.loadScreenDisplay.checkSelection(x,y)

        elif self.helpScreen:
            x,y = self.mouse
            self.helpScreenDisplay.checkSelection(x,y)

        elif self.stlSelectionScreen:
            x,y = self.mouse
            self.stlSelectionScreenDisplay.checkSelection(x,y)
        elif self.stlCompleteScreen:
            x,y = self.mouse
            self.stlCompleteScreenDisplay.checkSelection(x,y)

        elif self.playing:
            self.player.update(dt,self.keys)



        

    #Written based off of Tutorial
    def on_draw(self):
        self.clear()
        if self.startScreen:
            self.set2d()
            self.startScreenDisplay.draw()
            self.startScreenDisplay.drawSelection()
        elif self.pauseScreen:
            self.set2d()
            self.pauseScreenDisplay.draw()
            self.pauseScreenDisplay.drawSelection()
        elif self.saveScreen:
            self.set2d()
            self.saveScreenDisplay.draw()
            self.saveScreenDisplay.drawSelection()
            self.saveScreenDisplay.drawSaveName()
        elif self.ipSelectionScreen:
            self.set2d()
            self.ipSelectionScreenDisplay.draw()
            self.ipSelectionScreenDisplay.drawSelection()
            self.ipSelectionScreenDisplay.drawIP()
        elif self.playTypeScreen:
            self.set2d()
            self.playTypeScreenDisplay.draw()
            self.playTypeScreenDisplay.drawSelection()
        elif self.loadScreen:
            self.set2d()
            self.loadScreenDisplay.draw()
            self.loadScreenDisplay.drawSelection()
            self.loadScreenDisplay.drawLoads()
        elif self.helpScreen:
            self.set2d()
            self.helpScreenDisplay.draw()
            self.helpScreenDisplay.drawSelection()
        elif self.stlSelectionScreen:
            self.set2d()
            self.stlSelectionScreenDisplay.draw()
            self.stlSelectionScreenDisplay.drawSelection()
            self.stlSelectionScreenDisplay.drawFiles()
        elif self.stlCompleteScreen:
            self.set2d()
            self.stlCompleteScreenDisplay.draw()
            self.stlCompleteScreenDisplay.drawSelection()
        elif self.playing:
            self.set3d()
            self.drawFocusedBlock()
            self.blocks.drawBlocks(settings.blockInit)
            self.set2d()
            #self.fpsDisplay.draw()
            self.drawCurrentBlock()

    
    #Written based off of Tutorial
    def drawFocusedBlock(self):
        block = self.player.blockInSight()[0]
        if block:
            x, y, z = block
            cubePoint = listCubePoints(x+.01, y+.01, z+.01, 1.02)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', cubePoint))
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)


    #Written based off of Tutorial
    def drawCurrentBlock(self):
        if self.player.block == 1:
            image = pyglet.image.load(os.path.join(settings.texturesFolder,'Blue.png'))
            x,y = image.width, image.height
            image.blit(self.width-100,0)
        if self.player.block == 2:
            image = pyglet.image.load(os.path.join(settings.texturesFolder,'Red.png'))
            x,y = image.width, image.height
            image.blit(self.width-100,0)
        if self.player.block == 3:
            image = pyglet.image.load(os.path.join(settings.texturesFolder,'Purple.png'))
            x,y = image.width, image.height
            image.blit(self.width-100,0)
        if self.player.block == 4:
            image = pyglet.image.load(os.path.join(settings.texturesFolder,'Orange.png'))
            x,y = image.width, image.height
            image.blit(self.width-100,0)


if __name__ =='__main__':
    window = Window(width=settings.WIDTH,height=settings.HEIGHT,caption=settings.TITLE, resizable=False)
    image = pyglet.image.load(os.path.join(settings.texturesFolder,'cursor.png'))
    cursor = pyglet.window.ImageMouseCursor(image,20,20)
    window.set_mouse_cursor(cursor)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    pyglet.app.run()