import os

#THIS FILE CONTAINS STATIC ELEMENTS OF THE GAME AS WELL AS THE VARIABLES THAT ARE EDITTED WHEN:
#CREATING BLOCKS, HOSTIP IS ENTERED, THE SAVENAME OF FILES, AND WHICH INDEX IS USED OF THE LIST OF SAVES
#ALSO CONTAINS THE SOCKET VARIABLE ONCE INITIATED

TITLE = 'MineCAD'
WIDTH = 1280
HEIGHT = 800
FPS = 80

mapSize = 30
#player properties
playerAccX = 1
playerAccY = .7
playerFrict = -.12
maxJump=1
reach=7
speed = 5

playerHeight = 2
playerWidth = 1
faces = set()
blockInit = {}
mySocket = None
multiplayer = False
HostIP = ''
saveName=''
fileCount = 0


gameFolder = os.path.dirname(__file__)
texturesFolder = os.path.join(gameFolder,'textures')
savesFolder = os.path.join(gameFolder,'saves')
stlFolder = os.path.join(gameFolder,'stlFiles')