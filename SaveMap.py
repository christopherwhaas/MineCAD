import os
import json 
from settings import *

#FILE HANDLES SAVING MAPS

class SaveMap(object):
	def __init__(self):
		self.savesFolder = savesFolder
		
	def saveFile(self,file,save):
		fileName = os.path.join(self.savesFolder,file)
		saveFile = open(fileName, "w")
		saveFile.write(str(save))
		saveFile.close()




