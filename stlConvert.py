import os
import numpy as np
from stl import mesh
import ast
from settings import *

#THIS FILE HANDLES THE STL CONVERSION OF A SAVED .TXT FILE

def cubeVertices(x, y, z, n):
    return [
    [x  , y  , z  ],
    [x+n, y  , z  ],
    [x+n, y+n, z  ],
    [x  , y+n, z  ],
    [x  , y  , z+n],
    [x+n, y  , z+n],
    [x+n, y+n, z+n],
    [x  , y+n, z+n]]



class stlConvert(object):
	def __init__(self):
		self.verts=[]
		self.savesFolder = savesFolder
		self.faceset=set()
		self.singleface = []
		self.stlFolder = stlFolder


	def convert(self,file):
		self.blockDict = None
		self.faceset=set()
		self.singleface = []
		self.verts=[]
		file = file[:-4]
		fileName = os.path.join(self.savesFolder,file+'.txt')
		loadFile = open(fileName, 'r')
		self.blockDict = ast.literal_eval(loadFile.read())

		for coord in self.blockDict:
			x,z,y = coord

			if self.blockDict[coord]!=0:
				listOfVerts = cubeVertices(x,y,z,1)

				for face in listOfVerts:
					x,y,z = face
					self.verts.append([x,y,z])

		self.vertArray = np.array(self.verts)
		self.triangleFaces = []

		for n in range((len(self.verts)//8)):
			self.triangleFaces+=[0+8*n,3+8*n,1+8*n],\
			[1+8*n,3+8*n,2+8*n],[0+8*n,4+8*n,7+8*n],\
			[0+8*n,7+8*n,3+8*n],[4+8*n,5+8*n,6+8*n],\
			[4+8*n,6+8*n,7+8*n],[5+8*n,1+8*n,2+8*n],\
			[5+8*n,2+8*n,6+8*n],[2+8*n,3+8*n,6+8*n],\
			[3+8*n,7+8*n,6+8*n],[0+8*n,1+8*n,5+8*n],\
			[0+8*n,5+8*n,4+8*n]
								
		self.triFaces = np.array(self.triangleFaces)

		stlObject = mesh.Mesh(np.zeros(self.triFaces.shape[0], dtype=mesh.Mesh.dtype))

		for i, f in enumerate(self.triFaces):
		    for j in range(3):

		        stlObject.vectors[i][j] = self.vertArray[f[j],:]

		stlObject.save(os.path.join(self.stlFolder,file+'.stl'))

		
		



