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
from PySide import QtGui, QtCore # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
#TODO: Do we need this? I must check it later
class FACE_D:
	def __init__(self, view):
	   self.view = view
	   v=Gui.activeDocument().activeView()
		
	def getDirectionAxis(self):
		try:
			s=Gui.Selection.getSelectionEx()
			obj=s[0]
			faceSel = obj.SubObjects[0]
			dir = faceSel.normalAt(0,0)
			if dir.z == 1 :
				return "z"
			elif dir.y==1 :
				return "y"
			else :
				return "x"
		except ImportError as err:
			App.Console.PrintError("'FACE_D.getDirectionAxis' Failed. "
								   "{err}\n".format(err=str(err)))
				
	def MousePosition(self, info):
		try:
			down = (info["State"] == "DOWN")
			pos = info["Position"]
			#if (down):
			FreeCAD.Console.PrintMessage("Clicked on position: ("+str(pos[0])+", "+str(pos[1])+")\n")
			pnt = self.view.getPoint(pos)
			FreeCAD.Console.PrintMessage("World coordinates: " + str(pnt) + "\n")
			info = self.view.getObjectInfo(pos)
			FreeCAD.Console.PrintMessage("Object info: " + str(info) + "\n")
			o = ViewObserver(v)
			c = v.addEventCallback("SoMouseButtonEvent",o.logPosition)
			return pnt
		except ImportError as err:
			App.Console.PrintError("'FACE_D.getDirectionAxis' Failed. "
								   "{err}\n".format(err=str(err)))
			
	def ExtractFace(self):
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
			return self.newobj
				#o.Object.ViewObject.Visibility = False
		except ImportError as err:
			App.Console.PrintError("'FACE_D.ExtractFace' Failed. "
								   "{err}\n".format(err=str(err)))	