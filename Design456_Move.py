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

class Design456_Move:
	def __init__(self):
		return
	#TODO : Not working .. fix it 
	def Activated(self):
		Gui.runCommand('Draft_Move',0)
		return

	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Move.svg',
				'MenuText': 'Move',
				'ToolTip':	'Move Object'
				}

Gui.addCommand('Design456_Move', Design456_Move())
