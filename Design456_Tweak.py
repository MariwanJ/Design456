#***************************************************************************
#*																		   *
#*	Open source - FreeCAD												   *
#*	Design456 Workbench													   *
#*	Auth : Mariwan Jalal and others										   *
#***************************************************************************
import os
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from PySide import QtGui, QtCore # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
#Modify this command to be TWEAK 
class Design456_Tweak:
	def __init__(self):
		return
	def Activated(self):
		try:
			#TODO:Needs to be implemented .
			#Gui.runCommand('Draft_Move',0)
			return
		except ImportError as err:
			App.Console.PrintError("'ExtrudeFace' Failed. "
								   "{err}\n".format(err=str(err)))
	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Tweak.svg',
				'MenuText': 'Tweak',
				'ToolTip':	'Tweak the Object'
				}

Gui.addCommand('Design456_Tweak', Design456_Tweak())
