#***************************************************************************
#*																		   *
#*	Open source - FreeCAD												   *
#*	Design456 Part													   *
#*	Auth : Mariwan Jalal and others										   *
#***************************************************************************
import os
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
import Design456Init 
#from Part import CommandShapes  #Tube   not working


class Design456_Part_Utils:
	list= [ "Design456_Part_Join" ,
 
			] 
			   
	"""Design456 Part Utils Toolbar"""
	def GetResources(self):
		return{
				'Pixmap' :	Design456Init.ICON_PATH +  '/Part_Utils.svg',
				'MenuText': 'Utils',
				'ToolTip': 'Utils'
			}
	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True
    
	def Activated(self):
		self.appendToolbar("Design456_Part_Utils", self.list)
		


# Join
class Design456_Part_Box:
		
	def Activated(self):
		try:

		except ImportError as err:
			App.Console.PrintError("'Part::Box' Failed. "
								   "{err}\n".format(err=str(err)))
	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Part_Box.svg',
				'MenuText': 'Part_Box',
				'ToolTip':	'Part Box'
				}
Gui.addCommand('Design456_Part_Box', Design456_Part_Box())						
