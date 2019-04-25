import os
import ast
from settings import *

#THIS FILE GIVES THE LOADING MAP CAPABILITY 

class LoadMap(object):
	def __init__(self):
		self.savesFolder = savesFolder
	def loadFile(self,file):
		fileName = os.path.join(self.savesFolder,file)
		loadFile = open(fileName, 'r')
		return ast.literal_eval(loadFile.read())

