import sys
import os
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
import Design456Init 
sys.path.append(Design456Init.PYRAMID_PATH)
import polyhedrons
from PySide import QtCore, QtGui

class Design456_Pyramid:
	list= ["Pyramid",
			"Tetrahedron",
			"Hexahedron",
			"Octahedron",
			"Dodecahedron",
			"Icosahedron",
			"Icosahedron_truncated",
			"Geodesic_sphere"
			] 
			   
	"""Design456 Pyramid Toolbar"""
	def GetResources(self):
		return{
				'Pixmap' :	 Design456Init.PYRAMID_ICON_PATH+	'/Pyramid.svg',
				'MenuText': 'Pyramid',
				'ToolTip':	'Pyramid'
			}
	
	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True
 
	def Activated(self):
		self.appendToolbar("Pyramid",self.list) # creates a new toolbar with your commands
		self.appendMenu("Pyramid",self.list) # creates a new menu
		
