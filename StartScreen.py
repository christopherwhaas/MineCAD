import settings
import os
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse
from pyglet import image
import math

#THIS IF THE INITIAL TITLE SCREEN

def getTexture(file):
    tex = pyglet.image.load(file).get_texture()
    glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
    return pyglet.graphics.TextureGroup(tex)

class StartScreen(object):
	def __init__(self):
		self.width = settings.WIDTH
		self.height = settings.HEIGHT
		self.background = pyglet.image.load(os.path.join(settings.texturesFolder,'StartScreen.png'))
		self.select = pyglet.image.load(os.path.join(settings.texturesFolder,'selection.png'))
		self.background.width = settings.WIDTH
		self.background.height = settings.HEIGHT
		self.selection = None

	def checkSelection(self,x,y):
		if 406/1280*settings.WIDTH<=x<=874/1280*settings.WIDTH and 369<=y<=457:
			self.selection = 'New'
		elif 406/1280*settings.WIDTH<=x<=874/1280*settings.WIDTH and 225<=y<=313:
			self.selection = 'Load'
		else:
			self.selection = None


	def draw(self):
		self.background.blit(0,0)

	def drawSelection(self):
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		if self.selection == 'New':
			self.select.blit(406/1280*settings.WIDTH,369)
		elif self.selection == 'Load':
			self.select.blit(406/1280*settings.WIDTH,225)





