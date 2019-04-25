import settings
import os
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse
from pyglet import image
import math

#THIS FILE HANDLES THE DRAWING OF EACH SPLASH SCREEN OTHER THAN THE TITLE SCREEN

def listFilesInSaves():
        fileList = []
        for file in os.listdir(os.path.join(settings.gameFolder,'saves')):
            if file.endswith(".txt"):
                fileList.append(file)
        return fileList

class PauseScreen(object):
	def __init__(self):
		self.width = settings.WIDTH
		self.height = settings.HEIGHT
		self.background = pyglet.image.load(os.path.join(settings.texturesFolder,'pauseScreen.png'))
		self.select = pyglet.image.load(os.path.join(settings.texturesFolder,'selection.png'))
		self.background.width = settings.WIDTH
		self.background.height = settings.HEIGHT
		self.selection = None

	def checkSelection(self,x,y):
			if 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 643/800*settings.HEIGHT<=y<=732/800*settings.HEIGHT:
				self.selection = 'Resume'
			elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 500/800*settings.HEIGHT<=y<=589/800*settings.HEIGHT:
				self.selection = 'Save'
			elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 357/800*settings.HEIGHT<=y<=446/800*settings.HEIGHT:
				self.selection = 'stl'
			elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 214/800*settings.HEIGHT<=y<=303/800*settings.HEIGHT:
				self.selection = 'Load'
			elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 71/800*settings.HEIGHT<=y<=160/800*settings.HEIGHT:
				self.selection = 'Exit'
			else:
				self.selection = None
	def draw(self):
		self.background.blit(0,0)

	def drawSelection(self):
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		if self.selection == 'Resume':
			self.select.blit(405/1280*settings.WIDTH,643/800*settings.HEIGHT)
		elif self.selection == 'Save':
			self.select.blit(405/1280*settings.WIDTH,500/800*settings.HEIGHT)
		elif self.selection == 'stl':
			self.select.blit(405/1280*settings.WIDTH,357/800*settings.HEIGHT)
		elif self.selection == 'Load':
			self.select.blit(405/1280*settings.WIDTH,214/800*settings.HEIGHT)
		elif self.selection == 'Exit':
			self.select.blit(405/1280*settings.WIDTH,71/800*settings.HEIGHT)

class SaveScreen(object):
	def __init__(self):
		self.width = settings.WIDTH
		self.height = settings.HEIGHT
		self.background = pyglet.image.load(os.path.join(settings.texturesFolder,'saveScreenv2.png'))
		self.select = pyglet.image.load(os.path.join(settings.texturesFolder,'selection.png'))
		self.background.width = settings.WIDTH
		self.background.height = settings.HEIGHT
		self.selection = None

	def checkSelection(self,x,y):
			
			if 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 357/800*settings.HEIGHT<=y<=446/800*settings.HEIGHT:
				self.selection = 'save'
			
			elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 71/800*settings.HEIGHT<=y<=160/800*settings.HEIGHT:
				self.selection = 'back'
			else:
				self.selection = None
	def draw(self):
		self.background.blit(0,0)
	def drawSelection(self):
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		if self.selection == 'save':
			self.select.blit(405/1280*settings.WIDTH,357/800*settings.HEIGHT)
		elif self.selection == 'back':
			self.select.blit(405/1280*settings.WIDTH,71/800*settings.HEIGHT)

	def drawSaveName(self):
		pyglet.font.add_file(os.path.join(settings.texturesFolder,'dpcomic.ttf'))
		label = pyglet.text.Label(settings.saveName,
                          font_name='DPComic',
                          font_size=50,
                          x=(420/1280*settings.WIDTH), y=(545/800*settings.HEIGHT),
                          anchor_x='left', anchor_y='center')
		label.draw()

class LoadScreen(object):
	def __init__(self):
		self.width = settings.WIDTH
		self.height = settings.HEIGHT
		self.background = pyglet.image.load(os.path.join(settings.texturesFolder,'loadScreenv2.png'))
		self.select = pyglet.image.load(os.path.join(settings.texturesFolder,'selection.png'))
		self.select2 = pyglet.image.load(os.path.join(settings.texturesFolder,'selection2.png'))
		self.background.width = settings.WIDTH
		self.background.height = settings.HEIGHT
		self.selection = None

	def checkSelection(self,x,y):
		fileList = listFilesInSaves()
		fileList = sorted(fileList)
		if 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 643/800*settings.HEIGHT<=y<=732/800*settings.HEIGHT:
			if settings.fileCount < len(fileList):
				self.selection = 'save1'
		elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 500/800*settings.HEIGHT<=y<=589/800*settings.HEIGHT:
			if settings.fileCount+1 < len(fileList):
				self.selection = 'save2'
		elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 357/800*settings.HEIGHT<=y<=446/800*settings.HEIGHT:
			if settings.fileCount+2 < len(fileList):
				self.selection = 'save3'
		elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 214/800*settings.HEIGHT<=y<=303/800*settings.HEIGHT:
			if settings.fileCount+3 < len(fileList):
				self.selection = 'save4'
		elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 71/800*settings.HEIGHT<=y<=160/800*settings.HEIGHT:
			self.selection = 'back'
		elif 959/1280*settings.WIDTH<=x<=1052/1280*settings.WIDTH and 370/800*settings.HEIGHT<=y<=491/800*settings.HEIGHT:
			self.selection = 'next'
		elif 225/1280*settings.WIDTH<=x<=317/1280*settings.WIDTH and 370/800*settings.HEIGHT<=y<=491/800*settings.HEIGHT:
			self.selection='prev'
		else:
			self.selection = None
	def draw(self):
		self.background.blit(0,0)

	def drawSelection(self):
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		if self.selection == 'save1':
			self.select.blit(405/1280*settings.WIDTH,643/800*settings.HEIGHT)
		elif self.selection == 'save2':
			self.select.blit(405/1280*settings.WIDTH,500/800*settings.HEIGHT)
		elif self.selection == 'save3':
			self.select.blit(405/1280*settings.WIDTH,357/800*settings.HEIGHT)
		elif self.selection == 'save4':
			self.select.blit(405/1280*settings.WIDTH,214/800*settings.HEIGHT)
		elif self.selection == 'back':
			self.select.blit(405/1280*settings.WIDTH,71/800*settings.HEIGHT)
		elif self.selection == 'next':
			self.select2.blit(959/1280*settings.WIDTH,370/800*settings.HEIGHT)
		elif self.selection == 'prev':
			self.select2.blit(225/1280*settings.WIDTH,370/800*settings.HEIGHT)
	def drawLoads(self):
		for i in range(4):
			fileList = listFilesInSaves()
			fileList = sorted(fileList)
			if settings.fileCount+i < len(fileList):
				file = fileList[settings.fileCount+i]
				fileName = file[:-4]
				pyglet.font.add_file(os.path.join(settings.texturesFolder,'dpcomic.ttf'))
				label = pyglet.text.Label(fileName,
		                          font_name='DPComic',
		                          font_size=60,
		                          x=(settings.WIDTH//2), y=((687-143*i)/800*settings.HEIGHT),
		                          anchor_x='center', anchor_y='center')
				label.draw()


class HelpScreen(object):
	def __init__(self):
		self.width = settings.WIDTH
		self.height = settings.HEIGHT
		self.background = pyglet.image.load(os.path.join(settings.texturesFolder,'controlScreen.png'))
		self.select = pyglet.image.load(os.path.join(settings.texturesFolder,'selection.png'))
		self.background.width = settings.WIDTH
		self.background.height = settings.HEIGHT
		self.selection = None

	def checkSelection(self,x,y):
			if 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 48/800*settings.HEIGHT<=y<=137/800*settings.HEIGHT:
				self.selection = 'back'
			else:
				self.selection = None
	def draw(self):
		self.background.blit(0,0)
	def drawSelection(self):
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		if self.selection == 'back':
			self.select.blit(405/1280*settings.WIDTH,48/800*settings.HEIGHT)

class StlSelectionScreen(object):
	def __init__(self):
		self.width = settings.WIDTH
		self.height = settings.HEIGHT
		self.background = pyglet.image.load(os.path.join(settings.texturesFolder,'stlSelectionScreenv2.png'))
		self.select = pyglet.image.load(os.path.join(settings.texturesFolder,'selection.png'))
		self.select2 = pyglet.image.load(os.path.join(settings.texturesFolder,'selection2.png'))
		self.background.width = settings.WIDTH
		self.background.height = settings.HEIGHT
		self.selection = None

	def checkSelection(self,x,y):
		fileList = listFilesInSaves()
		fileList = sorted(fileList)
		if 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 643/800*settings.HEIGHT<=y<=732/800*settings.HEIGHT:
			if settings.fileCount < len(fileList):
				self.selection = 'save1'
		elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 500/800*settings.HEIGHT<=y<=589/800*settings.HEIGHT:
			if settings.fileCount+1 < len(fileList):
				self.selection = 'save2'
		elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 357/800*settings.HEIGHT<=y<=446/800*settings.HEIGHT:
			if settings.fileCount+2 < len(fileList):
				self.selection = 'save3'
		elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 214/800*settings.HEIGHT<=y<=303/800*settings.HEIGHT:
			if settings.fileCount+3 < len(fileList):
				self.selection = 'save4'
		elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 71/800*settings.HEIGHT<=y<=160/800*settings.HEIGHT:
			self.selection = 'back'
		elif 959/1280*settings.WIDTH<=x<=1052/1280*settings.WIDTH and 370/800*settings.HEIGHT<=y<=491/800*settings.HEIGHT:
			self.selection = 'next'
		elif 225/1280*settings.WIDTH<=x<=317/1280*settings.WIDTH and 370/800*settings.HEIGHT<=y<=491/800*settings.HEIGHT:
			self.selection='prev'

		else:
			self.selection = None

	def draw(self):
		self.background.blit(0,0)
		
	def drawSelection(self):
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		if self.selection == 'save1':
			self.select.blit(405/1280*settings.WIDTH,643/800*settings.HEIGHT)
		elif self.selection == 'save2':
			self.select.blit(405/1280*settings.WIDTH,500/800*settings.HEIGHT)
		elif self.selection == 'save3':
			self.select.blit(405/1280*settings.WIDTH,357/800*settings.HEIGHT)
		elif self.selection == 'save4':
			self.select.blit(405/1280*settings.WIDTH,214/800*settings.HEIGHT)
		elif self.selection == 'back':
			self.select.blit(405/1280*settings.WIDTH,71/800*settings.HEIGHT)
		elif self.selection == 'next':
			self.select2.blit(959/1280*settings.WIDTH,370/800*settings.HEIGHT)
		elif self.selection == 'prev':
			self.select2.blit(225/1280*settings.WIDTH,370/800*settings.HEIGHT)

	def drawFiles(self):
		for i in range(4):
			fileList = listFilesInSaves()
			fileList = sorted(fileList)
			if settings.fileCount+i < len(fileList):
				file = fileList[settings.fileCount+i]
				fileName = file[:-4]
				pyglet.font.add_file(os.path.join(settings.texturesFolder,'dpcomic.ttf'))
				label = pyglet.text.Label(fileName,
		                          font_name='DPComic',
		                          font_size=60,
		                          x=(settings.WIDTH//2), y=((687-143*i)/800*settings.HEIGHT),
		                          anchor_x='center', anchor_y='center')
				label.draw()


class PlayTypeScreen(object):
	def __init__(self):
		self.width = settings.WIDTH
		self.height = settings.HEIGHT
		self.background = pyglet.image.load(os.path.join(settings.texturesFolder,'multiOrSingle.png'))
		self.select = pyglet.image.load(os.path.join(settings.texturesFolder,'selection.png'))
		self.background.width = settings.WIDTH
		self.background.height = settings.HEIGHT
		self.selection = None

	def checkSelection(self,x,y):
		if 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 504/800*settings.HEIGHT<=y<=593/800*settings.HEIGHT:
			self.selection = 'Single'
		elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 361/800*settings.HEIGHT<=y<=450/800*settings.HEIGHT:
			self.selection = 'Multi'
		elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 71/800*settings.HEIGHT<=y<=160/800*settings.HEIGHT:
			self.selection = 'back'
		else:
			self.selection = None

	def draw(self):
		self.background.blit(0,0)
		
	def drawSelection(self):
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		if self.selection == 'Single':
			self.select.blit(405/1280*settings.WIDTH,504/800*settings.HEIGHT)
		elif self.selection == 'Multi':
			self.select.blit(405/1280*settings.WIDTH,361/800*settings.HEIGHT)
		elif self.selection == 'back':
			self.select.blit(405/1280*settings.WIDTH,71/800*settings.HEIGHT)

class IpSelectionScreen(object):
	def __init__(self):
		self.width = settings.WIDTH
		self.height = settings.HEIGHT
		self.background = pyglet.image.load(os.path.join(settings.texturesFolder,'ipAddress.png'))
		self.select = pyglet.image.load(os.path.join(settings.texturesFolder,'selection.png'))
		self.background.width = settings.WIDTH
		self.background.height = settings.HEIGHT
		self.selection = None

	def checkSelection(self,x,y):
		if 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 361/800*settings.HEIGHT<=y<=450/800*settings.HEIGHT:
			self.selection = 'conn'
		elif 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 71/800*settings.HEIGHT<=y<=160/800*settings.HEIGHT:
			self.selection = 'back'
		else:
			self.selection = None

	def draw(self):
		self.background.blit(0,0)
		
	def drawSelection(self):
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		if self.selection == 'conn':
			self.select.blit(405/1280*settings.WIDTH,361/800*settings.HEIGHT)
		elif self.selection == 'back':
			self.select.blit(405/1280*settings.WIDTH,71/800*settings.HEIGHT)
	def drawIP(self):
		pyglet.font.add_file(os.path.join(settings.texturesFolder,'dpcomic.ttf'))
		label = pyglet.text.Label(settings.HostIP,
                          font_name='DPComic',
                          font_size=50,
                          x=(420/1280*settings.WIDTH), y=(549/800*settings.HEIGHT),
                          anchor_x='left', anchor_y='center')
		label.draw()

class StlCompleteScreen(object):
	def __init__(self):
		self.width = settings.WIDTH
		self.height = settings.HEIGHT
		self.background = pyglet.image.load(os.path.join(settings.texturesFolder,'stlComplete.png'))
		self.select = pyglet.image.load(os.path.join(settings.texturesFolder,'selection.png'))
		self.background.width = settings.WIDTH
		self.background.height = settings.HEIGHT
		self.selection = None

	def checkSelection(self,x,y):
		if 405/1280*settings.WIDTH<=x<=873/1280*settings.WIDTH and 71/800*settings.HEIGHT<=y<=160/800*settings.HEIGHT:
			self.selection = 'back'
		else:
			self.selection = None

	def draw(self):
		self.background.blit(0,0)
		
	def drawSelection(self):
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		if self.selection == 'back':
			self.select.blit(405/1280*settings.WIDTH,71/800*settings.HEIGHT)
	