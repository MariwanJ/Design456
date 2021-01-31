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
from PySide import QtGui, QtCore
import Draft
import Part

class Design456_Extract:
	"""Extract the selected shapes from objects"""
	def Activated(self):
		try:
			s = Gui.Selection.getSelectionEx()
			for o in s:
				objName = o.ObjectName
				sh = o.Object.Shape.copy()
				if hasattr(o.Object, "getGlobalPlacement"):
					gpl = o.Object.getGlobalPlacement()
					sh.Placement = gpl
				for name in o.SubElementNames:
					fullname = objName+"_"+name
					newobj = o.Document.addObject("Part::Feature",fullname)
					newobj.Shape = sh.getElement(name)
			App.ActiveDocument.recompute()
		except ImportError as err:
			App.Console.PrintError("'Design456_Extract' Failed. "
								   "{err}\n".format(err=str(err)))
	def GetResources(self):
		return{
			'Pixmap' :	Design456Init.ICON_PATH +  '/Extract.svg',
			'MenuText': 'Extract',
			'ToolTip': 'Extract selected subshapes from objects'
		}
Gui.addCommand('Design456_Extract', Design456_Extract()) 